from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired

class createWord(FlaskForm):
    word = StringField('Word', validators=[DataRequired()])
    pronunciation = StringField('Pronunciation')
    conscript = StringField('Conscript')
    definition = StringField('Definition', validators=[DataRequired()])
    notes = StringField('Notes')
    etymology = StringField('Etymology')
    wordclass = IntegerField('Word class')
    inflection = StringField('Inflection')
    submit = SubmitField('Create')

class searchWord(FlaskForm):
    term = StringField('Search by word or definition:', validators=[DataRequired()])
    submit = SubmitField('Search')