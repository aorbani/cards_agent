from typing import Optional

from ollama import chat,Message
from aug_generation import build_context_from_list, LLM_PROMPT_TEMPLATE, USER_QUESTION_TEMPLATE
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from embeddings import  Embedding


def rag_system_answer(
        embedding:Embedding,
    question: str,
    model_name:str,
    messages:[],
    reranker: Optional[HuggingFaceCrossEncoder] = None,
    num_retrieved_docs: int = 6,
    num_docs_final: int = 5,):
    relevant_docs = embedding.similarity_search(question, num_retrieved_docs)
    if reranker:
        relevant_docs = reranker.compress_documents(relevant_docs, question)
    relevant_docs = relevant_docs[:num_docs_final]
    context = build_context_from_list(relevant_docs)
    messages.append(Message(role='assistant', content=LLM_PROMPT_TEMPLATE.format(context=context)))
    messages.append(Message(role='user', content=USER_QUESTION_TEMPLATE.format(question=question)))
    final_response= chat(model=model_name,messages=messages)
    return final_response, relevant_docs