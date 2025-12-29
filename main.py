from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return ('.' in filename) and (filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    logo = db.Column(db.String(60), nullable=False, default="default.jpeg")
    age = db.Column(db.Integer, nullable = True)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form["username"] and request.form["email"] and request.form["password"]:
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
        if request.form["age"]:
            age = request.form["age"]
        else:
            age = None
        if User.query.filter_by(username=username).first():
            return render_template("index.html")
        if User.query.filter_by(email=email).first():
            return render_template("index.html")

        logo_filename = "default.jpeg"

        if 'logo' in request.files:
            file = request.files['logo']
            if file and file.filename != '' and allowed_file(file.filename):
                logo_filename = file.filename
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], logo_filename))

        new_user = User(
            username = username,
            email = email,
            password = password,
            age = age,
            logo = logo_filename
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('show_user', id=new_user.id))

    return  render_template("index.html")

@app.route("/users/")
def users():
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/user/<id>")
def show_user(id):
    user = User.query.filter_by(id=id).first()
    return render_template("user_info.html", user=user)

with app.app_context():
    db.create_all()

app.run(debug=True)