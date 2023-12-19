from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Optional

class createWord(FlaskForm):
    word = StringField('Word', validators=[DataRequired()])
    pronunciation = StringField('Pronunciation', validators=[Optional()])
    conscript = StringField('Conscript', validators=[Optional()])
    definition = StringField('Definition', validators=[DataRequired()])
    notes = StringField('Notes', validators=[Optional()])
    etymology = StringField('Etymology', validators=[Optional()])
    wordclass = IntegerField('Word class', validators=[Optional()])
    inflection = StringField('Inflection', validators=[Optional()])
    csubmit = SubmitField('Create')
    esubmit = SubmitField('Save')

class searchWord(FlaskForm):
    term = StringField('Search by word or definition:')
    submit = SubmitField('Search')

class deleteWord(FlaskForm):
    submit = SubmitField('Yes')