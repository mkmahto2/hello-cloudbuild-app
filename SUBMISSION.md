# First Clinical Assistant — ADK Submission

## Title (Required to save)
**First Clinical Assistant — Notebook-First AI Agent with Google Cloud API**

---

## Subtitle
Lightweight, open-source ADK for clinical text & image analysis with safe offline fallbacks and PHI redaction helpers.

---

## Card and Thumbnail Image

**Thumbnail Description:**
A visual showing:
- Python + Google Cloud icons
- Clinical workflow (document → OCR → NLP analysis)
- Safe/secure badge (PHI redaction)
- GitHub + CI/CD indicators

**File:** `docs/thumbnail.png` (1200×630px recommended for GitHub/web cards)
*(To be added: high-quality clinical AI workflow diagram)*

---

## Submission Tracks

- **Healthcare AI / Clinical NLP** — Text analysis and entity extraction from clinical notes
- **Data Privacy & Security** — PHI redaction, de-identification, safe offline modes
- **Open Source Tooling** — Python ADK, fallback patterns, notebook-first design
- **Google Cloud Integration** — Optional Cloud NLP, Cloud Vision with local fallbacks

---

## Content

### Project Description

**First Clinical Assistant** is a notebook-native, lightweight Application Development Kit (ADK) for medical AI research and clinical text/image analysis. Built on Python with optional Google Cloud integration, it provides:

- **ClinicalAssistantADK** class for text analysis (entity extraction, sentiment, summarization)
- **PHI Redaction helpers** for safe de-identification (dates, SSNs, MRNs, names)
- **Image OCR pipeline** with three-tier fallback (Google Vision → pytesseract → metadata)
- **Demo Jupyter notebook** showing end-to-end OCR→NLP workflow
- **GitHub Actions CI** for automated testing without network access
- **Safe offline mode** — all code runs locally with deterministic fallbacks when cloud libraries unavailable

**Key Features:**
1. **Cloud-Optional**: Uses Google Cloud NLP/Vision when available and credentials are set; gracefully falls back to deterministic local logic for development and CI.
2. **Privacy-Aware**: Includes regex-based PHI redaction (rule-based, not ML; suitable for demos and research; not production-grade).
3. **Notebook-First**: Designed to work seamlessly in Jupyter notebooks and VS Code notebooks with minimal dependencies.
4. **Lightweight Test Suite**: Includes a custom test runner (`run_tests.py`) that runs without pytest, enabling CI without external installs.
5. **Comprehensive Examples**: Image processing, text analysis, redaction workflows, and a bundled demo image.

**Intended Use Cases:**
- Medical AI research and prototyping
- Clinical note analysis and summarization
- Scanned document OCR and extraction workflows
- Safe de-identification pipelines for HIPAA compliance research
- Teaching clinical NLP and privacy-aware AI design

**Important Disclaimer:**
This is a research/education prototype. It is not intended for autonomous clinical decision-making. All processed data should be treated with appropriate security and privacy safeguards.

---

## Project Links

### Repository
- **GitHub**: https://github.com/mkmahto2/hello-cloudbuild-app
- **Branch**: `main`
- **Status**: Active development

### Documentation
- **README**: https://github.com/mkmahto2/hello-cloudbuild-app/blob/main/README.md
- **ADK README**: https://github.com/mkmahto2/hello-cloudbuild-app/tree/main/adk
- **Examples README**: https://github.com/mkmahto2/hello-cloudbuild-app/tree/main/examples
- **Demo Notebook**: https://github.com/mkmahto2/hello-cloudbuild-app/blob/main/examples/demo_notebook.ipynb

### Key Files
- **ADK Client**: `adk/client.py` — Main API (analyze_text, summarize, redact_phi)
- **Tests**: `tests/test_client.py`, `tests/test_redaction.py` — Unit tests
- **Image Example**: `examples/image_example.py` — OCR pipeline
- **CI Workflow**: `.github/workflows/ci.yml` — GitHub Actions (runs on push/PR)
- **Test Runner**: `run_tests.py` — Lightweight test runner

### Quick Start
```powershell
# Clone the repo
git clone https://github.com/mkmahto2/hello-cloudbuild-app.git
cd hello-cloudbuild-app

# Create virtual environment
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1

# Run tests
python run_tests.py

# Use the ADK
python -c "from adk import ClinicalAssistantADK; client = ClinicalAssistantADK(); print(client.analyze_text('Patient with fever'))"
```

### Installation (Optional Dependencies)
```powershell
# Google Cloud support
python -m pip install google-cloud-language google-cloud-vision

# Local OCR
python -m pip install Pillow pytesseract
# Then install Tesseract binary from https://github.com/tesseract-ocr/tesseract

# Full dev environment
python -m pip install -r requirements.txt
```

---

## Technology Stack

- **Language**: Python 3.8+
- **Core Libraries**: (no hard dependencies in base ADK)
- **Optional Cloud**: Google Cloud NLP, Google Cloud Vision
- **Optional Local**: Pillow (image), pytesseract (OCR), pytest (testing)
- **CI/CD**: GitHub Actions
- **Notebooks**: Jupyter, VS Code Notebooks

---

## Team & Contact

- **Owner/Maintainer**: mkmahto2 (GitHub)
- **Repository**: mkmahto2/hello-cloudbuild-app
- **Issues & Contributions**: Open to community PRs and issue reports

---

## License

To be determined. Project is currently provided for research/education purposes.

---

## Roadmap & Future Work

- [ ] Add production-grade PHI redaction (integrate vetted library like `presidio`)
- [ ] Expand entity extraction (anatomy, medications, procedures)
- [ ] Add structured extraction (lab results, vital signs)
- [ ] Connectors to secure storage (Cloud Storage, BigQuery)
- [ ] Async variants for notebook environments
- [ ] Comprehensive end-to-end demo with sample de-identified clinical data
- [ ] Docker image for easy deployment
- [ ] Integration with popular clinical NLP libraries (spaCy, scispaCy, etc.)

---

## Acknowledgments

Built with:
- Google Cloud Platform APIs (NLP, Vision)
- Python ecosystem (Pillow, pytesseract)
- Open-source community tools and best practices

This project is inspired by the need for safe, accessible clinical AI research tools that prioritize privacy and ease of use.

