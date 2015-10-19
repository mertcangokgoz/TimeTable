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

database = pymysql.connect("localhost", "root", "muratcan22", "panoDB")
conn = database.cursor()


def check_authenticate(username, password):
    return username == 'Mertcan' and password == 'admin123'


def authenticate():
    return Response(
        'Kullanici Girisi Yapmanız gerekmektedir.!', 401,
        {'WWW-Authenticate': 'Basic realm="Yetkili Kullanici Girisi"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_authenticate(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


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


@app.route('/Api')
def ApiTech():
    conn.execute("SELECT * FROM TimeTable")
    data = conn.fetchall()
    objects_list = list()
    for row in data:
        selected = collections.OrderedDict()
        selected['id'] = row[0]
        selected['Type'] = row[1]
        selected['LectureTime'] = "test"  # row[2]
        selected['LectureTeacher'] = row[3]
        selected['Lesson'] = row[4]
        selected['Place'] = row[5]
        selected['Days'] = row[6]
        objects_list.append(selected)

    j = json.dumps(objects_list)
    return j


@app.route('/Program/Add')
@requires_auth
def AreaFill():
    conn.execute("SELECT * FROM TimeTable")
    data = conn.fetchall()
    return render_template("Add.html", data=data[::-1])


@app.route("/Program/Add/Send", methods=['POST'])
@requires_auth
def AddPostTable():
    Types = request.form['Types']
    LectureTime = request.form['LectureTime']
    LectureTeacher = request.form['LectureTeacher']
    Lesson = request.form['Lesson']
    Place = request.form['Place']
    Days = request.form['Days']

    conn.execute("INSERT INTO TimeTable VALUES (null,?,?,?,?,?,?)",
                 (Types, LectureTime, LectureTeacher, Lesson, Place, Days))
    database.commit()
    return "<script>document.location ='/Program/Add'</script>"


@app.route("/Program/Delete/<id>/", methods=['GET'])
@requires_auth
def DeletePostItems(id):
    conn.execute("DELETE FROM TimeTable WHERE  id=" + id)
    database.commit()
    return "Deleted Items"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("8080"), debug=True)
