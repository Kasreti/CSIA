from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class createWord(FlaskForm):
    word = StringField('Word', validators=[DataRequired()])
    pronunciation = StringField('Pronunciation', validators=[DataRequired()])
    definition = StringField('Definition', validators=[DataRequired()])
    submit = SubmitField('Create')