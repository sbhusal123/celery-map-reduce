import pdfplumber


def get_no_of_pages(pdf_path):
    """Get no of pages in pdf"""
    page_count = 0
    with pdfplumber.open(pdf_path) as pdf:
        page_count = len(pdf.pages)
    return page_count

def extract_text(pdf_path, pages=[1, 2]):
    """Extract text from the pages mentioned in array."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        print("Number of pages=",len(pdf.pages))
        for page_num in pages:
            if page_num <= len(pdf.pages):
                text += pdf.pages[page_num - 1].extract_text() + "\n\n"
    return text

