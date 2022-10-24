# /usr/bin/python3.4
__author__ = 'Mertcan Gokgoz'

from flask import Flask, send_from_directory
from flask import Response
from flask import render_template
from flask import request
from functools import wraps
import pymysql
import json
import collections

database = pymysql.connect("localhost", "username", "password", "databasename")
conn = database.cursor()


def check_authenticate(username, password):
    return username == 'Mertcan' and password == 'admin123'


def authenticate():
    return Response(
        'Authorized User Login Area!', 401,
        {'WWW-Authenticate': 'Basic realm="User Login"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_authenticate(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


# define static files path
app = Flask(__name__, static_url_path='/static')


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/Program')
def show_timetable():
    conn.execute("SELECT * FROM TimeTable")
    data = conn.fetchall()
    return render_template("timetable.html", data=data[::-1])


# MySQL datas convert to JSON format
@app.route('/Api')
def ApiTech():
    conn.execute("SELECT * FROM TimeTable")
    data = conn.fetchall()
    objects_list = []
    for row in data:
        selected = collections.OrderedDict()
        selected['id'] = row[0]
        selected['Type'] = row[1]
        selected['LectureTime'] = row[2]
        selected['LectureTeacher'] = row[3]
        selected['Lesson'] = row[4]
        selected['Place'] = row[5]
        selected['Days'] = row[6]
        objects_list.append(selected)

    return json.dumps(objects_list)


@app.route('/Program/Add')
@requires_auth
def AreaFill():
    conn.execute("SELECT * FROM TimeTable")
    data = conn.fetchall()
    return render_template("Add.html", data=data[::-1])


# data post method
@app.route("/Program/Add/Send", methods=['POST'])
@requires_auth
def AddPostTable():
    Types = str(request.form['type'])
    LectureTime = str(request.form['lecturetime'])
    LectureTeacher = str(request.form['lectureteacher'])
    Lesson = str(request.form['lesson'])
    Place = str(request.form['place'])
    Days = str(request.form['days'])

    conn.execute('''INSERT INTO TimeTable VALUES (NULL,%s,%s,%s,%s,%s,%s)''',
                 [Types, LectureTime, LectureTeacher, Lesson, Place, Days])
    database.commit()
    return "<script>document.location ='/Program/Add'</script>"


# data delete method
@app.route("/Program/Delete/<id>/", methods=['GET'])
@requires_auth
def DeletePostItems(id):
    conn.execute(f"DELETE FROM TimeTable WHERE  id={id}")
    database.commit()
    return "Deleted Item"


if __name__ == '__main__':
    # define flask run adress and port
    app.run(host="0.0.0.0", port=int("8080"), debug=False)
