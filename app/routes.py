from flask import render_template, flash, redirect, url_for, request, session
from app import app, db
from app.forms import createWord, searchWord
from app.models import Lexicon
import sqlalchemy as sa
import sqlalchemy.orm as so

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
                          selectedpos, form.inflection.data, form.wordclass.data, form.notes.data, form.etymology.data)
        db.session.add(newword)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('createword.html', title='Create word', form=form, pos=pos)

@app.route('/dictionary', methods=['GET', 'POST'])
def dictionary():
    form = searchWord()
    if form.validate_on_submit():
        session['term'] = form.term.data
        return redirect(url_for('dictresults'))
    return render_template('dictionary.html', form=form)

@app.route('/dictresults', methods=['GET', 'POST'])
def dictresults():
    substring = session['term']
    matches = (Lexicon.query.filter(Lexicon.word.icontains(substring)).order_by(Lexicon.word).all() or
               Lexicon.query.filter(Lexicon.definition.icontains(substring)).order_by(Lexicon.word).all())
    return render_template('dictionaryresults.html', term=substring, matches=matches)

@app.route('/word/<name>', methods=['GET', 'POST'])
def word(name):
    match = Lexicon.query.filter(Lexicon.word == name)
    return render_template('word.html', word=match)