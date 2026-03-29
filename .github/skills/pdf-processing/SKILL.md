---
name: pdf-processing
description: >
  Extract text, tables, and metadata from PDF documents. Parse scanned PDFs
  with OCR, analyze PDF structure, and convert PDFs to other formats. Use when
  the user needs to read, parse, or extract content from PDF files, even if they
  just say "get the text from this document."
license: MIT
compatibility: Requires Python 3.10+ and pip. OCR requires tesseract and poppler.
metadata:
  author: welcome
  version: "1.0"
---

# PDF Processing

## When to use this skill

Use this skill when the user needs to:
- Extract text or tables from PDF documents
- Parse scanned/image-based PDFs using OCR
- Read PDF metadata (author, title, page count, creation date)
- Convert PDF pages to images
- Analyze PDF structure (fonts, layout, embedded objects)

## Prerequisites

```bash
pip install pdfplumber pypdf pdf2image
```

For OCR on scanned PDFs:

```bash
pip install pytesseract Pillow
brew install tesseract poppler  # macOS
```

## Text Extraction

Use pdfplumber as the default. It handles most PDFs well.

```python
import pdfplumber

with pdfplumber.open("input.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            print(f"--- Page {i + 1} ---")
            print(text)
        else:
            print(f"--- Page {i + 1}: no text (likely scanned) ---")
```

### OCR Fallback for Scanned PDFs

When `extract_text()` returns `None` or empty string, the PDF is image-based. Fall back to OCR:

```python
from pdf2image import convert_from_path
import pytesseract

images = convert_from_path("scanned.pdf", dpi=300)
for i, img in enumerate(images):
    text = pytesseract.image_to_string(img)
    print(f"--- Page {i + 1} ---")
    print(text)
```

Use `scripts/extract_text.py` for automatic detection and OCR fallback.

## Table Extraction

```python
with pdfplumber.open("input.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                print(row)
```

For structured output, convert tables to pandas DataFrames:

```python
import pandas as pd

with pdfplumber.open("input.pdf") as pdf:
    tables = pdf.pages[0].extract_tables()
    if tables:
        df = pd.DataFrame(tables[0][1:], columns=tables[0][0])
        print(df.to_markdown(index=False))
```

## PDF Metadata

```python
from pypdf import PdfReader

reader = PdfReader("input.pdf")
meta = reader.metadata
print(f"Pages: {len(reader.pages)}")
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Creator: {meta.creator}")
print(f"Created: {meta.creation_date}")
```

## PDF to Images

```python
from pdf2image import convert_from_path

images = convert_from_path("input.pdf", dpi=300)
for i, img in enumerate(images):
    img.save(f"page_{i + 1}.png", "PNG")
```

## Gotchas

- **pdfplumber for reading, pypdf for writing**: pdfplumber excels at text/table extraction. Use pypdf for merge/split/form operations (see `pdf-service` skill).
- **Scanned PDFs return empty text**: Always check if `extract_text()` returns `None` or `""` and fall back to OCR.
- **pdf2image requires poppler**: On macOS: `brew install poppler`. Without it, `convert_from_path` fails with a cryptic error about `pdftoppm`.
- **Table extraction is layout-dependent**: pdfplumber uses visual line detection. Tables without visible borders may need `table_settings` tuning.
- **Large PDFs**: Process page-by-page. Never load all pages into memory at once.
- **Password-protected PDFs**: Use `PdfReader("file.pdf", password="secret")`. An empty password (`""`) works for some "encrypted" PDFs that aren't truly locked.

## Validation

After extraction:
1. Spot-check extracted text against the original PDF
2. For tables, verify column count and row count match the source
3. For OCR, check for common misreads (0/O, 1/l/I, rn/m)

## References

- See [references/REFERENCE.md](references/REFERENCE.md) for advanced extraction patterns and troubleshooting
