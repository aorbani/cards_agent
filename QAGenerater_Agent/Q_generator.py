import json
import os
from typing import List

import pandas as pd
from tqdm import tqdm
from QAGenerater_Agent.llm import call_model
from QAGenerater_Agent.prompt import QA_generation_prompt,generator_rules,generator_guidelines,generator_examples,generator_json_format

def generate_questions(source:pd.DataFrame ,output_file:str):
    if os.path.isfile(f"{output_file}.csv"):
        return pd.read_csv(f"{output_file}.csv")
    print(f"Generating QA couples...")
    outputs = []
    for sampled_context in tqdm(source[1]):
        # Generate QA couple
        output_QA_couple = call_model(QA_generation_prompt.format(rules=generator_rules,
                                                                  guidelines=generator_guidelines,
                                                                  examples = generator_examples,
                                                                  context=sampled_context,
                                                                  format=generator_json_format))
        try:
            output_QA_couple = json.loads(output_QA_couple)
            question = output_QA_couple['question']
            answer = output_QA_couple['answer']
            # assert len(answer) < 300, "Answer is too long"
            outputs.append(
                {
                    "context": sampled_context,
                    "question": question,
                    "answer": answer,
                }
            )
        except:
            continue


    question_answers = pd.DataFrame(outputs)
    question_answers.to_csv(f"{output_file}.csv")
    print(f"Successfully Generated QA benchmark")
    return question_answers