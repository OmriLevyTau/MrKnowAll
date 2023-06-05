"""
    This module provides basic document proccessing capabilities 
    used for the various tasks in MrKnowAll implementation.
    Mainly around PDF handling, and breaking documents into sentences.
"""

import base64
import io
import re
from io import BufferedReader
from typing import List

import nltk
import PyPDF2

from app.models.documents import Document

# Download the necessary data for sentence tokenization
nltk.download("punkt")


alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov|edu|me)"
digits = "([0-9])"
multiple_dots = r'\.{2,}'

def split_into_sentences_by_hand(text: str) -> list[str]:
    """
    Split the text into sentences.

    If the text contains substrings "<prd>" or "<stop>", they would lead 
    to incorrect splitting because they are used as markers for splitting.

    :param text: text to be split into sentences
    :type text: str

    :return: list of sentences
    :rtype: list[str]
    """
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
    if "Ph.D" in text: 
        text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text:
        text = text.replace(".”","”.")
    if "\"" in text:
        text = text.replace(".\"","\".")
    if "!" in text:
        text = text.replace("!\"","\"!")
    if "?" in text:
        text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences]
    if sentences and not sentences[-1]:
        sentences = sentences[:-1]
    return sentences

def split_into_sentences_by_nltk(text: str) -> list[str]:
    return nltk.sent_tokenize(text)

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
        page_sentences = split_into_sentences_by_nltk(page)
        for sentence in page_sentences:
            result.append(sentence)

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


