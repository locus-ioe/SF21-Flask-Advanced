from . import app
from flask import render_template, redirect, url_for
from modular_flask.models import Tag, Category, Post
from modular_flask.forms import TagForm, CategoryForm, PostForm


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
