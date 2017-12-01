from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from script import validate


# App config.
DEBUG = True
application = Flask(__name__)
application.config.from_object(__name__)
application.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])


@application.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        name = request.form['name']
        print(name)
        validated_name = validate(name)
        print(validated_name)

        if form.validate():
            # Save the comment here.
            flash('Hello ' + validated_name)
        else:
            flash('Error: All the form fields are required. ')

    return render_template('hello.html', form=form)
	
if __name__ == "__main__":
    application.run()
