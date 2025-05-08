import os.path
import random
import timeit
import pandas as pd
from ollama import Message
from QAGenerater_Agent import Q_generator
from RAG.aug_generation import model, system_prompt
from RAG.embeddings import  Embedding
from RAG.main import rag_system_answer
from RAG.reranker import load_reranker
from RAG.splitter import split_documents

embedding = Embedding("Cards")
start = timeit.default_timer()
chunks = split_documents('Cards')
print("----Splitting/Loading document took :",timeit.default_timer() - start)

start = timeit.default_timer()
knowledge_retriever, docstore = embedding.load_vector_knowledge_db(chunks)
print("----Generating/Loading Vector Store took :",timeit.default_timer() - start)


start= timeit.default_timer()
questions_df = Q_generator.generate_questions(chunks,"Cards")
print("----Generarting/Loading benchmark took :",timeit.default_timer() - start)


# reranker_model_name = "BAAI/bge-reranker-base"
final_context_size = 5
# reranker = load_reranker(reranker_model_name,num_docs_final=final_context_size)

messages =[]
messages.append(Message(role='system',content=system_prompt))
for i in range(3):
    question_index = random.randint(0, len(questions_df)-1)
    question = questions_df['question'][question_index]
    true_answer = questions_df['answer'][question_index]
    print(f'the question is : {question}')
    single_question_start= timeit.default_timer()
    assistant_response,relevant_docs = rag_system_answer(embedding,
                                                         question,
                                                         model,
                                                         messages,
                                                         None,
                                                         num_retrieved_docs=5,
                                                         num_docs_final=final_context_size)
    print("-----------------------The single question time is :",timeit.default_timer() - single_question_start)
    messages.append(assistant_response.message)
    print(f'The True answer is :\n {true_answer}')
    print(f'The RAG answer is : {assistant_response.message.content}')