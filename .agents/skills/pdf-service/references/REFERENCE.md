# PDF Service — Advanced Reference

## Watermarking

```python
from pypdf import PdfReader, PdfWriter

stamp = PdfReader("watermark.pdf").pages[0]
reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(stamp)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as f:
    writer.write(f)
```

## Encryption / Decryption

Encrypt with a password:

```python
from pypdf import PdfWriter

writer = PdfWriter("input.pdf")
writer.encrypt(user_password="read_pass", owner_password="owner_pass")
with open("encrypted.pdf", "wb") as f:
    writer.write(f)
```

## Metadata Editing

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()
writer.append(reader)
writer.add_metadata({
    "/Author": "Your Name",
    "/Title": "Document Title",
    "/Subject": "Subject",
})
with open("output.pdf", "wb") as f:
    writer.write(f)
```

## OCR Pipeline for Scanned PDFs

```python
from pdf2image import convert_from_path
import pytesseract

images = convert_from_path("scanned.pdf", dpi=300)
full_text = []
for img in images:
    text = pytesseract.image_to_string(img)
    full_text.append(text)

result = "\n---\n".join(full_text)
```

## Redaction with pikepdf

```python
import pikepdf

pdf = pikepdf.open("input.pdf")
# pikepdf provides low-level access for content stream manipulation
# Use for removing or replacing specific content objects
pdf.save("redacted.pdf")
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `extract_text()` returns None | Scanned/image PDF | Use OCR pipeline above |
| `PdfReadError: EOF marker not found` | Corrupted PDF | Try `pikepdf.open()` which has better error recovery |
| `convert_from_path` fails | poppler not installed | `brew install poppler` (macOS) |
| Form fields not updating visually | Need to set `/NeedAppearances` | `writer._root_object["/AcroForm"]["/NeedAppearances"] = True` |
| Merged PDF has wrong page size | Source PDFs have different dimensions | This is expected; each page keeps its original size |
