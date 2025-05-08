import numpy as np
import pandas as pd
import os
import faiss
from sentence_transformers import SentenceTransformer
from faiss import write_index, read_index, IndexFlatL2
sentence_transformer_model = SentenceTransformer(fr"\\172.16.123.109\ai\all-MiniLM-L6-v2")
class Embedding:
    def __init__(self,doc_name):
        self.doc_name=doc_name
    def load_vector_knowledge_db(self,chunks:pd.DataFrame|None) -> (IndexFlatL2,pd.DataFrame):
        index_path = f"./data/index_{self.doc_name}.index"
        csv_path = f"./data/chunks_{self.doc_name}.csv"
        if os.path.isfile(index_path) and os.path.isfile(csv_path):
            print("Loading from local...")
            self.index = read_index(index_path)
            self.chunks = pd.read_csv(csv_path)
            return self.index,self.chunks

        else:
            print("Index not found, generating it...")
            embeddings = sentence_transformer_model.encode(chunks[1].tolist())
            index = faiss.IndexFlatL2(embeddings.shape[1])
            index.add(embeddings)
            write_index(index, index_path)
            chunks.to_csv(csv_path)
            self.index=index
            self.chunks=chunks
            return self.index,self.chunks

    # test retrieval
    def similarity_search( self,question ,
                          k,
                          fetch_k: int = 20):
        embedding = sentence_transformer_model.encode([question])
        vector= np.array(embedding, dtype=np.float32)
        # faiss.normalize_L2(vector)
        scores, indices = self.index.search(vector,fetch_k)
        docs = []
        for j, i in enumerate(indices[0]):
            if i == -1:
                continue
            doc = self.chunks.iloc[i,2]
            docs.append((doc, scores[0][j]))
        return docs[:k]


