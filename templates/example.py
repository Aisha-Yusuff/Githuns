import requests

response = requests.get("https://opentdb.com/api.php?amount=10&type=boolean", params="parameters")

parameters = {"amount":10,
               "type": "boolean",
               }

def get_q():
    response.raise_for_status()
    data = response.json()
    questions_list = []
    for question in (data["results"]):
        question_data = {}
        question_data["text"] = (question["question"])
        question_data["answer"] = question["correct_answer"]
        questions_list.append(question_data)
    return (questions_list)