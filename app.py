from flask import Flask, render_template, redirect, url_for
import pymysql.cursors


app = Flask(__name__)

connection = pymysql.connect(host="localhost",
                             port=3306,
                             user="root",
                             password= 'password' ,
                             database="githuns",
                             charset="utf8mb4",
                             cursorclass=pymysql.cursors.DictCursor)
# class ScoreKeeper:
#     def __init__(self):
#         self.score = 0
#
#     def add_points(self, points):
#         self.score += points

@app.route('/score')
# need to add parameters, so that it looks for the right variables
def display_scores():
    # render user list
    score = 0
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
            print(leaderboard)
    return render_template('leaderboard.html', leaderboard=leaderboard)


if __name__ == '__main__':
    app.run()
