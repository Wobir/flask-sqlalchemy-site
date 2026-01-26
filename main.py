from flask import Flask, render_template, request, redirect, url_for, session

from models import db, User, UserPost

from forms import RegForm, AuthForm, PostCreationForm

import os, uuid

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "secret-key"
def allowed_file(filename):
    return ('.' in filename) and (filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
db.init_app(app)



@app.route('/', methods=["GET", "POST"])
def index():
    posts = UserPost.query.all()
    if session['user_id']:
        user = User.query.filter_by(id = session['user_id']).first()
    return render_template('index.html', posts = posts)

@app.route('/create_post/', methods=["GET", "POST"])
def create_post():
    createPostForm = PostCreationForm()
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if createPostForm.validate_on_submit():
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
    return render_template('create_post.html', form = createPostForm)

@app.route('/auth/', methods=["GET", "POST"])
def login():
    authForm = AuthForm()
    if authForm.validate_on_submit():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(username = username).first()
            if user and user.password == password:
                session['user_id'] = user.id
                return redirect(url_for('show_user', id=user.id))
            else:
                return render_template('auth.html',form = authForm, error='Неверное имя пользователя или пароль')
    return render_template('auth.html', form = authForm)

@app.route('/logout/', methods=["GET", "POST"])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/reg/', methods=["GET", "POST"])
def reg():
    regForm = RegForm()
    message = ""

    if regForm.validate_on_submit():
        if request.method == "POST":
            username = request.form.get("user_name")
            email = request.form.get("email")
            password = request.form.get("password")
            if User.query.filter_by(username = username).first() or User.query.filter_by(email = email).first():
                message = "Пользователь с таким именем или почтой уже существует"
                return render_template("reg.html", form = regForm, message = message)
            logo_filename = "default.jpeg"

            new_user = User(
                username=username,
                email=email,
                password=password,
                logo=logo_filename
            )
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return redirect(url_for('show_user', id=new_user.id))
    return render_template("reg.html", form = regForm, message = message)

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