from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import createWord

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'miguel'}
    return render_template('index.html', title='Welcome', user=user)

@app.route('/createword', methods=['GET', 'POST'])
def createword():
    form = createWord()
    if form.validate_on_submit():
        flash('Word {} created with definition {} and pronunciation {}.'.format(form.word.data, form.definition.data, form.pronunciation.data))
        return redirect(url_for('index'))
    return render_template('createword.html', title='Create word', form=form)