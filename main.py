from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

import os, uuid

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "secret-key"
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

class UserPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image = db.Column(db.String(100), nullable = True)
    caption = db.Column(db.String(200), nullable = True)
    def __repr__(self):
        return f"Post ('{self.image}', '{self.id}')"

@app.route('/', methods=["GET", "POST"])
def index():
    posts = UserPost.query.all()
    user = User.query.filter_by(id = session['user_id']).first()
    return render_template('index.html', user=user, posts = posts)

@app.route('/create_post/', methods=["GET", "POST"])
def create_post():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == "POST":
        caption = request.form['caption']
        image_file = None
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename != "" and allowed_file(file.filename):
                filename = file.filename
                ext = filename.rsplit('.', 1)[1].lower()
                image_file = f"post_{uuid.uuid4().hex}.{ext}"
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], image_file))
        post = UserPost(
            user_id = session['user_id'],
            image = image_file,
            caption = caption
        )
        db.session.add(post)
        db.session.commit()
        return  redirect(url_for('index'))
    return render_template('create_post.html')

@app.route('/auth/', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username = username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('show_user', id=user.id))
        else:
            return render_template('auth.html', error='Неверное имя пользователя или пароль')
    return render_template('auth.html')

@app.route('/logout/', methods=["GET", "POST"])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/registration/', methods=["GET", "POST"])
def reg():
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
            return render_template("registration.html")
        if User.query.filter_by(email=email).first():
            return render_template("registration.html")

        logo_filename = "default.jpeg"

        if 'logo' in request.files:
            file = request.files['logo']
            if file and file.filename != '' and allowed_file(file.filename):
                logo_filename = file.filename
                ext = logo_filename.rsplit('.', 1)[1].lower()
                logo_filename = f'user_{uuid.uuid4().hex}.{ext}'
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

    return  render_template("registration.html")

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