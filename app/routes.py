from flask import render_template, flash, redirect, url_for, request, session
from app import app, db
from app.forms import createWord, searchWord, deleteWord, ipatable
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
        flash('{} {} created with definition {}.'.format(selectedpos, form.word.data, form.definition.data, form.pronunciation.data))
        newword = Lexicon(form.word.data, form.pronunciation.data, form.conscript.data, form.definition.data,
                          selectedpos, form.inflection.data, form.wordclass.data, form.notes.data, form.etymology.data)
        db.session.add(newword)
        db.session.commit()
        return redirect(url_for('word', name=form.word.data))
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
    if substring=="":
        stitle = "Showing all results"
    else:
        stitle = "Results for " + substring
    return render_template('dictionaryresults.html', term=substring, title=stitle, matches=matches)

@app.route('/word/<name>', methods=['GET', 'POST'])
def word(name):
    match = Lexicon.query.filter(Lexicon.word == name).first()
    return render_template('word.html', word=match)

@app.route('/word/<name>/edit', methods=['GET', 'POST'])
def modifyword(name):
    pos = ['Adjective', 'Adverb', 'Conjunction', 'Demonstrative', 'Interrogative', 'Noun', 'Numeral', 'Pronoun',
           'Proper noun', 'Verb']
    match = Lexicon.query.filter(Lexicon.word == name).first()
    ogid = match.id
    form = createWord(obj=match)
    if form.validate_on_submit():
        selectedpos = request.form.get('posselect')
        flash('{} {} successfully edited.'.format(selectedpos, form.word.data))
        refitem = Lexicon.query.get(ogid)
        refitem.word = form.word.data
        refitem.pronunciation = form.pronunciation.data
        refitem.conscript = form.conscript.data
        refitem.definition = form.definition.data
        refitem.partofspeech = selectedpos
        refitem.inflection = form.inflection.data
        refitem.wordclass = form.wordclass.data
        refitem.notes = form.notes.data
        refitem.etymology = form.etymology.data
        db.session.commit()
        return redirect(url_for('word', name=form.word.data, word = match.word))
    return render_template('modifyword.html', word=match, form=form, pos=pos)

@app.route('/word/<name>/delete', methods=['GET', 'POST'])
def deleteword(name):
    match = Lexicon.query.filter(Lexicon.word == name).first()
    ogid = match.id
    ogword = match.word
    form = deleteWord()
    if form.validate_on_submit():
        flash('{} has been deleted.'.format(ogword))
        Lexicon.query.filter(Lexicon.id == ogid).delete()
        db.session.commit()
        return redirect(url_for('dictionary'))
    return render_template('deleteword.html', word=match, form=form)

@app.route('/phonology', methods=['GET', 'POST'])
def phonology():
    return render_template('phonology.html', form=ipatable())