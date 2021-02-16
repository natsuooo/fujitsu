from flask import Flask,render_template, request, url_for ,redirect
from models.models import Teacher, Review, Lecture
from models.database import db_session
from datetime import datetime
import random

app = Flask(__name__)


@app.route("/")
@app.route("/index")
# @app.route("/teachers")
def index():
    teachers = Teacher.query.all()
    return render_template("teachers.html", teachers=teachers)

@app.route("/request", methods=["POST"])
def req():
    if request.method == "POST":
        teacher_id = request.form["teacher_id"]
        lecture = Lecture(teacher_id, datetime.now())
        db_session.add(lecture)
        db_session.commit()
    return redirect(url_for("mypage"))

@app.route("/mypage")
def mypage():
    # if request.method == "POST":
    #     teacher_id = request.form["teacher_id"]
    #     lecture = Lecture(teacher_id, datetime.now())
    #     db_session.add(lecture)
    #     db_session.commit()
    # elif request.method == "POST":

    # 非効率．余裕があればリレーショナルDBへ．
    lectures = Lecture.query.all()
    teachers = []
    for lecture in lectures:
        teacher = Teacher.query.filter_by(id=lecture.teacher_id).first()
        teachers.append(teacher)
    return render_template("mypage.html", teachers=teachers)
    

@app.route("/teachers/<int:id>", methods=["GET", "POST"])
def teacher(id):
    # if request.method == "POST":
    #     teacher_id = request.form["teacher_id"]
    #     lecture = Lecture(teacher_id, datetime.now())
    #     db_session.add(lecture)
    #     db_session.commit()

    teacher = Teacher.query.filter_by(id=id).first()
    return render_template("teacher.html", teacher=teacher)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/teachers", methods=["GET", "POST"])
def teachers():
    if request.method == "POST":
        name = request.form["name"]
        subject = request.form["subject"]
        price = request.form["price"]
        time = request.form["time"]
        text = request.form["text"]
        image = random.randrange(5)
        teacher = Teacher(name, subject, price, time, text, image, datetime.now())
        db_session.add(teacher)
        db_session.commit()

    teachers = Teacher.query.all()
    return render_template("teachers.html", teachers=teachers)    



if __name__ == "__main__":
    app.run(debug=True)