import re
import pymupdf  # PyMuPDF


def create_clickable_toc(
    pdf_path: str,
    output_path: str,
    toc_start_page: int,
    toc_end_page: int,
    page_offset: int,
    front_matter: list = None,
):
    """
    :param page_offset: Difference between physical PDF page and printed page (Physical - Printed)
    :param front_matter: Optional list of tuples: [("Title", physical_pdf_page_number)]
    """
    doc = pymupdf.open(pdf_path)
    extracted_toc = []

    # 1. Add any preliminary / front matter bookmarks manually
    if front_matter:
        for title, phys_page in front_matter:
            extracted_toc.append([1, title, phys_page])

    # 2. Extract standard numbered chapters from TOC pages
    for page_num in range(toc_start_page - 1, toc_end_page):
        page = doc[page_num]
        lines = page.get_text("text").split("\n")

        for line in lines:
            line = line.strip()
            match = re.search(r"^(.*?)\s*[\.\s\-_·]*\s*(\d+)$", line)

            if match:
                title = match.group(1).strip()
                printed_page = int(match.group(2))

                # Apply the offset to map printed number -> physical PDF page
                target_physical_page = printed_page + page_offset

                if len(title) > 2 and 1 <= target_physical_page <= len(doc):
                    level = 1
                    if title.lower().startswith(
                        ("section", "subsection", "-", "•")
                    ):
                        level = 2
                    extracted_toc.append([level, title, target_physical_page])

    if not extracted_toc:
        print("No entries generated. Check your TOC page range or regex.")
        return

    doc.set_toc(extracted_toc)
    doc.save(output_path)
    print(f"Generated PDF with {len(extracted_toc)} bookmarks at '{output_path}'")


# === CONFIGURATION ===
if __name__ == "__main__":
    # Add any pages that come before Chapter 1 with their direct PDF page numbers
    custom_front_matter = [
        ("Cover", 1),
        ("Table of Contents", 3),
        ("Preface", 10),
    ]

    create_clickable_toc(
        pdf_path="input.pdf",
        output_path="output_clickable.pdf",
        toc_start_page=3,  # PDF page where TOC starts
        toc_end_page=9,  # PDF page where TOC ends
        page_offset=19,  # (PDF page of Chapter 1) - (Printed page number of Chapter 1)
        front_matter=custom_front_matter,
    )
