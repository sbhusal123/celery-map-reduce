import pdfplumber

def extract_text_from_pdf(pdf_path, pages=[1, 2]):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        # print("Number of pages=",len(pdf.pages))
        for page_num in pages:
            if page_num <= len(pdf.pages):  # Ensure the page exists
                text += pdf.pages[page_num - 1].extract_text() + "\n\n\n"
    return text


# print(extracted_text)

if __name__ == "__main__":
    pdf_file = "src/media/pdfs/file-example_PDF_1MB.pdf"
    extracted_text = extract_text_from_pdf(pdf_file, pages=[3, 5])
    print(extracted_text)
