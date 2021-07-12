from flask_wtf import FlaskForm

from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import InputRequired, NumberRange


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
