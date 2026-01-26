from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, PasswordField, EmailField, TextAreaField

from wtforms.validators import DataRequired, Length, EqualTo

class RegForm(FlaskForm):
    user_name = StringField("UserName", validators=[DataRequired()], render_kw={"placeholder":"Имя пользователя"})
    email = EmailField("Email", validators=[DataRequired()], render_kw={"placeholder":"Электронная почта"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=20)] , render_kw={"placeholder":"Пароль"})
    password_confirm = PasswordField("Password", validators=[DataRequired(), EqualTo('password')] , render_kw={"placeholder":"Повтор пароля"})
    submit = SubmitField(render_kw={"value":"Отправить"})

class AuthForm(FlaskForm):
    user_name = StringField("UserName", validators=[DataRequired()], render_kw={"placeholder":"Имя пользователя"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=20)], render_kw={"placeholder":"Пароль"})
    submit = SubmitField(render_kw={"value":"Отправить"})

class PostCreationForm(FlaskForm):
    caption = TextAreaField("Текст поста", validators=[Length(max=300)], render_kw={"placeholder":"Текст поста"})
    file = FileField(render_kw={"placeholder":"Файл поста"})
    submit = SubmitField(render_kw={"value":"Отправить"})