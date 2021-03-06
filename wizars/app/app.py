from flask import Flask,render_template, request, url_for ,redirect
from models.models import Teacher, Review, Lecture
from models.database import db_session
from datetime import datetime
import random

app = Flask(__name__)

# 先生一覧画面
@app.route("/")
@app.route("/index")
@app.route("/teachers")
def teachers():
    teachers = Teacher.query.all()
    return render_template("teachers.html", teachers=teachers) 

# 先生詳細画面
@app.route("/teachers/<int:id>")
def teacher(id):
    reviews = Review.query.filter_by(teacher_id=id).all()
    score = []
    for review in reviews:
        score.append(review.rating)
    score_average = 0
    if len(score) != 0:
        score_average = round(sum(score) / len(score), 1)
    score_round = round(score_average)
    teacher = Teacher.query.filter_by(id=id).first()
    return render_template("teacher.html", teacher=teacher, reviews=reviews, score_average=score_average, score_round=score_round)

# マイページ
@app.route("/mypage")
def mypage():
    # 非効率．余裕があればリレーショナルDBへ．
    lectures = Lecture.query.all()
    lecture = Lecture.query.first()
    if lecture != None:
        teachers = []
        for lecture in lectures:
            teacher = Teacher.query.filter_by(id=lecture.teacher_id).first()
            teachers.append(teacher)
        return render_template("mypage.html", teachers=teachers)
    else:
        return render_template("mypage.html")

# ビデオチャット
@app.route("/video")
def video():
    return render_template("video.html")
    
# 先生登録
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        subject = request.form["subject"]
        price = request.form["price"]
        time = request.form["time"]
        text = request.form["text"]
        image = random.randrange(10)
        teacher = Teacher(name, subject, price, time, text, image, datetime.now())
        db_session.add(teacher)
        db_session.commit()
        return redirect(url_for("teachers"))
    else:
        return render_template("register.html")

# リクエスト
@app.route("/request", methods=["POST"])
def req():
    if request.method == "POST":
        teacher_id = request.form["teacher_id"]
        lecture = Lecture(teacher_id, datetime.now())
        db_session.add(lecture)
        db_session.commit()
    return redirect(url_for("mypage"))  

# レビュー投稿
@app.route("/review", methods=["POST"])
def review():
    if request.method == "POST":
        teacher_id = request.form["teacher_id"]
        rating = request.form["rating"]
        text = request.form["text"]
        review = Review(teacher_id, rating, text, datetime.now())
        db_session.add(review)
        db_session.commit()
    return redirect(url_for("mypage"))

# データリセット
@app.route("/reset", methods=["POST"])
def reset():
    if request.method == "POST":
        reset = request.form["reset"]
        if reset == "reset":
            db_session.query(Teacher).delete()
            db_session.query(Lecture).delete()
            db_session.query(Review).delete()
            db_session.commit()
    return redirect(url_for("teachers"))

if __name__ == "__main__":
    app.run(debug=True)