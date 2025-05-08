evaluater_prompt = """
You are tasked with evaluating if a given context contains sufficient rich context to generate a fact-based question (factoid) and its answer. 

The evaluation should satisfy the rules below:
{rules}

Follow these steps to evaluate the context:
{guidelines}

Here are some examples (delimited by triple backticks):
```
{examples}
```
Now here is the context (delimited by triple quotes):

Context: \"\"\"{context}\"\"\" \n

Please use the JSON schema below for your output:
Output = {format}
Return Output
"""

evaluater_rules = """ - The context must present a clear subject or main idea.
-The context must include specific details, facts, or examples.
- The context must contain claims, arguments, or explanations that could be questioned.
- The context must have sufficient depth or complexity to allow meaningful questions to be generated."""

evaluater_guidelines = """1. Read the context thoroughly to understand its depth and scope.
2. Identify whether the context includes specific details or claims.
3. Assess if a meaningful question can be generated from the information provided.
4. Conclude if the context has "enough rich context" or "lacks sufficient context."""

evaluater_examples = """
    # Example 1:
    ## context: The Earth revolves around the Sun in an elliptical orbit, completing one revolution approximately every 365.25 days.
    ## reasoning": The context contains a clear subject (Earth's orbit) and provides specific details (elliptical orbit, 365.25 days).
    ## evaluation": Yes
    # Example 2:
    ## context": Apples are a type of fruit.
    ## reasoning": The context is too general and lacks specific details or claims to generate a meaningful question.
    ## evaluation": No

"""
QA_generation_prompt= """
You are tasked with generating a fact-based question based on given context and its answer. 

The evaluation should satisfy the rules below:
{rules}

Follow these steps to evaluate the context:
{guidelines}

Here are some examples (delimited by triple backticks):
```
{examples}
```
Now here is the context (delimited by triple quotes):

Context: \"\"\"{context}\"\"\" \n

Please use the JSON schema below for your output:
Output = {format}
Return Output
"""
generator_rules = """ - The context must present a clear subject or main idea.
-The context must include specific details, facts, or examples.
- The context must contain claims, arguments, or explanations that could be questioned.
- The context must have sufficient depth or complexity to allow meaningful questions to be generated."""

generator_guidelines = """1. Read the context thoroughly to understand its depth and scope.
2. Identify whether the context includes specific details or claims.
3. Assess if a meaningful question can be generated from the information provided.
4. Conclude if the context has "enough rich context" or "lacks sufficient context."""

generator_examples = """
    # Example 1:
    ## context: VISA Signature.- Travel privileges -  Lifestyle benefits  -  Protection & Assistance services - Luxury Hotel Collection
    ## question": What are privileges of VISA Signature Card?.
    ## answer": - Travel privileges -  Lifestyle benefits  -  Protection & Assistance services - Luxury Hotel Collection
    # Example 2:
    ## context": الحد الائتماني يتراوح ما بين 5,000 د.ك ولغاية 20،000 د.ك خدمة كشف الحساب الإلكتروني مجانًا
إمكانية مراقبة رصيد حساب البطاقة من خلال خدمة "التمويل أون لاين" أو من خلال تطبيق بيت التمويل الكويتي "بيتك" على الهواتف الذكية
الدفع الآمن مع الشريحة الذكية والرقم السري، وعند التسوق عبر الإنترنت مع خدمة  3D Secure.
    ## question": What is the minimum credit amount for Diamond?.
    ## answer": 5000KD

"""
generator_json_format="""
{
  "question": "generate question here",
  "answer": "generate answer here",
}
"""