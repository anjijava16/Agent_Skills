#!/usr/bin/env python3
"""Extract text from a PDF file, with OCR fallback for scanned documents."""

import sys

def extract_text(pdf_path: str) -> str:
    import pdfplumber

    pages_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and text.strip():
                pages_text.append(text)
            else:
                # OCR fallback
                try:
                    from pdf2image import convert_from_path
                    import pytesseract

                    images = convert_from_path(pdf_path, first_page=i + 1, last_page=i + 1, dpi=300)
                    ocr_text = pytesseract.image_to_string(images[0])
                    pages_text.append(ocr_text)
                except ImportError:
                    pages_text.append(f"[Page {i + 1}: scanned image — install pdf2image and pytesseract for OCR]")

    return "\n---\n".join(pages_text)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_text.py <pdf_path>", file=sys.stderr)
        sys.exit(1)
    print(extract_text(sys.argv[1]))
