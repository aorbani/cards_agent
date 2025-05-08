from tqdm import tqdm
from llm import call_model
from QAGenerater_Agent.source import chunks

def critique(outputs):

    for output in tqdm(outputs):
        evaluations = {
            "groundedness": call_model(
                question_validation_prompt_template.format(
                    task=groundedness_task,
                    evaluation_criteria=groundedness_eval,
                    evaluation_steps = groundedness_steps,
                    json_format=rating_json_format,
                    question=question_template.format(question=output["question"]),
                    context=context_template.format(context=output["context"])
                ),
            ),
            "relevance": call_model(
                QA_model,
                question_validation_prompt_template.format(
                    task=relevance_task.format(domain=topic),
                    evaluation_criteria=relevance_eval.format(domain=topic),
                    evaluation_steps = relevance_steps,
                    json_format=rating_json_format,
                    question=question_template.format(question=output["question"]),
                    context=context_template.format(context=output["context"])
                ),
            ),
            "standalone": call_model(
                QA_model,
                question_validation_prompt_template.format(
                    task=standalone_task.format(domain=topic),
                    evaluation_criteria=standalone_eval.format(domain=topic),
                    evaluation_steps = standalone_steps,
                    json_format=rating_json_format,
                    question=question_template.format(question=output["question"]),
                    context="",
                ),
            ),
        }
        try:
            # Extract evaluations
            for criterion, evaluation in evaluations.items():
                evaluation= eval(evaluation)
                score, evalu = (
                    int(evaluation["Score"]),
                    evaluation["Evaluation"],
                )
                output.update(
                    {
                        f"{criterion}_score": score,
                        f"{criterion}_eval": evalu,
                    }
                )
        except Exception as e:
            continue