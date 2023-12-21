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

class ipatable(FlaskForm):
    # NASALS
    nbilnas = BooleanField()
    vbilnas = BooleanField()
    nladnas = BooleanField()
    vladnas = BooleanField()
    nalvnas = BooleanField()
    valvnas = BooleanField()
    npalnas = BooleanField()
    vpalnas = BooleanField()
    nvelnas = BooleanField()
    vvelnas = BooleanField()
    nglonas = BooleanField()
    vglonas = BooleanField()
    # PLOSIVES
    nbilplo = BooleanField()
    vbilplo = BooleanField()
    nladplo = BooleanField()
    vladplo = BooleanField()
    nalvplo = BooleanField()
    valvplo = BooleanField()
    npalplo = BooleanField()
    vpalplo = BooleanField()
    nvelplo = BooleanField()
    vvelplo = BooleanField()
    ngloplo = BooleanField()
    vgloplo = BooleanField()
    # SIBILANT AFFRICATES
    nalvsaf = BooleanField()
    valvsaf = BooleanField()
    npavsaf = BooleanField()
    vpavsaf = BooleanField()
    npalsaf = BooleanField()
    vpalsaf = BooleanField()
    # SIBILANT FRICATIVE
    nalvsif = BooleanField()
    valvsif = BooleanField()
    npavsif = BooleanField()
    vpavsif = BooleanField()
    npalsif = BooleanField()
    vpalsif = BooleanField()
    # NON-SIBILANT FRICATIVES
    nbilnsf = BooleanField()
    vbilnsf = BooleanField()
    nladnsf = BooleanField()
    vladnsf = BooleanField()
    ndennsf = BooleanField()
    vdennsf = BooleanField()
    nalvnsf = BooleanField()
    valvnsf = BooleanField()
    nposnsf = BooleanField()
    vposnsf = BooleanField()
    npalnsf = BooleanField()
    vpalnsf = BooleanField()
    nvelnsf = BooleanField()
    vvelnsf = BooleanField()
    nglonsf = BooleanField()
    vglonsf = BooleanField()
    # APPROXIMANTS
    valvapr = BooleanField()
    vpalapr = BooleanField()
    vvelapr = BooleanField()
    vgloapr = BooleanField()

    submit = SubmitField('Save')