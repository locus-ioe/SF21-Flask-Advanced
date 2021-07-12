from . import db

tags = db.Table(
    "tags",
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
    db.Column("post_id", db.Integer, db.ForeignKey(
        "post.id"), primary_key=True),
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

    category_id = db.Column(db.Integer, db.ForeignKey(
        "category.id"), nullable=False)
    category = db.relationship(
        "Category", backref=db.backref("posts", lazy=True))

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
