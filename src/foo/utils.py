import pdfplumber

def extract_text_from_pdf(pdf_path, pages=[1, 2]):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        print("Number of pages=",len(pdf.pages))
        for page_num in pages:
            if page_num <= len(pdf.pages):
                text += pdf.pages[page_num - 1].extract_text() + "\n\n"
    return text

