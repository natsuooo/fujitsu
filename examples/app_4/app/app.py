from flask import Flask,render_template, request
from models.models import User

app = Flask(__name__)


@app.route("/")
@app.route("/index")
@app.route("/teachers")
def teachers():
    users = User.query.all()
    return render_template("teachers.html", users=users)

@app.route("/mypage")
def mypage():
    return render_template("mypage.html")

@app.route("/teachers/<int:id>")
def teacher(id):
    user = User.query.filter_by(id=id).first()
    return render_template("teacher.html", user=user)


if __name__ == "__main__":
    app.run(debug=True)