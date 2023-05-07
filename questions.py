import html

def questions_left(questions_list):
    if len(questions_list) <= 0:
        return False
    else:
        return True

def get_question(questions_list):
    question = (questions_list[0])
    questions_list.remove(question)
    return question


def check_answer(request,score, lives):
    user_answer = request.form['answer']
    correct_answer = request.form['correct_answer']
    q_result = "Incorrect"

    if user_answer == correct_answer:
        score += 1
        q_result = "Correct"
    else:
        lives -= 1
    return score, q_result, lives







