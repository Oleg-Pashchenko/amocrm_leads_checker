import PyPDF2


def extract_text_from_pdf(pdf_file_path):
    text = ""
    with open(pdf_file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text().replace('\n', ' ')
        file.close()
    return text


extracted_text = extract_text_from_pdf(pdf_file_path='description.pdf')
print(extracted_text)
