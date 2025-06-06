import json
import random

QUESTION_FILES = {
    "AWS": "database/questions/aws_questions.json",
    "DevOps": "database/questions/devops_questions.json"
}

def get_random_questions(tool: str):
    tool = tool.capitalize()
    try:
        with open(QUESTION_FILES[tool], "r") as f:
            data = json.load(f)
        return random.sample(data, 10)
    except (KeyError, FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Error loading questions for tool '{tool}': {e}")

def evaluate_answers(form_data):
    tool = form_data["tool"].capitalize()
    try:
        with open(QUESTION_FILES[tool], "r") as f:
            questions = json.load(f)
            correct_answers = {str(q["id"]): q["answer"] for q in questions}
    except (KeyError, FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Error loading answers for tool '{tool}': {e}")

    user_answers = {k: v for k, v in form_data.items() if k.startswith("q")}
    score = sum(1 for qid, ans in user_answers.items() if ans == correct_answers.get(qid))
    return score
