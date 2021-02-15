#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask,render_template

#Flaskオブジェクトの生成
app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html')


@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/teachers")
def teachers():
    return render_template("teachers.html")

@app.route("/mypage")
def mypage():
    return render_template("mypage.html")


#おまじない
if __name__ == "__main__":
    app.run(debug=True)