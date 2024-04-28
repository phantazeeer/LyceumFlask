from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class Add_Post(FlaskForm):
    name = StringField("Тема поста", validators=[DataRequired()])
    text = TextAreaField()
    pic = MultipleFileField("Загрузить картинки")
    submit = SubmitField("Создать/изменить тему")