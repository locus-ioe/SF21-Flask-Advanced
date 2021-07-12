from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import InputRequired, NumberRange
from wtforms.fields.html5 import IntegerField


class CategoryForm(FlaskForm):
    name = StringField("Category Name", validators=[InputRequired()])
    submit = SubmitField("Submit")


class TagForm(FlaskForm):
    name = StringField("Tag Name", validators=[InputRequired()])
    submit = SubmitField("Submit")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired("Title required")])
    body = StringField("Body", validators=[InputRequired("Body Required")])
    category = SelectField(
        "Category",
        coerce=int,
    )
    tags = SelectMultipleField("Tags", coerce=int)
    submit = SubmitField("Submit")


class NameForm(FlaskForm):
    name = StringField("Full Name")  # add validation here
    submit = SubmitField("Submit")


class NameFormSecond(FlaskForm):
    name = StringField("Full Name", validators=[InputRequired()])
    age = IntegerField(
        "Age",
        validators=[
            InputRequired(),
            NumberRange(min=13, max=60, message="Age must be between 13 and 60."),
        ],
    )
    submit = SubmitField("Submit")
