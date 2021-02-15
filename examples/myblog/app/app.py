from flask import Flask,render_template,session,request,redirect,url_for
from models.database import Base,db_session
from models.models import BlogContent,Users

app = Flask(__name__)

@app.route("/")
def index():
    # if ("name" in session):
    #     if (not session["name"] == None):
    #         app.add_template_global(name="status",f="login")
    # else:
    app.add_template_global(name="status",f="n")
    posts = db_session.query(BlogContent).order_by(BlogContent.id.desc())
    return render_template("index.html",posts=posts)

# @app.route('/template')
# def template():
#     return render_template('index.html', message='intro template')


app.secret_key = "UfriMzp7nEQcKSf"

@app.route("/login")
def login():
    if ("name" in session):
        if (not session["name"] == None):
            return redirect(url_for("index"))
    else:
        app.add_template_global(name="status",f="n")
        return render_template("login.html")

@app.route("/login",methods=["post"])
def login_check():
    name = request.form["name"]
    password = request.form["password"]
    user = db_session.query(Users).filter_by(name = name,password = password).first()
    if user:
        session["name"] = name
        return redirect(url_for("index"))
    else:
        return render_template("login.html",message="NameまたはPasswordが違います")

@app.route("/logout")
def logout():
    session.pop("name",None)
    return redirect(url_for("index"))

@app.route("/add")
def add():
    if ("name" in session):
        if (not session["name"] == None):
            app.add_template_global(name="status",f="login")
            return render_template("add_post.html")
    else:
        return redirect(url_for("login"))

@app.route("/add",methods=["post"])
def add_post():
    if ("name" in session):
        if (not session["name"] == None):
            app.add_template_global(name="status",f="login")
            if (request.form["title"]) and (request.form["body"]):
                title = request.form["title"]
                body = request.form["body"]
                check_title = db_session.query(BlogContent).filter_by(title = title).first()
                if check_title:
                    message = title + "は既に使われています"
                    return render_template("add_post.html",message=message,title=title,body=body)
                else:
                    post_data = BlogContent(title,body)
                    db_session.add(post_data)
                    db_session.commit()
                    return redirect(url_for("post",title=title))
            else:
                if request.form["title"]:
                    return render_template("add_post.html",title=request.form["title"])
                if request.form["body"]:
                    return render_template("add_post.html",body=request.form["body"])
                if (not request.form["title"]) and (not request.form["body"]):
                    return redirect(url_for("add"))
    else:
        return redirect(url_for("login"))

@app.route("/post/<title>")
def post(title):
    if ("name" in session):
        if (not session["name"] == None):
            app.add_template_global(name="status",f="login")
    else:
        app.add_template_global(name="status",f="n")
    post_data = db_session.query(BlogContent).filter_by(title=title).first()
    if post_data:
        return render_template("post.html",post=post_data)
    else:
        return render_template("notfound.html")

@app.route("/post")
def post_none():
    return redirect(url_for("index"))

@app.route("/edit/<title>")
def edit(title):
    if ("name" in session):
        if (not session["name"] == None):
            app.add_template_global(name="status",f="login")
            post_check = db_session.query(BlogContent).filter_by(title = title).first()
            if post_check:
                return render_template("edit_post.html",post=post_check)
            else:
                return redirect(url_for("index"))
    else:
        return redirect(url_for("login"))


@app.route("/edit/<title>",methods=["post"])
def edit_update(title):
    if ("name" in session):
        if (not session["name"] == None):
            app.add_template_global(name="status",f="login")
            post = db_session.query(BlogContent).filter_by(title = title).first()
            if post:
                if (request.form["title"]) and (request.form["body"]):
                    new_title = request.form["title"]
                    new_body = request.form["body"]
                    if (title == new_title):
                        post.body = new_body
                        db_session.commit()
                        return redirect(url_for("post",title=title))
                    else:
                        post_check = db_session.query(BlogContent).filter_by(title = new_title).first()
                        if post_check:
                            message = new_title+"は既に使われています"
                            return render_template("edit_post.html",post=post_check,message=message)
                        else:
                            post.title = new_title
                            post.body = new_body
                            db_session.commit()
                            return redirect(url_for("post",title=new_title))
                else:
                    return redirect(url_for("edit",title=title))
            else:
                return redirect(url_for("index"))
    else:
        return redirect(url_for("login"))


@app.route("/delete/<title>")
def delete(title):
    if ("name" in session):
        if (not session["name"] == None):
            app.add_template_global(name="status",f="login")
            post_check = db_session.query(BlogContent).filter_by(title = title).first()
            if post_check:
                post = db_session.query(BlogContent).filter_by(title = title).first()
                db_session.delete(post)
                db_session.commit()
                return redirect(url_for("index"))
            else:
                return redirect(url_for("index"))
    else:
        return redirect(url_for("login"))

blog_name = "MasuBlog"

app.add_template_global(name="blog_name",f=blog_name)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("notfound.html"), 404

if __name__ == '__main__':
    app.run(debug=True)

    
