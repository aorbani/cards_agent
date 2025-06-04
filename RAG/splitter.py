import os.path
import re
from spire.pdf.common import *
from spire.pdf import *

import pandas as pd
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter
from docling_core.transforms.chunker import HierarchicalChunker
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True
pipeline_options.ocr_options.use_gpu = False  # <-- set this.
pipeline_options.do_table_structure = True
pipeline_options.table_structure_options.do_cell_matching = True

def split_documents(
        source: str,
        chunk_size: int=1500,
        chunking_strategy: str="hyprid",
) -> pd.DataFrame:
    source_filename = source.split('.')
    file_name =f"./data/split_{source_filename[0]}_{chunk_size}_{chunking_strategy}.csv"
    if os.path.isfile(file_name):
        return pd.read_csv(file_name)
    converter = DocumentConverter(format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    })
    if source.endswith(".pdf"):
        pdf = PdfDocument()
        pdf.LoadFromFile(source)
        pdf.SaveToFile(f'{source_filename[0]}.docx', FileFormat.DOCX)
        pdf.Close()
        source =f'{source_filename[0]}.docx'
    documents = converter.convert(f"{source}")
    if chunking_strategy == "recursive":
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=int(chunk_size / 10),
            add_start_index=True,
            strip_whitespace=True,
            separators=["\n\n", "\n", ".", " ","|" ""],
        )
        document_text = documents.document.export_to_text()
        docs_processed = text_splitter.create_documents([document_text])
        chunks_text = [(_,doc.page_content) for _,doc in enumerate(docs_processed)]
    elif chunking_strategy == "hierarchical":
        chunks = list(HierarchicalChunker().chunk(documents.document))
        chunks_text= [(_,chunk.text) for _,chunk in enumerate(chunks)]
    elif chunking_strategy == "hyprid":
        chunk_iter = HybridChunker().chunk(dl_doc=documents.document)
        chunks = list(chunk_iter)
        chunks_text= [(_,chunk.text) for _,chunk in enumerate(chunks)]
    chunks_df = pd.DataFrame(chunks_text)
    chunks_df = chunks_df.loc[chunks_df[1].apply(lambda x: (len(re.findall('[a-z]', x))+len(re.findall('[ا-ي]', x)))>0)]
    chunks_df.to_csv(file_name)
    return chunks_df


chunks = split_documents("cards_test.pdf")