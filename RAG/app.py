import os.path
import random
import timeit
import pandas as pd
import uvicorn
from fastapi import FastAPI, UploadFile, File
from ollama import Message
from QAGenerater_Agent import Q_generator
from RAG.aug_generation import model, system_prompt
from RAG.embeddings import  Embedding
from RAG.main import rag_system_answer
from RAG.reranker import load_reranker
from RAG.splitter import split_documents
app = FastAPI()
messages =[]
def internal(file_name):
    embedding = Embedding(file_name)
    start = timeit.default_timer()
    chunks = split_documents(file_name,chunk_size=2000,chunking_strategy="hierarchical")
    print("----Splitting/Loading document took :", timeit.default_timer() - start)
    start = timeit.default_timer()
    knowledge_retriever, docstore = embedding.load_vector_knowledge_db(chunks)
    print("----Generating/Loading Vector Store took :", timeit.default_timer() - start)

    # start= timeit.default_timer()
    # questions_df = Q_generator.generate_questions(chunks,file_name)
    # print("----Generarting/Loading benchmark took :",timeit.default_timer() - start)
    return embedding
@app.post("/create_rag_system")
def create_rag_system(file:UploadFile = File(...)):
    contents = file.file.read()
    with open(f"../{file.filename}", 'wb') as f:
        f.write(contents)
    file_name = file.filename.split('.')[0]
    internal(file_name)
    return True
@app.post("/chat")
def chat(question:str,file_name:str):
    embedding = internal(file_name)
    # reranker_model_name = "BAAI/bge-reranker-base"
    final_context_size = 5
    # reranker = load_reranker(reranker_model_name,num_docs_final=final_context_size)
    if len(messages)==0:
        messages.append(Message(role='system',content=system_prompt))
    single_question_start = timeit.default_timer()
    assistant_response, relevant_docs = rag_system_answer(embedding,
                                                          question,
                                                          model,
                                                          messages,
                                                          None,
                                                          num_retrieved_docs=5,
                                                          num_docs_final=final_context_size)
    print("-----------------------The single question time is :", timeit.default_timer() - single_question_start)
    messages.append(assistant_response.message)
    return messages

