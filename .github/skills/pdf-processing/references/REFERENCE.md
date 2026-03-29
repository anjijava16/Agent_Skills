# PDF Processing — Advanced Reference

## Custom Table Settings

When default table detection fails (tables without borders, merged cells):

```python
table_settings = {
    "vertical_strategy": "text",
    "horizontal_strategy": "text",
    "snap_tolerance": 5,
}

with pdfplumber.open("input.pdf") as pdf:
    page = pdf.pages[0]
    tables = page.extract_tables(table_settings=table_settings)
```

### Strategy Options

| Strategy | When to use |
|----------|------------|
| `"lines"` (default) | Tables with visible borders |
| `"text"` | Tables aligned by text position, no borders |
| `"explicit"` | When you define exact line positions |

## Extracting Specific Regions

Crop a page before extraction to get text from a specific area:

```python
with pdfplumber.open("input.pdf") as pdf:
    page = pdf.pages[0]
    # Crop to top-right quadrant (coordinates: x0, top, x1, bottom)
    bbox = (page.width / 2, 0, page.width, page.height / 2)
    cropped = page.crop(bbox)
    text = cropped.extract_text()
```

## Handling Multi-Column Layouts

pdfplumber reads left-to-right, top-to-bottom by default. For multi-column PDFs:

```python
with pdfplumber.open("input.pdf") as pdf:
    page = pdf.pages[0]
    mid = page.width / 2
    left_col = page.crop((0, 0, mid, page.height)).extract_text()
    right_col = page.crop((mid, 0, page.width, page.height)).extract_text()
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `extract_text()` returns None | Scanned/image PDF | Use OCR pipeline |
| Garbled characters | Font encoding issues | Try `pypdf` as alternative: `page.extract_text()` |
| Tables misaligned | No visible borders | Use `"text"` strategy in table_settings |
| Slow on large PDFs | Loading all pages | Process page-by-page with index |
| `pdftoppm` not found | poppler not installed | `brew install poppler` (macOS) |
| OCR quality poor | Low DPI source | Increase DPI: `convert_from_path(path, dpi=400)` |
