"""Unit tests for the ADK client.

These tests avoid requiring Google Cloud libraries by exercising the offline
fallback behavior. They validate small, deterministic behaviors so the scaffold
is testable in CI without external access.
"""
from adk import ClinicalAssistantADK


def test_analyze_text_empty():
    client = ClinicalAssistantADK()
    res = client.analyze_text("")
    assert res["entities"] == []
    assert res["tokens"] == 0
    assert isinstance(res["sentiment"], dict)


def test_analyze_text_basic_entities_and_sentiment():
    client = ClinicalAssistantADK()
    text = "John Doe presented with fever and cough. Symptoms improved after treatment."
    res = client.analyze_text(text)
    # tokens > 0
    assert res["tokens"] > 0
    # 'John' or 'John Doe' should be detected as a proper noun entity by heuristic
    names = [e["name"] for e in res["entities"]]
    assert any("John" in n for n in names)
    # sentiment score should be a float
    assert isinstance(res["sentiment"]["score"], float)


def test_summarize_short_text():
    client = ClinicalAssistantADK()
    s = "Line one. Line two. Line three."
    summary = client.summarize(s, max_sentences=2)
    # Summary should contain at most 2 sentences
    assert summary.count('.') <= 2
