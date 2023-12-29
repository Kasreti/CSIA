from flask import render_template, flash, redirect, url_for, request, session
from app import app, db
from app.forms import createWord, searchWord, deleteWord, ipatable, createText, searchText, modifyText, infForm
from app.models import Lexicon, Phonology, Texts, VerbInflections
import app.customscripts as cs
from sqlalchemy.sql import collate
import re


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'miguel'}
    return render_template('index.html', title='Welcome', user=user)


@app.route('/word/create', methods=['GET', 'POST'])
def createword():
    pos = ['Adjective', 'Adverb', 'Conjunction', 'Demonstrative', 'Interrogative', 'Noun', 'Numeral', 'Pronoun',
           'Proper noun', 'Verb']
    form = createWord()
    if form.validate_on_submit():
        selectedpos = request.form.get('posselect')
        flash('{} {} created with definition {}.'.format(selectedpos, form.word.data, form.definition.data,
                                                         form.pronunciation.data))
        if form.pronunciation.data == '':
            pronunciation = cs.ipacreate(form.word.data)
        else:
            pronunciation = form.pronunciation.data
        if form.conscript.data == '':
            conscript = cs.concreate(form.word.data)
        else:
            conscript = form.conscript.data
        newword = Lexicon(form.word.data, pronunciation, conscript, form.definition.data,
                          selectedpos, form.wordclass.data, form.notes.data, form.etymology.data, form.irregular.data)
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
    matches = (Lexicon.query.filter(Lexicon.word.icontains(substring)).order_by(
        collate(Lexicon.word, 'NOCASE')).all() or
               Lexicon.query.filter(Lexicon.definition.icontains(substring)).order_by(
                   collate(Lexicon.word, 'NOCASE')).all())
    if substring == "":
        stitle = "Showing all results"
    else:
        stitle = "Results for " + substring
    return render_template('dictionaryresults.html', term=substring, title=stitle, matches=matches)


@app.route('/word/<name>', methods=['GET', 'POST'])
def word(name):
    match = Lexicon.query.filter(Lexicon.word == name).first()
    inf = []
    if match.partofspeech == "Verb":
        for inflection in VerbInflections.query.filter(VerbInflections.irregular == 0).all():
            inf.append(inflection)
    if match.irregular == 1:
        irf = []
        if match.partofspeech == "Verb":
            for aspect in ['Present', 'Past Perfect', 'Future', 'Future Perfect', 'Subjunctive', 'Presumptive',
                           'Imperative']:
                m2 = (VerbInflections.query.filter(VerbInflections.aspect == (match.word + " " + aspect)).first())
                irf.append(m2)
    else:
        placeholder = VerbInflections("temp", 1, "NA", "", "" , "")
        irf = [placeholder]*7
    return render_template('word.html', word=match, inf=inf, irf=irf)


@app.route('/word/<name>/edit', methods=['GET', 'POST'])
def modifyword(name):
    pos = ['Adjective', 'Adverb', 'Conjunction', 'Demonstrative', 'Interrogative', 'Noun', 'Numeral', 'Pronoun',
           'Proper noun', 'Verb']
    match = Lexicon.query.filter(Lexicon.word == name).first()
    ogid = match.id
    form = createWord(obj=match)
    inf = []
    if match.partofspeech == "Verb":
        for inflection in VerbInflections.query.filter(VerbInflections.irregular == 0).all():
            inf.append(inflection)
    if match.irregular == 1:
        irf = []
        if match.partofspeech == "Verb":
            for aspect in ['Present', 'Past Perfect', 'Future', 'Future Perfect', 'Subjunctive', 'Presumptive',
                           'Imperative']:
                m2 = (VerbInflections.query.filter(VerbInflections.aspect == (match.word + " " + aspect)).first())
                irf.append(m2)
    else:
        placeholder = VerbInflections("temp", 1, "NA", "", "", "")
        irf = [placeholder] * 7
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
        refitem.irregular = form.irregular.data
        refitem.etymology = form.etymology.data
        if form.irregular.data:
            for aspect in inf:
                m2 = VerbInflections.query.filter(VerbInflections.aspect == (match.word + " " + aspect.aspect)).first()
                db.session.delete(m2)
                for key in request.form.keys():
                    for value in request.form.getlist(key):
                        if key == (aspect.aspect + " 1s"):
                            fs = value
                        elif key == (aspect.aspect + " 2s"):
                            ss = value
                        elif key == (aspect.aspect + " gen"):
                            other = value
                newaspect = VerbInflections(refitem.word + " " + aspect.aspect, 1, aspect.gloss, fs, ss, other)
                db.session.add(newaspect)
        db.session.commit()
        return redirect(url_for('word', name=form.word.data, word=match.word))
    return render_template('modifyword.html', word=match, form=form, pos=pos, inf=inf, irf=irf)


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
    if substring == "":
        stitle = "Showing all results"
    else:
        stitle = "Results for " + substring
    return render_template('textresults.html', term=substring, title=stitle, matches=matches)


@app.route('/texts/create', methods=['GET', 'POST'])
def createtext():
    status = ['Complete', 'Work in Progress', 'Incomplete', 'Checklist']
    form = createText()
    if form.validate_on_submit():
        nstatus = request.form.get('status')
        created = Texts(form.title.data, nstatus, form.content.data)
        flash('Translatable text {} with status {} created.'.format(created.title, created.status))
        db.session.add(created)
        db.session.commit()
        match = Texts.query.filter(Texts.title == form.title.data).first()
        return redirect(url_for('modifytext', id=match.id))
    return render_template('createtext.html', form=form, status=status)


@app.route('/texts/<id>/', methods=['GET', 'POST'])
def readtext(id):
    match = Texts.query.filter(Texts.id == id).first()
    return render_template('readtext.html', match=match)


@app.route('/texts/<id>/delete', methods=['GET', 'POST'])
def deletetext(id):
    match = Texts.query.filter(Texts.id == id).first()
    form = deleteWord()
    if form.validate_on_submit():
        flash('{} has been deleted.'.format(match.title))
        Texts.query.filter(Texts.id == match.id).delete()
        db.session.commit()
        return redirect(url_for('texts'))
    return render_template('deletetext.html', match=match, form=form)


@app.route('/texts/<id>/edit', methods=['GET', 'POST'])
def modifytext(id):
    match = Texts.query.filter(Texts.id == id).first()
    status = ['Complete', 'Work in Progress', 'Incomplete']
    form = modifyText(obj=match)
    splits = re.split(r'(?<=[\.\!\?\,\-])\s*', match.content)
    splits.pop()
    if (match.translation != None):
        tsplits = re.split(r'(?<=[\.\!\?\,\-])\s*', match.translation)
        tsplits.pop()
    else:
        tsplits = [''] * len(splits)
    if form.validate_on_submit():
        flash('Translation has been updated.')
        newtrans = ""
        for key in request.form.keys():
            for value in request.form.getlist(key):
                if key == "translated":
                    newtrans = newtrans + value + ' '
        match.status = request.form.get('status')
        match.title = form.title.data
        match.content = form.content.data
        match.translation = newtrans
        db.session.commit()
        return redirect(url_for('readtext', id=match.id))
    return render_template('modifytext.html', form=form, match=match, status=status, splits=splits, tsplits=tsplits)


@app.route('/checklist/<id>', methods=['GET', 'POST'])
def editchecklist(id):
    match = Texts.query.filter(Texts.id == id).first()
    form = modifyText(obj=match)
    checklist = match.content.split(", ")
    exist = []
    complete = []
    if form.validate_on_submit():
        flash('Checklist has been updated.')
        match.title = form.title.data
        match.content = form.content.data
        return redirect(request.url)
    for entry in checklist:
        m2 = Lexicon.query.filter(Lexicon.definition.icontains(entry)).order_by(collate(Lexicon.word, 'NOCASE')).first()
        if m2 is not None:
            exist.append(m2.word)
            complete.append("Yes")
        else:
            exist.append("")
            complete.append("No")
    return render_template('modifychecklist.html', match=match, form=form, checklist=checklist,
                           exist=exist, complete=complete)


@app.route('/inflections', methods=['GET', 'POST'])
def inflections():
    form = infForm()
    vinf = []
    for inflection in VerbInflections.query.filter(VerbInflections.irregular == 0).all():
        vinf.append(inflection)
    if form.validate_on_submit():
        flash('Inflections have been updated.')
        for aspect in vinf:
            for key in request.form.keys():
                for value in request.form.getlist(key):
                    if key == (aspect.aspect + " 1s"):
                        aspect.fs = value
                    elif key == (aspect.aspect + " 2s"):
                        aspect.ss = value
                    elif key == (aspect.aspect + " gen"):
                        aspect.other = value
        db.session.commit()
        return redirect(request.url)
    return render_template('inflections.html', verb=vinf, form=form)

@app.route('/texts/<id>/gloss', methods=['GET', 'POST'])
def viewgloss(id):
    match = Texts.query.filter(Texts.id == id).first()
    status = ['Complete', 'Work in Progress', 'Incomplete']
    splits = re.split(r'(?<=[\.\!\?\,\-])\s*', match.translation)
    splits.pop()
    tsplits = []
    for sentence in splits:
        tsplits.append(cs.gloss(sentence))
    return render_template('viewgloss.html', match=match, status=status, splits=splits, tsplits=tsplits)
