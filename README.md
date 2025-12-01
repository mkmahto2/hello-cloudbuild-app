# First Clinical Assistant — ADK (Google ADK + Google Cloud API)

A notebook-first, lightweight Application Development Kit (ADK) for the
"First Clinical Assistant" research prototype. This repository provides a
minimal ADK that wraps Google Cloud NLP (when available) and safe offline
fallbacks for local development, demos, and CI.

IMPORTANT: This is a research/education prototype and must not be used for
autonomous clinical decision-making. Treat any PHI with appropriate safeguards.

Repository layout

- `adk/` — ADK package exposing `ClinicalAssistantADK` (text analysis + summarization).
- `examples/` — example scripts (image OCR pipeline and README).
- `tests/` — unit tests for ADK fallback behavior.
- `run_tests.py` — lightweight runner for the tests (no pytest required).
- `requirements.txt` — optional dependencies (cloud clients, OCR libs, test tooling).

Quick checklist (Windows / PowerShell)

1. Install Python 3.8+ (3.10+ recommended).
2. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. (Optional) Install the minimal dependencies for development:

```powershell
python -m pip install -U pip
python -m pip install -r requirements.txt
```

Run the included tests (lightweight runner — no pytest required):

```powershell
python run_tests.py
```

If you prefer pytest (recommended for richer output):

```powershell
python -m pip install pytest
python -m pytest -q
```

Using the ADK in code or notebooks

Example: analyze a short clinical note

```python
from adk import ClinicalAssistantADK

client = ClinicalAssistantADK()
note = "John Doe, 55, presented with fever and productive cough. Symptoms improved after antibiotics."
result = client.analyze_text(note)
print(result)

summary = client.summarize(note, max_sentences=2)
print('Summary:', summary)
```

Image OCR -> NLP end-to-end example

This repository includes `examples/image_example.py` which demonstrates a
three-tier approach for extracting text from images:

1. Google Cloud Vision (if `google-cloud-vision` is installed and credentials are set).
2. Local OCR using `pytesseract` (if installed and Tesseract engine available).
3. Pillow-only metadata fallback (format/size/mode) when OCR is unavailable.

Example flow (OCR text passed to ADK for analysis):

```python
from adk import ClinicalAssistantADK
import subprocess, json

# run the example script to get OCR text (or metadata)
# on success it prints JSON with keys like 'vision_text' or 'tesseract_text'
proc = subprocess.run(['python','examples/image_example.py','--image','C:\path\to\image.jpg'], capture_output=True, text=True)
data = json.loads(proc.stdout)

text = data.get('vision_text') or data.get('tesseract_text') or ''
client = ClinicalAssistantADK()
if text:
    analysis = client.analyze_text(text)
    print(analysis)
else:
    print('No OCR text available, metadata:', data.get('metadata'))
```

Installation notes — optional dependencies

- Google Cloud NLP: `google-cloud-language` — used by `ClinicalAssistantADK`
- Google Cloud Vision: `google-cloud-vision` — used by `examples/image_example.py`
- Local OCR: `pytesseract` + Tesseract engine + `Pillow`

Install OCR support (local):

```powershell
python -m pip install Pillow pytesseract
# On Windows, install the Tesseract binary from https://github.com/tesseract-ocr/tesseract/releases
# and add the install folder (e.g., C:\Program Files\Tesseract-OCR) to your PATH.
```

Install Google Cloud vision (optional):

```powershell
python -m pip install google-cloud-vision google-cloud-language
setx GOOGLE_APPLICATION_CREDENTIALS "C:\path\to\service-account.json"
```

API reference (minimal)

- ClinicalAssistantADK(project: Optional[str])
  - analyze_text(text: str) -> dict
    - Returns: {'entities': [...], 'sentiment': {'score': float,'magnitude': float}, 'tokens': int}
    - Uses Google Cloud NLP if available, otherwise a deterministic fallback.
  - summarize(text: str, max_sentences: int = 3) -> str
    - Returns an extractive-style short summary using a simple heuristic in fallback mode.

Development & testing

- Use the lightweight runner to validate the scaffold without installing pytest:

```powershell
python run_tests.py
```

- For CI: add a job that creates a venv, installs dev deps, and runs `python run_tests.py`.

Security & privacy

- This repository contains example code for processing clinical text and images.
  Do not upload PHI to public cloud accounts without proper safeguards and
  administrative approvals. Use secure environments and de-identification when
  working with real patient data.

Contributing

- Please open issues or PRs for bug fixes and useful feature additions (PHI
  redaction, structured extraction, connectors to secure storage, etc.).

License

Add an appropriate LICENSE file for your project. This scaffold does not
include a license by default.
