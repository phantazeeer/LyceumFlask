from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    username = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    age = DateField("Дата рождения", validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')