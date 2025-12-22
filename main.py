from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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

        new_user = User(username = username, email = email, password = password, age = age)
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(username=username).first()
        #return render_template("user_info.html", user=user)
        return redirect(url_for(F"user/{user.id}"))
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