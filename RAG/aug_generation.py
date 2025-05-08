
from typing import List


system_prompt ="""You are an expert assistant in KFH Bank Cards. Use the provided set of extracted documents as context to answer the user's question accurately, clearly, and concisely. 
If the context does not have enough information, indicate that you do not have sufficient information and avoid making up answers.
do not use phrases like based on the text,According to Document, or according to the text, etc. Don't share context to user.
"""


model ='llama3.2'
LLM_PROMPT_TEMPLATE = """
Here the collected contexts and the user question:

### Context:
{context}
"""
USER_QUESTION_TEMPLATE ="""
### Question:
{question}

"""
def build_context_from_list(retrieved_docs) -> str:

    context = "\nExtracted documents:\n"
    context += "".join(
        [f"\n\n <<<Document {str(i)}>>>:::\n\n" + doc[0] for i, doc in enumerate(retrieved_docs)]
    )
    return context