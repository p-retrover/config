# PDF Navigation & TOC Generation Notes

## Prerequisites & Assumptions

* **Standard Documents Only:** The Python TOC script relies on a standard text layout (chapters/sections followed by dot leaders or spaces and a numeric page number) and sequential page numbering. It works best on professionally typeset books, reports, and standard documents. It may fail on complex multi-column layouts, heavily stylized art books, or irregular table of contents formats.

## PDF Processing Workflow

1. **Check if PDF is Scanned (Image-only):**
   * If the PDF consists of flat images without selectable text, the Python script (`fitz.get_text("text")`) will fail to find any text lines.
2. **Run OCR (`ocrmypdf`):**
   * Convert image-only PDFs into searchable text PDFs first using `ocrmypdf`:

     ```bash
     ocrmypdf input_scanned.pdf output_searchable.pdf
     ```

   * *Note: Ensure you have `ocrmypdf` and its dependencies (like Tesseract) installed on your system.*
3. **Generate Clickable TOC / Bookmarks:**
   * Run the PyMuPDF script on the OCR'ed (or natively digital) PDF:

     ```bash
     python3 generate_toc.py
     ```

   * Adjust `toc_start_page`, `toc_end_page`, and `page_offset` to match the physical PDF page indexes vs. printed page numbers.
   * Add any missing front matter (Preface, Foreword, etc.) manually via the `front_matter` configuration list.
