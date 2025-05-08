import os.path

import pandas as pd
from docling.document_converter import DocumentConverter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from docling_core.transforms.chunker import HierarchicalChunker


def split_documents(
        source: str,
        chunk_size: int=2000,
        chunking_strategy: str="recursive",
) -> pd.DataFrame:
    file_name =f"./data/split_{source}_{chunk_size}_{chunking_strategy}.csv"
    if os.path.isfile(file_name):
        return pd.read_csv(file_name)
    converter = DocumentConverter()
    documents = converter.convert(f"../{source}.pdf")

    if chunking_strategy == "recursive":
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=int(chunk_size / 10),
            add_start_index=True,
            strip_whitespace=True,
            separators=["\n\n", "\n", ".", " ", ""],
        )
        document_text = documents.document.export_to_text()
        docs_processed = text_splitter.create_documents([document_text])
        chunks_text = [(_,doc.page_content) for _,doc in enumerate(docs_processed)]
    elif chunking_strategy == "hierarchical":
        chunks = list(HierarchicalChunker().chunk(documents.document))

        chunks_text= [(_,chunk.text) for _,chunk in enumerate(chunks)]
    chunks_df = pd.DataFrame(chunks_text)
    chunks_df.to_csv(file_name)
    return chunks_df


# test document splitter
# chunk_size = 500
# chunk_strategy = "recursive"
# chunks = split_documents(result , chunk_size, chunk_strategy)
# pass
