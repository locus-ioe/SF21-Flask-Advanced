from flask import Flask, render_template, flash, redirect, url_for
from forms import NameForm, NameFormSecond

app = Flask(__name__)
app.config.from_pyfile("config.py")


@app.route("/")
def index():
    return render_template("index.html")


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


if __name__ == "__main__":
    app.run(debug=True)
