from flask import Flask, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm

from wtforms import SelectField, SelectMultipleField, StringField, SubmitField, widgets
from wtforms.validators import InputRequired

app = Flask(__name__)

app.config.from_pyfile("config.py")
db = SQLAlchemy(app)


tags = db.Table(
    "tags",
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"), primary_key=True),
)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Tag {self.name}>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = db.relationship("Category", backref=db.backref("posts", lazy=True))

    tags = db.relationship(
        "Tag", secondary=tags, lazy="subquery", backref=db.backref("posts", lazy=True)
    )

    def __repr__(self):
        return f"<Post {self.title}>"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Category {self.name}>"


class CategoryForm(FlaskForm):
    name = StringField("Category Name", validators=[InputRequired()])
    submit = SubmitField("Submit")


class TagForm(FlaskForm):
    name = StringField("Tag Name", validators=[InputRequired()])
    submit = SubmitField("Submit")


# CREATE A CUSTOM WIDGET

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """

    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class PostForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired("Title required")])
    body = StringField("Body", validators=[InputRequired("Body Required")])
    category = SelectField(
        "Category",
        coerce=int,
    )
    tags = MultiCheckboxField("Tags", coerce=int)
    submit = SubmitField("Submit")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tags", methods=["GET", "POST"])
def get_tags():
    form = TagForm()
    if form.validate_on_submit():
        name = form.name.data

        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for("get_tags"))

    return render_template("tags.html", tags=Tag.query.all(), form=form)


@app.route("/posts", methods=["GET", "POST"])
def get_posts():
    form = PostForm()
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
    form.category.choices = [
        (category.id, category.name) for category in Category.query.all()
    ]
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category_id = form.category.data
        tag_ids = form.tags.data
        tags = [Tag.query.get(tag_id) for tag_id in tag_ids]

        post = Post(title=title, body=body, category_id=category_id)
        post.tags = tags
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("get_posts"))

    return render_template(
        "posts.html",
        posts=Post.query.all(),
        tags=Tag.query.all(),
        categories=Category.query.all(),
        form=form,
    )


@app.route("/categories", methods=["GET", "POST"])
def get_categories():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data

        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("get_categories"))

    return render_template(
        "categories.html", categories=Category.query.all(), form=form
    )


if __name__ == "__main__":
    print("Creating Database...")
    db.create_all()
    print("Database Created!")
