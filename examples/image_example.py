"""Image example for the First Clinical Assistant ADK.

This script demonstrates a small, safe example of processing an image that
may contain clinical text (scanned notes, reports). It attempts to use Google
Cloud Vision if installed and credentials are available. Otherwise it falls
back to pytesseract (if installed) or to a simple metadata-only fallback using
Pillow.

Usage:
    python examples/image_example.py --image PATH/TO/IMAGE.jpg

Outputs a JSON-like summary to stdout with one of:
- `vision_text` from Google Cloud Vision
- `tesseract_text` from pytesseract
- `metadata` with basic image info

This is intended as an example and not production-ready OCR/PII handling.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Dict, Any


def try_google_vision(image_path: str) -> Dict[str, Any] | None:
    try:
        from google.cloud import vision  # type: ignore

        client = vision.ImageAnnotatorClient()
        with open(image_path, "rb") as f:
            content = f.read()
        image = vision.Image(content=content)
        resp = client.document_text_detection(image=image)
        if resp.error.message:
            return {"error": resp.error.message}
        return {"vision_text": resp.full_text_annotation.text}
    except Exception:
        return None


def try_pytesseract(image_path: str) -> Dict[str, Any] | None:
    try:
        from PIL import Image
        import pytesseract

        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return {"tesseract_text": text}
    except Exception:
        return None


def fallback_metadata(image_path: str) -> Dict[str, Any]:
    try:
        from PIL import Image

        img = Image.open(image_path)
        return {
            "metadata": {
                "format": img.format,
                "size": img.size,
                "mode": img.mode,
            }
        }
    except Exception as e:
        return {"error": str(e)}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Image example for ADK")
    p.add_argument("--image", required=True, help="Path to image file")
    args = p.parse_args(argv)

    image_path = args.image

    # Try Google Vision first
    out = try_google_vision(image_path)
    if out is not None:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0

    # Try pytesseract next
    out = try_pytesseract(image_path)
    if out is not None:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0

    # Fallback to metadata
    out = fallback_metadata(image_path)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
