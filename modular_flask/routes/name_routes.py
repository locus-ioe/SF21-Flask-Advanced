from . import app
from flask import render_template
from modular_flask.forms import NameForm, NameFormSecond


@app.route("/nameform", methods=["GET", "POST"])
def nameform():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
    return render_template("nameform.html", form=form, name=name)


@app.route("/nameform2", methods=["GET", "POST"])
def nameform2():
    name = None
    age = None
    form = NameFormSecond()
    if form.validate_on_submit():
        name = form.name.data
        age = form.age.data
        form.name.data = ""
        form.age.data = ""
    return render_template("nameform2.html", form=form, name=name, age=age)
