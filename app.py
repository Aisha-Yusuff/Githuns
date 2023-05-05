from flask import Flask, render_template, request, redirect, url_for
import pymysql.cursors
from cryptography.fernet import Fernet

# encrypt database password with cryptography to connect with aws ec2 mysql
key = Fernet.generate_key()
fernet = Fernet(key)
password = 'Password1!'
password_bytes = password.encode()
encrypted_password = fernet.encrypt(password_bytes)


app = Flask(__name__)

connection = pymysql.connect(host='localhost',
                             # host='52.56.52.147',
                             port=3306,
                             database="githuns",
                             user="root",
                             password='password',
                             # password=password_bytes,
                             charset="utf8mb4",
                             cursorclass=pymysql.cursors.DictCursor)

categories = ["General Knowledge", "Music", "History", "Movies", "Science"]
currentUser = ''

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
    app.run(debug=True)