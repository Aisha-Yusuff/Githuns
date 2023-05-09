from flask import Flask, render_template, request, redirect, url_for
import pymysql.cursors
from cryptography.fernet import Fernet
import questions_api
from questions import get_question, check_answer, questions_left
import csv
import smtplib

# encrypt database password with cryptography to connect with aws ec2 mysql
key = Fernet.generate_key()
fernet = Fernet(key)
password = 'Password1!'
password_bytes = password.encode()
encrypted_password = fernet.encrypt(password_bytes)

app = Flask(__name__, static_url_path='/static')
score = 0
questions_list = []
lives = 5

# Connected to the ec2 database:
# dominique was here
connection = pymysql.connect(
                             host='52.56.52.147',
                             port=3306,
                             database="githuns",
                             user="root",
                             password=password_bytes,
                             charset="utf8mb4",
                             cursorclass=pymysql.cursors.DictCursor)

currentUser = ''


@app.route("/", methods=['GET', 'POST'])
def home():
    global lives
    global score

    lives = 5
    if request.method == 'POST' and 'name' in request.form:

        # fetch the form data - the user's name
        username = request.form['name']

        # save name to the db
        try:
            # Open the connection
            connection.ping(reconnect=True)
            with connection:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `scores`(`name`) VALUE (%s)"
                    cursor.execute(sql, username)
                connection.commit()
        except Exception as e:
            print(e)
        score = 0
        return redirect(url_for('choices'))
    else:
        score = 0
        return render_template('home.html')


@app.route("/choices", methods=["GET", "POST"])
def choices():
    connection.ping(reconnect=True)
    #     select username from db
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT name FROM scores ORDER BY ID DESC LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            name = result
    print(name)
    return render_template("choices.html", name=name)


@app.route('/quiz', methods=['POST'])
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

    # Open the connection
    connection.ping(reconnect=True)
    with connection:
        with connection.cursor() as cursor:
            # Fetch the name from the database
            sql = "SELECT name FROM scores ORDER BY ID DESC LIMIT 1"
            cursor.execute(sql)
            name = cursor.fetchone()
            print(name)

    score, q_result, lives = check_answer(request, score, lives)
    if lives <= 0:
        try:
            # Update the score in the database
            connection.ping(reconnect=True)
            with connection:
                with connection.cursor() as cursor:
                    sql = "UPDATE `scores` SET `score` = %s WHERE `name` = %s"
                    cursor.execute(sql, (score, name['name']))
                connection.commit()
                print("Score updated successfully.")
        except pymysql.Error as e:
            print(f"Error updating score: {e}")

        return render_template("scorepage.html", score=score, name=name)

    if questions_left(questions_list):
        question = get_question(questions_list)
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
                writer.writerow([score])

    return render_template("scorepage.html", score=score, name=name)


@app.route('/score')
def display_scores():
    # render user list
    connection.ping(reconnect=True)
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT name FROM scores ORDER BY ID DESC LIMIT 1"
            cursor.execute(sql)
            name = cursor.fetchone()
    return render_template('scorepage.html', name=name, score=score)


@app.route('/return_home', methods=['POST'])
def return_home():
    return redirect(url_for('home'))


@app.route('/leaderboard', methods=['POST'])
def leaderboard():
    connection.ping(reconnect=True)
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT name, score FROM scores ORDER BY score DESC;"
            cursor.execute(sql)
            leaderboard = cursor.fetchall()
    return render_template('leaderboard.html', leaderboard=leaderboard)


@app.route('/bug_report', methods=["GET"])
def bug_report():
    return render_template('report_bug.html')


@app.route('/thank_you', methods=["POST", "GET"])
def bug_submit():
    send_mail = questions_api.send_mail(request, smtplib)
    return render_template("thank_you.html")


if __name__ == "__main__":
    app.run(debug=True)
