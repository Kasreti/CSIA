from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
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