# Examples

This folder contains small examples showing how to use the ADK. The examples
are intentionally simple to keep dependencies optional.

image_example.py
- Demonstrates image processing with three tiers of capability:
  1. Google Cloud Vision (if installed + authenticated)
  2. pytesseract (local OCR if installed)
  3. Pillow-only metadata fallback

Use case
- Extract text from scanned clinical notes or image-based reports for downstream
  NLP processing. Example flow:
  1. Run OCR on the image to extract text.
  2. Pass the extracted text to `adk.ClinicalAssistantADK.analyze_text()` to
     detect entities and compute a summary.

Example commands

```powershell
# Basic metadata fallback
python examples/image_example.py --image path/to/your/image.jpg

# If you have pytesseract installed, you may get OCR output locally
python -m pip install pillow pytesseract
python examples/image_example.py --image path/to/your/image.jpg

# If you have Google Cloud Vision configured, you'll get Vision OCR output
python -m pip install google-cloud-vision
setx GOOGLE_APPLICATION_CREDENTIALS "C:\path\to\creds.json"
python examples/image_example.py --image path/to/your/image.jpg
```

Privacy note
- OCR and image processing may surface PHI. Use appropriate safeguards when
  processing clinical images.
