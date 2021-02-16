from flask import Flask,render_template, request
from models.models import Teacher
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

@app.route("/mypage/<int:id>")
def mypage(id):
    teacher = Teacher.query.filter_by(id=id).first()
    return render_template("mypage.html", teacher=teacher)
    

@app.route("/teachers/<int:id>")
def teacher(id):
    teacher = Teacher.query.filter_by(id=id).first()
    return render_template("teacher.html", teacher=teacher)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/teachers", methods=["GET", "POST"])
def teachers():
    teachers = Teacher.query.all()
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        time = request.form["time"]
        text = request.form["text"]
        image = random.randrange(5)
        teacher = Teacher(name, price, time, text, image, datetime.now())
        db_session.add(teacher)
        db_session.commit()

    teachers = Teacher.query.all()
    return render_template("teachers.html", teachers=teachers)    



if __name__ == "__main__":
    app.run(debug=True)