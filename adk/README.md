# ADK for First Clinical Assistant — AI Agent

This folder contains a small, notebook-friendly Application Development Kit (ADK)
for the First Clinical Assistant research prototype. The ADK is intentionally
minimal and provides safe fallbacks so notebooks and CI can import it without
network access or Google Cloud credentials.

Contents
- `client.py` — `ClinicalAssistantADK` class with `analyze_text` and `summarize`.

Quick start
1. In a notebook:
   from adk import ClinicalAssistantADK
   client = ClinicalAssistantADK()
   client.analyze_text("Patient with fever and cough.")

Notes
- If `google-cloud-language` is installed and credentials are available, the ADK
  will attempt to use the real Google Cloud NLP APIs. Otherwise it uses a
  deterministic offline fallback which is suitable for demos and unit tests.
