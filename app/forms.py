from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Optional, NumberRange, ValidationError

# Custom-defined length check validator, with default values min=1 and max=255
def lengthcheck(min=1, max=255):
    # The error message to be displayed.
    message = 'Must be between %d and %d characters long.' % (min, max)
    def _lengthcheck(form, field):
        l = field.data and len(field.data) or 0
        if l < min or max != -1 and l > max:
            raise ValidationError(message)
    return _lengthcheck

def isint(form, field):
    # This custom validator checks whether the inputted data fits into the restrictions.
    if type(field.data) != int or field.data < 0:
        raise ValidationError('Please enter a valid positive integer!')
class createWord(FlaskForm):
    # Each attribute has a validation check. The length check is being used here.
    word = StringField('Word', validators=[DataRequired(), lengthcheck(max=50)])
    # This validator checks if the data is a positive integer.
    wordclass = StringField('Word class', validators=[Optional(), isint])
    pronunciation = StringField('Pronunciation (leave empty to auto-generate)', validators=[Optional(), lengthcheck(max=50)])
    conscript = StringField('Conscript (leave empty to auto-generate)', validators=[Optional(), lengthcheck(max=50)])
    definition = StringField('Definition', validators=[DataRequired(), lengthcheck(max=255)])
    notes = TextAreaField('Notes', validators=[Optional()])
    etymology = TextAreaField('Etymology', validators=[Optional()])
    inflection = StringField('Inflection', validators=[Optional()])
    irregular = BooleanField('Irregular', validators=[Optional()])
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
    nretnas = BooleanField()
    vretnas = BooleanField()
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
    nretplo = BooleanField()
    vretplo = BooleanField()
    npalplo = BooleanField()
    vpalplo = BooleanField()
    nvelplo = BooleanField()
    vvelplo = BooleanField()
    ngloplo = BooleanField()
    # SIBILANT AFFRICATES
    nalvsaf = BooleanField()
    valvsaf = BooleanField()
    npavsaf = BooleanField()
    nretsaf = BooleanField()
    vretsaf = BooleanField()
    vpavsaf = BooleanField()
    npalsaf = BooleanField()
    vpalsaf = BooleanField()
    # SIBILANT FRICATIVE
    nalvsif = BooleanField()
    valvsif = BooleanField()
    npavsif = BooleanField()
    vpavsif = BooleanField()
    nretsif = BooleanField()
    vretsif = BooleanField()
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
    nretnsf = BooleanField()
    vretnsf = BooleanField()
    npalnsf = BooleanField()
    vpalnsf = BooleanField()
    nvelnsf = BooleanField()
    vvelnsf = BooleanField()
    nglonsf = BooleanField()
    vglonsf = BooleanField()
    # APPROXIMANTS
    vladapr = BooleanField()
    valvapr = BooleanField()
    vretapr = BooleanField()
    vpalapr = BooleanField()
    vvelapr = BooleanField()
    vgloapr = BooleanField()
    # TAPS/FLAPS
    vbiltap = BooleanField()
    vladtap = BooleanField()
    nalvtap = BooleanField()
    valvtap = BooleanField()
    nrettap = BooleanField()
    vrettap = BooleanField()
    # TRILLS
    nbiltri = BooleanField()
    vbiltri = BooleanField()
    nalvtri = BooleanField()
    valvtri = BooleanField()
    nrettri = BooleanField()
    vrettri = BooleanField()
    # LATERAL APPROXIMANTS
    valvlap = BooleanField()
    vretlap = BooleanField()
    vpallap = BooleanField()
    vvellap = BooleanField()
    # VOWELS
    clfu = BooleanField()
    clfr = BooleanField()
    clcu = BooleanField()
    clcr = BooleanField()
    clbu = BooleanField()
    clbr = BooleanField()
    ncfu = BooleanField()
    ncfr = BooleanField()
    ncbr = BooleanField()
    cmfu = BooleanField()
    cmfr = BooleanField()
    cmcu = BooleanField()
    cmcr = BooleanField()
    cmbu = BooleanField()
    cmbr = BooleanField()
    mifu = BooleanField()
    mifr = BooleanField()
    mic = BooleanField()
    mibu = BooleanField()
    mibr = BooleanField()
    omfu = BooleanField()
    omfr = BooleanField()
    omcu = BooleanField()
    omcr = BooleanField()
    ombu = BooleanField()
    ombr = BooleanField()
    nofu = BooleanField()
    noc = BooleanField()
    opfu = BooleanField()
    opfr = BooleanField()
    opcu = BooleanField()
    opbu = BooleanField()
    opbr = BooleanField()
    # END
    submit = SubmitField('Save')
    replacements = TextAreaField('Replacements', validators=[Optional()])

class createText(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Text content', validators=[DataRequired()])
    submit = SubmitField('Create')

# An example of a Flask Form.
class modifyText(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Original content', validators=[DataRequired()])
    submit = SubmitField('Save')

class searchText(FlaskForm):
    title = StringField('Search by text:')
    submit = SubmitField('Search')

class infForm(FlaskForm):
    submit = SubmitField('Save all inflections')

class gloss(FlaskForm):
    title = StringField('Title')
    text = TextAreaField('Enter the text you want to be glossed.')
    submit = SubmitField('Generate')