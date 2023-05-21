from typing import List
# from app.models.documents import Document
import PyPDF2

# def get_documents_chunks(document: Document, MAX_CHUNK_SIZE: int) -> List[str]:
#     pass

def read_pdf_generator(path: str):
    pdf_file = open(path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    
    return read_pdf_in_chunks(pdf_reader, pdf_file)


def read_pdf_in_chunks(pdf_reader, pdf_file):
    # Iterate over each page and extract text
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        yield text
    
    pdf_file.close()

# https://stackoverflow.com/questions/4576077/how-can-i-split-a-text-into-sentences

# if __name__ == "__main__":
#     pdf_gen = read_pdf_generator("C:\\Users\\Omri\\Desktop\\dev\\MrKnowAll\\backend\\resources\\israel-gaza.pdf")
#     print(pdf_gen.__next__())

