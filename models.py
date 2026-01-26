from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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