# -*- coding: utf-8 -*-
import os
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy.sql.expression import func, select
from werkzeug.utils import secure_filename
from wtforms import Form, BooleanField, TextField, PasswordField, TextAreaField, SelectField, FileField, HiddenField, validators

app = Flask(__name__)

# Check if we're on Openshift
if 'OPENSHIFT_APP_DNS' in os.environ:
    app.config.from_pyfile('app-openshift.cfg')
else:
    app.config.from_pyfile('app-local.cfg')
db = SQLAlchemy(app)

class Model(db.Model):
    __tablename__ = 'model'
    id = db.Column('model_id', db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)

    def __init__(self, title, description):
        self.title = title
        self.description = description

class InputForm(Form):
    title = TextField('Title', [validators.required(), validators.Length(max=45)], description="Enter a title")
    description = TextAreaField('Description', [validators.required(), validators.length(max=1300)], description="Enter a description")

# Randomize and redirect to challenge if exists, otherwise go to admin
@app.route('/')
def index():
	form = InputForm(request.form)
	if request.method == 'POST' and form.validate():
            # Save to database
            model = Model(form.title.data, form.description.data)
            db.session.add(model)
            db.session.commit()
            flash(u'Modellen har lagts till', 'primary')
            return redirect(url_for('index'))
	return render_template('index.html', form=form)

# Empties the database and creates all tables
@app.route('/clean_db')
def clean_db():
    db.drop_all()
    db.create_all()
    flash(u'Database records updated', 'primary')
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run()
