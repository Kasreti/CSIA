from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import createWord
from app.models import Lexicon

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'miguel'}
    return render_template('index.html', title='Welcome', user=user)

@app.route('/createword', methods=['GET', 'POST'])
def createword():
    pos = ['Adjective', 'Adverb', 'Conjunction', 'Demonstrative', 'Interrogative', 'Noun', 'Numeral', 'Pronoun',
           'Proper noun', 'Verb']
    form = createWord()
    if form.validate_on_submit():
        selectedpos = request.form.get('posselect')
        flash('{} {} created with definition {} and pronunciation {}.'.format(selectedpos, form.word.data, form.definition.data, form.pronunciation.data))
        newword = Lexicon(form.word.data, form.pronunciation.data, form.conscript.data, form.definition.data,
                          selectedpos, form.inflection.data, form.wordclass.data, form.notes, form.etymology)
        db.session.add(newword)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('createword.html', title='Create word', form=form, pos=pos)