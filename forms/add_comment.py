from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class AddComment(FlaskForm):
    text = TextAreaField("Оставить комментарий", validators=[DataRequired()])
    picture = MultipleFileField("Прикрепить изображение")
    submit = SubmitField("Добавить комментарий")