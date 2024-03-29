from flask import render_template, flash, redirect, url_for, request, session
from app import app, db
from app.forms import createWord, searchWord, deleteWord, ipatable, createText, searchText, modifyText, infForm, gloss
from app.models import Lexicon, Phonology, Texts, VerbInflections, NounInflections
import app.customscripts as cs
from sqlalchemy.sql import collate
import re


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Welcome')


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
        newword = Lexicon(form.word.data.strip(), pronunciation.strip(), conscript.strip(), form.definition.data.strip(),
                          selectedpos, form.wordclass.data, form.notes.data, form.etymology.data, None)
        db.session.add(newword)
        db.session.commit()
        return redirect(url_for('word', name=form.word.data))
    return render_template('createword.html', title='Create word', form=form, pos=pos)


@app.route('/dictionary', methods=['GET', 'POST'])
def dictionary():
    form = searchWord()
    if form.validate_on_submit():
        # The search keyword is saved as a session...
        session['term'] = form.term.data
        return redirect(url_for('dictresults'))
    return render_template('dictionary.html', form=form)


@app.route('/dictionary/search', methods=['GET', 'POST'])
def dictresults():
    # ...and is passed into the dictionary results page...
    substring = session['term']
    # where it can then be used in SQL queries.
    # Matching results are found and put into an array...
    matches = (Lexicon.query.filter(Lexicon.word.icontains(substring)).order_by(
        collate(Lexicon.word, 'NOCASE')).all() or
               Lexicon.query.filter(Lexicon.definition.icontains(substring)).order_by(
                   collate(Lexicon.word, 'NOCASE')).all())
    if substring == "":
        stitle = "Showing all results"
    else:
        stitle = "Results for " + substring
    # and passed to Jinja.
    return render_template('dictionaryresults.html', term=substring, title=stitle, matches=matches)


@app.route('/word/<name>', methods=['GET', 'POST'])
def word(name):
    match = Lexicon.query.filter(Lexicon.word == name).first()
    inf = []
    irf = []
    if match.partofspeech == "Verb":
        for inflection in VerbInflections.query.filter(VerbInflections.irregular == 0).all():
            inf.append(inflection)
    elif match.partofspeech == "Noun":
        for inflection in NounInflections.query.filter(NounInflections.irregular == 0).all():
            inf.append(inflection)
    if match.irregular == 1:
        irf = []
        if match.partofspeech == "Verb":
            for aspect in ['Present', 'Past Perfect', 'Future', 'Future Perfect', 'Subjunctive', 'Presumptive',
                           'Imperative']:
                m2 = (VerbInflections.query.filter(VerbInflections.aspect == (match.word + " " + aspect)).first())
                irf.append(m2)
        elif match.partofspeech == "Noun":
            m2 = (NounInflections.query.filter(NounInflections.number == (match.word + " SG")).first())
            if m2 != None:
                irf.append(NounInflections(match.word + " SG", 1, m2.NOM, m2.ACC, m2.GEN, m2.DAT, m2.OBL))
            else:
                irf.append(NounInflections(match.word + "temp", 1, "", "", "", "", ""))
            m3 = (NounInflections.query.filter(NounInflections.number == (match.word + " PL")).first())
            if m3 != None:
                irf.append(NounInflections(match.word + " SG", 1, m3.NOM, m3.ACC, m3.GEN, m3.DAT, m3.OBL))
            else:
                irf.append(NounInflections(match.word + "temp", 1, "", "", "", "", ""))
    else:
        if match.partofspeech == "Verb":
            placeholder = VerbInflections("temp", 1, "NA", "", "", "")
            irf = [placeholder] * 7
        elif match.partofspeech == "Noun":
            placeholder = NounInflections(match.word + "temp", 1, "", "", "", "", "")
            irf = [placeholder] * 2
    return render_template('word.html', word=match, inf=inf, irf=irf)


@app.route('/word/<name>/edit', methods=['GET', 'POST'])
def modifyword(name):
    pos = ['Adjective', 'Adverb', 'Conjunction', 'Demonstrative', 'Interrogative', 'Noun', 'Numeral', 'Pronoun',
           'Proper noun', 'Verb']
    match = Lexicon.query.filter(Lexicon.word == name).first()
    originalid = match.id
    form = createWord(obj=match)
    inf = []
    irf = []
    SG = ""
    PL = ""
    # The section below fetches the irregular inflections, if any for the relevant word.
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
        elif match.partofspeech == "Noun":
            SG = (NounInflections.query.filter(NounInflections.number == (match.word + " SG")).first())
            PL = (NounInflections.query.filter(NounInflections.number == (match.word + " PL")).first())
    else:
        if match.partofspeech == "Verb":
            placeholder = VerbInflections("temp", 1, "NA", "", "", "")
            irf = [placeholder] * 7
        elif match.partofspeech == "Noun":
            placeholder = NounInflections(match.word + "temp", 1, "", "", "", "", "")
            irf = [placeholder] * 2
    if form.validate_on_submit():
        selectedpos = request.form.get('posselect')
        flash('{} {} successfully edited.'.format(selectedpos, form.word.data))
        refitem = Lexicon.query.get(originalid)
        refitem.word = form.word.data.strip()
        if form.pronunciation.data == '':
            refitem.pronunciation = cs.ipacreate(refitem.word.strip())
        else:
            refitem.pronunciation = form.pronunciation.data.strip()
        if form.conscript.data == '':
            refitem.conscript = cs.concreate(refitem.word.strip())
        else:
            refitem.conscript = form.conscript.data.strip()

        refitem.definition = form.definition.data.strip()
        refitem.partofspeech = selectedpos
        refitem.inflection = form.inflection.data
        refitem.wordclass = form.wordclass.data
        refitem.notes = form.notes.data
        refitem.irregular = form.irregular.data
        refitem.etymology = form.etymology.data
        # The section below saves the relevant irregular inflections, if any.
        if form.irregular.data and selectedpos == "Verb":
            for aspect in inf:
                m2 = VerbInflections.query.filter(VerbInflections.aspect == (match.word + " " + aspect.aspect)).first()
                if m2 is not None:
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
        elif form.irregular.data and selectedpos == "Noun":
            ninf = NounInflections.query.filter(NounInflections.irregular == 0).all()
            for number in ninf:
                m2 = NounInflections.query.filter(NounInflections.number == (match.word + " " + number.number)).first()
                if m2 is not None:
                    db.session.delete(m2)
                for key in request.form.keys():
                    for value in request.form.getlist(key):
                        if key == (number.number + " NOM"):
                            NOM = value
                        elif key == (number.number + " ACC"):
                            ACC = value
                        elif key == (number.number + " GEN"):
                            GEN = value
                        elif key == (number.number + " DAT"):
                            DAT = value
                        elif key == (number.number + " OBL"):
                            OBL = value
                newaspect = NounInflections(form.word.data + " " + number.number, 1, NOM, ACC, GEN, DAT, OBL)
                db.session.add(newaspect)
        db.session.commit()
        return redirect(url_for('word', name=form.word.data, word=match.word))
    return render_template('modifyword.html', word=match, form=form, pos=pos, inf=inf, irf=irf, SG=SG, PL=PL)


@app.route('/word/<name>/delete', methods=['GET', 'POST'])
def deleteword(name):
    match = Lexicon.query.filter(Lexicon.word == name).first()
    originalid = match.id
    originalword = match.word
    form = deleteWord()
    if form.validate_on_submit():
        flash('{} has been deleted.'.format(originalword))
        # Find the entry in Lexicon that has the same ID to the word that is to be deleted,
        # and deleted the entry.
        Lexicon.query.filter(Lexicon.id == originalid).delete()
        # Save the database.
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
            if field.name != 'csrf_token' and field.name != 'submit' and field.name != 'replacements':
                match = Phonology.query.filter(Phonology.phoneme == field.name).first()
                match.exists = field.data
        for temp in exists:
            for key in request.form.keys():
                for value in request.form.getlist(key):
                    if 'rom ' + temp.phoneme == key:
                        temp.romanized = value
                    elif 'con ' + temp.phoneme == key:
                        temp.conscript = value
        # The file is opened with the 'write' mode -- overriding all existing data.
        # It must have UTF-8 encoding to be able to support all characters that my client
        # will need.
        rep = open("app/static/replacements.txt", "w", encoding="utf-8")
        # The entered data is written to the file, and the .txt is closed.
        rep.write(form.replacements.data)
        rep.close()
        db.session.commit()
        return redirect(url_for('phonology'))
    reptxt = open("app/static/replacements.txt", "r", encoding="utf-8")
    rep = reptxt.read()
    form.replacements.data = rep
    reptxt.close()
    for field in form:
        if field.name != 'csrf_token' and field.name != 'submit' and field.name != 'replacements':
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
        # Using the constructor created earlier, a new Texts object is created.
        created = Texts(form.title.data, nstatus, form.content.data)
        flash('Translatable text {} with status {} created.'.format(created.title, created.status))
        # The new object is added to the database.
        db.session.add(created)
        # The database is saved.
        db.session.commit()
        match = Texts.query.filter(Texts.title == form.title.data).first()
        if match.status=="Checklist":
            return redirect(url_for('editchecklist', id=match.id))
        else:
            return redirect(url_for('modifytext', id=match.id))
    return render_template('createtext.html', form=form, status=status)


@app.route('/texts/<id>/', methods=['GET', 'POST'])
def readtext(id):
    match = Texts.query.filter(Texts.id == id).first()
    print(match.translation)
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
    # match.content, which contains the full text as saved, is split into multiple lines
    # that can be separated at each punctuation mark.
    splits = re.split(r'(?<=[.!?,\-:;])\s*', match.content)
    splits.pop()
    if (match.translation != None):
        tsplits = re.split(r'(?<=[.!?,\-:;])\s*', match.translation)
    else:
        tsplits = [''] * len(splits)
    if form.validate_on_submit():
        # After the form has been submitted, form data can be obtained.
        # The GET method was used here to instruct the server to skip
        # over this code when no data has been submitted yet,
        # instead skipping to render the page.
        flash('Translation has been updated.')
        newtrans = ""
        for key in request.form.keys():
            for value in request.form.getlist(key):
                if key == "translated":
                    newtrans = newtrans + value + ' '
        match.status = request.form.get('status')
        match.title = form.title.data
        match.content = form.content.data.strip()
        match.translation = newtrans.strip()
        db.session.commit()
        return redirect(url_for('readtext', id=match.id))
    # The page is rendered.
    return render_template('modifytext.html', form=form, match=match, status=status, splits=splits, tsplits=tsplits)


@app.route('/checklist/<id>', methods=['GET', 'POST'])
def editchecklist(id):
    # The correct text has been selected by matching it with the right ID.
    match = Texts.query.filter(Texts.id == id).first()
    form = modifyText(obj=match)
    checklist = match.content.split(", ")
    exist = []
    complete = []
    # When the form has been submitted...
    if form.validate_on_submit():
        # Display a message at the top of the screen.
        flash('Checklist has been updated.')
        # Update the fields of the selected object with the form's data.
        match.title = form.title.data
        match.content = form.content.data
        # Save to database.
        db.session.commit()
        return redirect(request.url)
    for entry in checklist:
        # This line finds the first match in the Lexicon database that contains the substring entry
        # within the definition. The order_by(collate()) section ensures that the search results will
        # be caps-insensitive and sort it by alphabetical order, and it takes the first result.
        m2 = Lexicon.query.filter(Lexicon.definition == entry).order_by(collate(Lexicon.word, 'NOCASE')).first()
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
    ninf = []
    for inflection in VerbInflections.query.filter(VerbInflections.irregular == 0).all():
        vinf.append(inflection)
    for inflection in NounInflections.query.filter(NounInflections.irregular == 0).all():
        ninf.append(inflection)
    if form.validate_on_submit():
        flash('Inflections have been updated.')
        # This script fetches the values from each field.
        for aspect in vinf:
            for key in request.form.keys():
                for value in request.form.getlist(key):
                    if key == (aspect.aspect + " 1s"):
                        aspect.fs = value
                    elif key == (aspect.aspect + " 2s"):
                        aspect.ss = value
                    elif key == (aspect.aspect + " gen"):
                        aspect.other = value
        for number in ninf:
            for key in request.form.keys():
                for value in request.form.getlist(key):
                    if key == (number.number + " NOM"):
                        number.NOM = value
                    elif key == (number.number + " ACC"):
                        number.ACC = value
                    elif key == (number.number + " GEN"):
                        number.GEN = value
                    elif key == (number.number + " DAT"):
                        number.DAT = value
                    elif key == (number.number + " OBL"):
                        number.OBL = value
        db.session.commit()
        return redirect(request.url)
    return render_template('inflections.html', verb=vinf, form=form, SG=ninf[0], PL=ninf[1])


@app.route('/texts/<id>/gloss', methods=['GET', 'POST'])
def viewgloss(id):
    match = Texts.query.filter(Texts.id == id).first()
    status = ['Complete', 'Work in Progress', 'Incomplete']
    splits = re.split(r'(?<=[\.\!\?\,\-])\s*', match.translation)
    tsplits = []
    ipa = []
    con = []
    for sentence in splits:
        sentence.strip()
        tsplits.append(cs.gloss(sentence))
        # IPA notation requires slashes to be put before and after the IPA.
        ipa.append("/" + cs.ipacreate(sentence) + "/")
        con.append(cs.concreate(sentence))
    return render_template('gloss.html', match=match, status=status, splits=splits, tsplits=tsplits, ipa=ipa, con=con)


# This page deals with creating a gloss from an inputted text.
@app.route('/gloss/', methods=['GET', 'POST'])
def glosshome():
    # The form used in this script is imported from the forms.py file.
    form = gloss()
    # When the form has been submitted...
    if form.validate_on_submit():
        # Split the inputted string at every punctuation mark (.!?,-).
        splits = re.split(r'(?<=[.!?,\-])\s*', form.text.data)
        # Create three empty arrays: tsplits for the interlinear gloss, IPA for the transcription
        # and con for the conscript.
        tsplits = []
        ipa = []
        con = []
        for sentence in splits:
            if sentence != "":
                tsplits.append(cs.gloss(sentence))
                # Slashes are to be added around the IPA transcription as a standard convention.
                ipa.append("/" + cs.ipacreate(sentence) + "/")
                con.append(cs.concreate(sentence))
        # The three arrays are passed to the HTML page, where it will be dealt with by Jinja.
        return render_template('glossview.html', splits=splits, tsplits=tsplits, ipa=ipa, con=con)
    # If the form has not been submitted, instead load the glosshome.html page with the form.
    return render_template('glosshome.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    flash("This page doesn't exist!")
    return render_template("index.html")


@app.errorhandler(500)
def internal_server_error(e):
    flash("An internal server error has occurred! Please contact Kasreti.")
    return render_template("index.html")
