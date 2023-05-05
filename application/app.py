from flask import Flask, render_template, request, redirect, url_for
import pymysql.cursors

app = Flask(__name__)

connection = pymysql.connect(host='database-2.cnyrbefiq91q.eu-west-2.rds.amazonaws.com',
                             # host="database-1.cnyrbefiq91q.eu-west-2.rds.amazonaws.com"
                             port=3306,
                             user="admin",
                             password="password1",
                             charset="utf8mb4",
                             cursorclass=pymysql.cursors.DictCursor)

categories = ["General Knowledge", "Music", "History", "Movies", "Science"]
currentUser = ''


# https://neil.tesaluna.com/posts/connecting-flask-to-aws-rds/

@app.route("/", methods=['GET', 'POST'])
def home():
    print('function called')
    # print(request.form['name'])
    if request.method == 'POST' and 'name' in request.form:

        # fetch the form data - the user's name
        username = request.form['name']

        # save name to the db
        try:
            with connection:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `scores`(`name`) VALUE (%s)"
                    cursor.execute(sql, username)
                connection.commit()
        except Exception as e:
            print(e)

        return redirect(url_for('menu'))
    else:
        return render_template('home.html')


@app.route("/menu", methods=['GET', 'POST'])
def menu():
    connection.ping(reconnect=True)
    #     select username from db
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT name FROM scores ORDER BY ID DESC LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            currentUser = result
    print(currentUser)
    return render_template('menu.html', categories=categories, name=currentUser)


@app.route("/start/<category>")
def start(category):
    connection.ping(reconnect=True)
    #     select username from db
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT name FROM scores ORDER BY ID DESC LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            currentUser = result

    return render_template('start.html', category=category, name=currentUser)


# run the app in debug mode
if __name__ == "__main__":
    # dbconnect()
    app.run(debug=True)
