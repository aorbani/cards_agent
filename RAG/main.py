import timeit
from typing import Optional

from ollama import chat,Message
from aug_generation import build_context_from_list, LLM_PROMPT_TEMPLATE, USER_QUESTION_TEMPLATE
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from embeddings import  Embedding


def rag_system_answer(
        embedding:Embedding, question: str, model_name:str, messages:[],
        reranker: Optional[HuggingFaceCrossEncoder] = None, num_retrieved_docs: int = 6,
        num_docs_final: int = 5,):
    single_question_start = timeit.default_timer()
    relevant_docs = embedding.similarity_search(question, num_retrieved_docs)
    print("-----------------------The fetch similar time is :", timeit.default_timer() - single_question_start)
    if reranker:
        relevant_docs = reranker.compress_documents(relevant_docs, question)
    relevant_docs = relevant_docs[:num_docs_final]
    context = build_context_from_list(relevant_docs)
    messages.append(Message(role='assistant', content=LLM_PROMPT_TEMPLATE.format(context=context)))
    messages.append(Message(role='user', content=USER_QUESTION_TEMPLATE.format(question=question)))
    llm_generating_response = timeit.default_timer()
    final_response= chat(model=model_name,messages=messages,keep_alive=10)
    print("-----------------------The llm generating response is :", timeit.default_timer() - llm_generating_response)
    return final_response, relevant_docs