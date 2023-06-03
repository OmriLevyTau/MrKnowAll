"""
    This module provides basic document proccessing capabilities 
    used for the various tasks in MrKnowAll implementation.
    Mainly around PDF handling, and breaking documents into sentences.
"""

import base64
import io
from io import BufferedReader
from typing import List

import nltk
import PyPDF2

from app.models.documents import Document
from app.services.embeddings import MAX_SEQ

# Download the necessary data for sentence tokenization
nltk.download("punkt")

def get_documents_chunks(document: Document) -> List[str]:
    """
    Given a Document object, return a list of senenteces.
    Args:
        document (Document)
    Returns:
        List[str]: A list of senteces
    """
    doc_path = document.path
    doc_encoding = document.pdf_encoding
    
    chunks = None

    # get text chunks from encoded pdf string
    if (doc_encoding is not None) and (doc_path is None):
        chunks = get_document_chunks_helper(pdf_generator=read_pdf_from_bytes_generator, generator_input=doc_encoding)   
    # get pdf chunks from pdf file
    if (doc_path is not None) and (doc_encoding is None):
        chunks = get_document_chunks_helper(pdf_generator=read_pdf_from_path_generator, generator_input=doc_path)
    
    if chunks is not None:
        return chunks    
    
    raise ValueError("document must have path or pdf_encoding only.")    


def get_document_chunks_helper(pdf_generator, generator_input: str) -> List[str]:
    """
    given a pdf_generator, as constructed in read_pdf_from_path_generator or
    read_pdf_from_bytes_generator, and the generator matching input,
    returns a list of sentences composing the document.
    """
    pages = pdf_generator(generator_input)
    result = []
    for page in pages:
        page_sentences = nltk.sent_tokenize(page)
        for sentence in page_sentences:
            result.append(sentence)
            # if sentence.count(" ") < MAX_SEQ:
            #     result.append(sentence)
    return result


def read_pdf_from_path_generator(path: str):
    """
    creates a pdf generator from a file located
    in <path>

    Args:
        path (str): a valid path argument for a pdf file

    """
    pdf_file_descriptor = open(path, "rb")
    pdf_reader = PyPDF2.PdfReader(pdf_file_descriptor)
    return pdf_chunks_generator(pdf_reader, pdf_file_descriptor)


def read_pdf_from_bytes_generator(encoded_pdf: str):
    decoded_pdf = base64.b64decode(encoded_pdf)
    pdf_file_obj = io.BytesIO()
    # in-memory bytes buffer
    pdf_file_obj.write(decoded_pdf)

    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)

    return pdf_chunks_generator(pdf_reader, None)


def pdf_chunks_generator(pdf_reader: PyPDF2.PdfReader, pdf_file_descriptor: BufferedReader):
    """
    A generator method which yiels text of a single
    pdf page at a time.
    Args:
        pdf_reader (BufferedReader): a valid PyPDF2 PDReader object
        pdf_file_descriptor (BufferedReader): if it's a file from path, None otherwise

    Yields:
        _type_: _description_
    """
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        yield text
    
    if pdf_file_descriptor is not None:
        pdf_file_descriptor.close()


