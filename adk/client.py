"""Lightweight ADK client for the First Clinical Assistant.

This module provides a `ClinicalAssistantADK` class with simple methods for
analyzing and summarizing clinical text. When Google Cloud client libraries are
available and authenticated, the class will attempt to use them; otherwise it
falls back to deterministic, offline behavior suitable for development and tests.

The code is intentionally small and dependency-light so notebooks can import it
without network access.
"""
from typing import Dict, Any

def google_cloud_available() -> bool:
    """Return True if a real Google Cloud NLP library is importable.

    We avoid importing cloud libraries at module import time; this helper
    attempts a lazy import when called.
    """
    try:
        import google.cloud.language_v1  # type: ignore
        return True
    except Exception:
        return False


class ClinicalAssistantADK:
    """Minimal ADK client exposing text analysis helpers.

    Methods are synchronous and return plain Python types (dicts/strings).

    Usage:
        from adk import ClinicalAssistantADK
        client = ClinicalAssistantADK()
        result = client.analyze_text("Patient has a fever and cough.")
    """

    def __init__(self, project: str | None = None):
        self.project = project
        self._use_cloud = google_cloud_available()

        # Lazy client placeholder — created on first cloud call to avoid import
        # errors when libraries are missing.
        self._nlp_client = None

    def _ensure_nlp_client(self):
        """Create the Google Cloud NLP client if available.

        Returns True if a client is available, otherwise False.
        """
        if not self._use_cloud:
            return False
        if self._nlp_client is None:
            try:
                from google.cloud import language_v1  # type: ignore

                self._nlp_client = language_v1.LanguageServiceClient()
            except Exception:
                self._nlp_client = None
                self._use_cloud = False
                return False
        return True

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze a piece of clinical text and return a small structured result.

        The returned dict contains:
        - `entities`: list of {name, type, salience}
        - `sentiment`: {score, magnitude} (may be approximate in fallback)
        - `tokens`: token count

        The implementation uses Google Cloud NLP when available; otherwise it
        returns a deterministic fallback that is useful for testing and demos.
        """
        if not text:
            return {"entities": [], "sentiment": {"score": 0.0, "magnitude": 0.0}, "tokens": 0}

        if self._ensure_nlp_client():
            # Real Google Cloud NLP path
            from google.cloud import language_v1  # type: ignore

            document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
            # Entities
            entities_resp = self._nlp_client.analyze_entities(request={"document": document})
            entities = []
            for e in entities_resp.entities:
                entities.append({"name": e.name, "type": language_v1.Entity.Type(e.type_).name, "salience": e.salience})
            # Sentiment (may require a separate API call depending on client)
            try:
                sentiment_resp = self._nlp_client.analyze_sentiment(request={"document": document})
                sentiment = {"score": sentiment_resp.document_sentiment.score, "magnitude": sentiment_resp.document_sentiment.magnitude}
            except Exception:
                sentiment = {"score": 0.0, "magnitude": 0.0}

            tokens = len(text.split())
            return {"entities": entities, "sentiment": sentiment, "tokens": tokens}

        # Fallback deterministic analysis (no external calls)
        tokens = len(text.split())
        # Very small heuristic: find capitalized words as possible entities
        words = text.replace(".", " ").replace(",", " ").split()
        entities = []
        for w in words:
            if w[0].isupper() and len(w) > 2:
                entities.append({"name": w, "type": "PROPER_NOUN", "salience": 0.5})

        # Sentiment heuristic: presence of negation lowers score, presence of 'good'/'improved' raises
        score = 0.0
        lowered = text.lower()
        if any(x in lowered for x in ["improved", "better", "stable"]):
            score += 0.6
        if any(x in lowered for x in ["worse", "worsening", "decline", "deterior"]):
            score -= 0.6
        if any(x in lowered for x in ["pain", "fever", "cough", "shortness"]):
            score -= 0.2

        # magnitude as normalized token-based value
        magnitude = min(5.0, tokens / 10.0)

        return {"entities": entities, "sentiment": {"score": score, "magnitude": magnitude}, "tokens": tokens}

    def summarize(self, text: str, max_sentences: int = 3) -> str:
        """Return a short extractive-style summary of the text.

        This method uses a simple sentence-rank heuristic in the fallback mode and
        delegates to cloud summarization if available (not implemented here).
        """
        if not text:
            return ""

        # Very small fallback: split into sentences and pick the longest N sentences
        import re

        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
        if len(sentences) <= max_sentences:
            return " ".join(sentences)

        # rank by sentence length as a proxy for importance
        ranked = sorted(sentences, key=lambda s: len(s), reverse=True)
        chosen = ranked[:max_sentences]
        # Preserve original order
        chosen_sorted = [s for s in sentences if s in chosen]
        return " ".join(chosen_sorted)

    def redact_phi(self, text: str, redact_names: bool = True, redact_dates: bool = True, redact_ids: bool = True) -> str:
        """Return a redacted copy of `text` where simple PHI patterns are replaced.

        This is a heuristic, rule-based redactor intended for demos and tests.
        It is NOT a production-grade PHI redaction implementation. The method
        applies simple regex-based rules for:
        - dates (YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY)
        - SSN-like patterns (###-##-####)
        - long numeric IDs (MRNs) of 6+ digits
        - simple Titlecase name sequences (e.g., "John Doe") when `redact_names` is True

        Returns the redacted string. Example replacement tokens: [REDACTED_NAME],
        [REDACTED_DATE], [REDACTED_ID].
        """
        import re

        out = text

        if redact_dates:
            # ISO-like dates
            out = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", "[REDACTED_DATE]", out)
            # Common slashed dates DD/MM/YYYY or MM/DD/YYYY
            out = re.sub(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", "[REDACTED_DATE]", out)

        if redact_ids:
            # SSN-like
            out = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_ID]", out)
            # Long numeric identifiers (e.g., MRN): 6 or more consecutive digits
            out = re.sub(r"\b\d{6,}\b", "[REDACTED_ID]", out)

        if redact_names:
            # Improved heuristic:
            # - Redact sequences of 2-3 Titlecase words (e.g., "John Doe", "Mary Ann Lee").
            # - Also redact single Titlecase word when preceded by honorifics or labels
            #   like 'Dr.', 'Mr.', 'Mrs.', 'Ms.', or the word 'Patient'.
            def _name_replacer(m: re.Match) -> str:
                return "[REDACTED_NAME]"

            # sequences of 2-3 Titlecase words
            out = re.sub(r"\b([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,}){1,2})\b", _name_replacer, out)

            # honorifics or labels followed by a single Titlecase word (e.g., "Dr. John")
            out = re.sub(r"\b(?:Dr\.|Mr\.|Mrs\.|Ms\.|Patient)\s+([A-Z][a-z]{2,})\b", lambda m: m.group(0).split()[0] + " [REDACTED_NAME]", out)

        return out
