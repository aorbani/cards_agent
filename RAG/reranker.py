from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

def load_reranker(model_name: str ="BAAI/bge-reranker-base",num_docs_final: int =7):
    ranker_model = HuggingFaceCrossEncoder(model_name=model_name)
    compressor = CrossEncoderReranker(model=ranker_model, top_n=num_docs_final)
    return compressor