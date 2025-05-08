
from ollama import  pull, generate


pull('llama3.2')
# generation_config = {"response_mime_type":"application/json"})

def call_model(prompt:str):
    output=generate(model='llama3.2', prompt=prompt,format={
    "type": "object",
    "properties": {
      "question": {
        "type": "string"
      }, "answer": {
            "type": "string"
        },
    },
    "required": [
      "question",
      "answer"
    ]
  })
    return output.response

