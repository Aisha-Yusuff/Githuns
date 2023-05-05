from flask import Flask, request, render_template
import questions_api
from questions import get_question, check_answer,  questions_left
import csv



app = Flask(__name__, static_url_path='/static')
score = 0
questions_list = []
lives = 5



@app.route('/', methods=['POST'])
def choice():
    global questions_list
    if request.method == 'POST':
        if request.form["difficulty"]:
            difficulty = request.form["difficulty"]
            category = request.form["category"]
            questions_list = questions_api.get_questions(difficulty, category)
    question = (get_question(questions_list))
    return render_template('quiz.html', question=question, score=score, lives=lives)

@app.route('/submit', methods=['POST'])
def submit():
    global score
    global questions_list
    global lives

    score, q_result, lives = check_answer(request,score, lives)
    if lives <= 0:
        return render_template("result.html", score=score)
    if questions_left(questions_list) == True:
        question = (get_question(questions_list))
        return render_template('quiz.html', question=question, score=score, result=q_result, lives=lives)
    else:
        highest_score = 0
        with open("score.csv", mode="r", newline='') as data:
            writer = csv.reader(data)
            for row in writer:
                row_score = int(row[0])
                if row_score > highest_score:
                    highest_score = row_score
        if score > highest_score:
            with open("score.csv", mode="w", newline='') as data:
                writer = csv.writer(data)
                writer.writerow(f"{score}")
    return render_template("result.html", score=score)



@app.route("/choices", methods=["GET","POST"])
def choices():
    return render_template("choices.html")


@app.route('/bug_report', methods=["GET"])
def bug_report():
    return render_template('report_bug.html')

@app.route('/thank_you', methods=["POST","GET"])
def bug_submit():
    return render_template("thank_you.html")











if __name__ == "__main__":
     app.run(debug=True)