---
name: pdf-service
description: >
  Extract text and tables from PDFs, fill PDF forms, merge and split PDF files,
  and convert PDFs to other formats. Use when the user mentions PDFs, document
  extraction, form filling, or needs to manipulate PDF files.
license: MIT
compatibility: Requires Python 3.10+ and pip
metadata:
  author: welcome
  version: "1.0"
---

# PDF Service

## When to use this skill

Use this skill when the user needs to:
- Extract text or tables from PDF documents
- Fill out PDF form fields programmatically
- Merge multiple PDFs into one or split a PDF into pages
- Convert PDFs to images or other formats
- Analyze PDF structure (page count, metadata, form fields)

## Prerequisites

Install dependencies before first use:

```bash
pip install pdfplumber pypdf reportlab pdf2image pikepdf
```

For scanned/image-based PDFs requiring OCR:

```bash
pip install pytesseract Pillow
brew install tesseract  # macOS
```

## Text Extraction

Use pdfplumber for text extraction. For scanned documents, fall back to pdf2image with pytesseract.

```python
import pdfplumber

with pdfplumber.open("input.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            print(text)
```

For tables:

```python
with pdfplumber.open("input.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                print(row)
```

## Form Filling

Use the plan-validate-execute pattern:

1. **Analyze** — List all form fields:

```python
from pypdf import PdfReader

reader = PdfReader("form.pdf")
fields = reader.get_fields()
for name, field in fields.items():
    print(f"{name}: type={field.get('/FT')}, value={field.get('/V')}")
```

2. **Map** — Create a dict mapping field names to values
3. **Fill** — Write values into the form:

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("form.pdf")
writer = PdfWriter()
writer.append(reader)
writer.update_page_form_field_values(writer.pages[0], {"field_name": "value"})
with open("filled.pdf", "wb") as f:
    writer.write(f)
```

## Merge and Split

Merge multiple PDFs:

```python
from pypdf import PdfMerger

merger = PdfMerger()
for path in ["file1.pdf", "file2.pdf", "file3.pdf"]:
    merger.append(path)
merger.write("merged.pdf")
merger.close()
```

Split into individual pages:

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    writer.write(f"page_{i + 1}.pdf")
```

## PDF to Images

```python
from pdf2image import convert_from_path

images = convert_from_path("input.pdf", dpi=300)
for i, img in enumerate(images):
    img.save(f"page_{i + 1}.png", "PNG")
```

## Gotchas

- **pdfplumber vs pypdf**: Use pdfplumber for *reading* text/tables. Use pypdf for *writing* (merge, split, form fill). They solve different problems.
- **Scanned PDFs return empty text**: `extract_text()` returns `None` or `""` for image-based PDFs. Detect this and fall back to OCR with pytesseract.
- **Form field names are case-sensitive** and often contain spaces or special characters. Always list fields first before attempting to fill.
- **Encrypted PDFs**: pypdf can open PDFs with an empty password (`PdfReader("file.pdf", password="")`), but truly encrypted files need the actual password.
- **Large PDFs**: Process page-by-page instead of loading entire documents into memory.
- **pdf2image requires poppler**: On macOS install via `brew install poppler`. Without it, `convert_from_path` will fail with a cryptic error.

## Validation

After any PDF operation:
1. Open the output file to verify it renders correctly
2. For form fills, re-read the filled PDF and check field values match expected
3. For merges, verify page count equals sum of input page counts

## References

- See [references/REFERENCE.md](references/REFERENCE.md) for advanced patterns (watermarks, encryption, metadata editing)
