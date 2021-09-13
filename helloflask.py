from os import name
import re
from flask import Flask
from flask import url_for
from flask import request
from flask import render_template
from flask import make_response
from flask import redirect
from flask import jsonify
from flask import session
from flask import flash
from markupsafe import escape
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# @app.route("/<name>")
# def hello(name):
#     return f"Hello, {escape(name)}"

import uuid

my_uuid = uuid.uuid4()

@app.route("/user/<string:name>/<int:age>/<float:salary>/")
def user(name,age,salary):
    return f"Name : {escape(name.title())}  Age : {escape(age)} Salary : {escape(salary)}"

with app.test_request_context():
    # print(url_for('user',age=10,name="prabhat sharma",salary=12.2))
    print(url_for('static',filename="style.css"))


@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == "POST":
        return "POST request recieved"
    else:
        return "GET request recieved"

@app.route("/html/")
@app.route("/html/<name>")
def html_render(name=None):
    return render_template("hello.html",name = name)


@app.route("/first_response",methods = ['GET','POST'])
def first_response():
    csrf = request.cookies.get("csrftoken")
    print(csrf,request.cookies.get("sessionid"))
    resp = make_response(render_template("hello.html",name="chidori"))
    resp.set_cookie("username","itachi")
    resp.headers["abcd"] = "hello"
    return resp


# http://127.0.0.1:5000/first_form?extra=100

@app.route('/first_form',methods = ["POST"])
def first_form():
    if request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]
            return f"{password} {username}  {request.args.get('extra','')}"
        except KeyError:
            return "KeyError"


@app.route("/file_upload",methods = ["POST"])
def file_upload():
    if request.method == "POST":
        print(request.files)
        # f = request.files['the_file']
        # f.save(f'/var/www/uploads/{secure_filename(f.filename)}')
        return f"success"


@app.route('/redirect')
def first_redirect():
    return redirect(url_for('login'))


# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template("page_not_found_404.html"), 404

@app.route("/json_response")
def json_response():
    return {
        "a":"1232",
        "b":"3421"
    }

@app.route("/tuple_response")
def tuple_response():
    return ({"a":"c"},200)


@app.route("/session",methods = ["GET","POST"])
def first_session():
    if 'username' in session:
        return f"session {session['username']}"


@app.route("/router",methods = ["GET","POST"])
def first_router():
    if request.method == "POST":
        session["username"] = request.form['username']
        return redirect(url_for('first_session'))
    else:
        return '''
        <form method="POST">
            <p><input type=text name=username></p>
            <p><input type=submit value=Login>
        </form>
        '''

# Message Flashing
@app.route("/flash_index",methods=["GET"])
def flash_index():
    return render_template("index.html")

import logging

logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.route("/flash_login",methods = ["GET","POST"])
def flash_login():
    error = None
    if request.method == "POST":
        if request.form["username"] != "admin" or request.form["password"] != "secret":
            flash("Invalid Password",'error')
            app.logger.debug("Invalid password")
        else:
            flash("You were successfully logged in",'success')
            app.logger.debug("Success")
            return redirect(url_for('flash_index'))
    return (render_template("login.html",error=error))