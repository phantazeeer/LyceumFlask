from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, DateField, StringField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    name = StringField("Имя", validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    rep_pass = PasswordField("Повторите пароль", validators=[DataRequired()])
    surname = StringField("Фамилия")
    second_name = StringField('Отчество')
    age = DateField("Дата рождения", validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')