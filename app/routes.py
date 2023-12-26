from flask import render_template, flash, redirect, url_for, request, session
from app import app, db
from app.forms import createWord, searchWord, deleteWord, ipatable, createText, searchText
from app.models import Lexicon, Phonology, Texts
import app.customscripts as cs
from sqlalchemy.sql import collate

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
        if form.pronunciation.data == '':
            pronunciation = cs.ipacreate(form.word.data)
        else:
            pronunciation = form.pronunciation.data
        if form.conscript.data == '':
            conscript = cs.concreate(form.word.data)
        else:
            conscript = form.conscript.data
        newword = Lexicon(form.word.data, pronunciation, conscript, form.definition.data,
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

@app.route('/dictionary/search', methods=['GET', 'POST'])
def dictresults():
    substring = session['term']
    matches = (Lexicon.query.filter(Lexicon.word.icontains(substring)).order_by(collate(Lexicon.word, 'NOCASE')).all() or
               Lexicon.query.filter(Lexicon.definition.icontains(substring)).order_by(collate(Lexicon.word, 'NOCASE')).all())
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
        if form.pronunciation.data == '':
            refitem.pronunciation = cs.ipacreate(refitem.word)
        else:
            refitem.pronunciation = form.pronunciation.data
        if form.conscript.data == '':
            refitem.conscript = cs.concreate(refitem.word)
        else:
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
    form = ipatable()
    exists = Phonology.query.filter(Phonology.exists == True).all()
    if form.validate_on_submit():
        flash('Phonological inventory, romanization and conscript systems have been updated.')
        for field in form:
            if field.name != 'csrf_token' and field.name != 'submit':
                match = Phonology.query.filter(Phonology.phoneme == field.name).first()
                match.exists = field.data
        for temp in exists:
            for key in request.form.keys():
                for value in request.form.getlist(key):
                    if 'rom ' + temp.phoneme == key:
                        temp.romanized = value
                    elif 'con ' + temp.phoneme == key:
                        temp.conscript = value
        db.session.commit()
        return redirect(url_for('phonology'))
    for field in form:
        if field.name != 'csrf_token' and field.name != 'submit':
            match = Phonology.query.filter(Phonology.phoneme == field.name).first()
            field.data = match.exists
    return render_template('phonology.html', form=form, exists=exists)

@app.route('/texts', methods=['GET', 'POST'])
def texts():
    form = searchText()
    matches = Texts.query.order_by(collate(Texts.title, 'NOCASE')).all()
    if form.validate_on_submit():
        session['title'] = form.title.data
        return redirect(url_for('textresults'))
    return render_template('texts.html', matches=matches, form=form)

@app.route('/texts/search', methods=['GET', 'POST'])
def textresults():
    substring = session['title']
    matches = Texts.query.filter(Texts.title.icontains(substring)).order_by(collate(Texts.title, 'NOCASE')).all()
    if substring=="":
        stitle = "Showing all results"
    else:
        stitle = "Results for " + substring
    return render_template('textresults.html', term=substring, title=stitle, matches=matches)

@app.route('/texts/create', methods=['GET', 'POST'])
def createtext():
    status = ['Complete', 'Work in Progress', 'Incomplete']
    form = createText()
    if form.validate_on_submit():
        nstatus = request.form.get('status')
        created = Texts(form.title.data, nstatus, form.content.data)
        flash('Translatable text {} with status {} created.'.format(created.title, created.status))
        db.session.add(created)
        db.session.commit()
        return render_template('textresults.html')
    return render_template('createtext.html', form=form, status=status)

@app.route('/texts/<id>/', methods=['GET', 'POST'])
def readtext(id):
    match = Texts.query.filter(Texts.id == id)
    return render_template('createtext.html', match=match)