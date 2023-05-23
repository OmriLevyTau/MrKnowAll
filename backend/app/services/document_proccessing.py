import logging
from typing import List

import nltk
import PyPDF2

from app.models.documents import Document
from app.services.embeddings import MAX_SEQ

# Download the necessary data for sentence tokenization
nltk.download("punkt")

def get_documents_chunks(document: Document) -> List[str]:
    path = document.path
    chunks = get_document_chunks_helper(path)
    return chunks


def get_document_chunks_helper(path: str) -> List[str]:
    pages = read_pdf_generator(path=path)
    result = []
    for page in pages:
        page_sentences = nltk.sent_tokenize(page)
        for sentence in page_sentences:
            if sentence.count(" ") < MAX_SEQ:
                result.append(sentence)
    return result


def read_pdf_generator(path: str):
    pdf_file = open(path, "rb")
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    return read_pdf_in_chunks(pdf_reader, pdf_file)


def read_pdf_in_chunks(pdf_reader, pdf_file):
    # Iterate over each page and extract text
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        yield text

    pdf_file.close()


# if __name__ == "__main__":
#     answer = get_document_chunks_helper(
#         "C:\\Users\\idani\\Desktop\\dev\\MrKnowAll\\backend\\resources\\israel-gaza.pdf")
#     maximum = 0
#     sentence = ""
#     for j in range(len(answer)):
#         if (len(answer[j]) > maximum):
#             maximum = len(answer[j])
#             sentence = answer[j]
#         print(answer[j])
#     print(maximum)
#     print(sentence.count(' '))
