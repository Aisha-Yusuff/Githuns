from flask import Flask, request, render_template
from data import question_data
import questions




app = Flask(__name__)
score = 0
questions_list = question_data




@app.route('/')
def quiz():

    question = (questions.get_question(questions_list))
    return render_template('quiz.html', question=question, score=score)

@app.route('/submit', methods=['POST'])
def submit():
    global score
    score = questions.check_answer(request,score)
    if questions.questions_left(questions_list):
        question = (questions.get_question(questions_list))

        return render_template('quiz.html', question=question, score=score)
    else:
        return render_template("result.html",score=score)







if __name__ == "__main__":
     app.run(debug=True)