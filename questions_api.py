import requests

import html
import json


def get_questions(difficulty,category,):
    response = requests.get(
        f'https://opentdb.com/api.php?amount=10&category={category}&difficulty={difficulty}&type=multiple')
    data = response.json()
    questions_list = []
    for question in data["results"]:
        if question["type"] == "multiple":
            question_data = {}
            question_data["text"] = html.unescape(question["question"])
            question_data["answer"] = html.unescape(question["correct_answer"])
            answer_list = html.unescape(question["incorrect_answers"])
            answer_list.append(question["correct_answer"])
            answer_list.sort()
            question_data["answers"] = answer_list
            questions_list.append(question_data)
    return(questions_list)


def send_mail(request,smtplib):
    message = request.form["message"]
    title = request.form["title"]
    email = "dcd5497@gmail.com"
    password = "wtoddaqzhqrnxrov"
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=email, password=password)
    connection.sendmail(from_addr=email, to_addrs=email, msg=f"subject:{title}\n\n{message}")
    connection.close()
