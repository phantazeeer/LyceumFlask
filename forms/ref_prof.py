from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class Refactor_Profile(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    surname = StringField("Фамилия", validators=[DataRequired()])
    second_name = StringField("Отчество")
    country = StringField("Страна  проживания")
    city = StringField("Город проживания")
    projects = TextAreaField("Объекты на которых вы работали")
    picture = FileField("Ваш аватар")
    submit = SubmitField("Сохранить")