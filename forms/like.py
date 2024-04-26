from flask_wtf import FlaskForm
from wtforms import SubmitField


class Like(FlaskForm):
    like = SubmitField("Понравилось")