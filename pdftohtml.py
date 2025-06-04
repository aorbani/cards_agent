from pdf2docx import parse

pdf_file = "RAG/cards_test.pdf"
docx_file = "RAG/cards_test.docx"

print(parse(pdf_file, docx_file))