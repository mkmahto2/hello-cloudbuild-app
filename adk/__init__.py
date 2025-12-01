"""ADK package for First Clinical Assistant — AI Agent.

This package provides a minimal, notebook-friendly Application Development Kit (ADK)
that wraps Google Cloud API calls where available and provides safe offline fallbacks
for development and testing.

Public API
- ClinicalAssistantADK: lightweight client class with methods like `analyze_text` and
  `summarize`.

Notes
- This scaffold intentionally avoids requiring Google Cloud libraries at import time.
  Use the `google_cloud_available()` helper to detect if the real client is usable.
"""

from .client import ClinicalAssistantADK  # re-export for convenience

__all__ = ["ClinicalAssistantADK"]
