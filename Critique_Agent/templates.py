question_validation_prompt_template = """
{task}
{evaluation_criteria}

Follow these steps to generate your evaluation:
{evaluation_steps}

Please respond using the following JSON schema:

Answer = {json_format}

You MUST provide values for 'Evaluation:' and 'Score' in your answer.

{question}
{context}

Answer: """
rating_json_format = """
{
    "Evaluation":"your rationale for the rating, as a text",
    "Score":"your rating, as a number between 1 and 5",
}
"""
question_template = """Now here are the question (delimited by triple backticks)
Question: ```{question}```
"""

context_template = """here are the context (delimited by triple quotes).
Context: \"\"\"{context}\"\"\"\n
"""
groundedness_task = """You will be given a context and a question.
Your task is to evaluate the question based on the given context and provide a score between 1 and 5 according to the following criteria:"""

groundedness_eval = """- Score 1: The context does not provide sufficient information to answer the question in any way.
- Score 2 or 3: The context provides some relevant information, but the question remains partially answerable, or is unclear/ambiguous.
- Score 4: The context offers sufficient information to answer the question, but some minor details are missing or unclear.
- Score 5: The context provides all necessary information to answer the question clearly and without ambiguity."""

groundedness_steps = """- Read the context and question carefully.
- Analyse and evaluate the question based on the provided evaluation criteria.
- Provide a scaled score between 1 and 5 that reflect your evaluation."""

topic = "Climat Change"
relevance_task = """You will be provided with a question that may or may not relate to the {domain} domain.
Your task is to evaluate its usefulness to users seeking information in the {domain} domain and assign a score between 1 and 5 based on the following criteria:"""

relevance_eval = """- Score 1: The question is unrelated to the {domain} domain.
- Score 2 or 3: The question touches on {domain} but leans more towards another domain and is not particularly useful or relevant for {domain}-specific needs.
- Score 4: The question is related to the {domain} domain but lacks direct usefulness or relevance for users looking for valuable information in this domain.
- Score 5: The question is clearly related to the {domain} domain, makes sense, and is likely to be useful to users seeking information within this domain."""

relevance_steps = """- Read the question carefully.
- Analyse and evaluate the question based on the provided evaluation criteria.
- Provide a scaled score between 1 and 5 that reflect your evaluation."""

standalone_task = """You will be given a question.
Your task is to evaluate how context-independant this question is. You need to assess how self-contained and understandable a question is without relying on external context.
The score reflects whether the question makes sense on its own. Questions referring to a specific, unstated context, such as "in the document" or "in the context," should receive a lower score. 
Technical terms or acronyms related to {domain} can still qualify for a high score if they are clear to someone with standard domain knowledge and documentation access.
Please provide a score between 1 and 5 based on the following criteria:"""

standalone_eval = """- Score 1: The question is highly dependent on external context and cannot be understood without additional information.
- Score 2: The question provides some clarity but still requires significant additional context to make sense.
- Score 3: The question can mostly be understood but may depend slightly on an external context for complete clarity.
- Score 4: The question is nearly self-contained, with only minor reliance on external context.
- Score 5: The question is entirely self-contained and makes complete sense on its own, without any reliance on external context."""

standalone_steps = """- Read the question carefully.
- Analyse and evaluate the question based on the provided evaluation criteria.
- Provide a scaled score between 1 and 5 that reflect your evaluation."""