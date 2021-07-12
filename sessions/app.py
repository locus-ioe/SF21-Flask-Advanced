from flask import Flask, redirect, render_template, session, url_for
from flask_wtf import FlaskForm

from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config.from_pyfile("config.py")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


@app.route("/")
def index():
    if "username" in session:
        return render_template("index.html")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session["username"] = form.username.data
        return redirect(url_for("index"))

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.pop("username")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
