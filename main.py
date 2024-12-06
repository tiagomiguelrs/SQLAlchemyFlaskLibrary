from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired, NumberRange
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

class Base(DeclarativeBase):
  pass


class BookForm(FlaskForm):
    book = StringField(label="Book", validators=[DataRequired()],
                       render_kw={"class": "form-control", "placeholder": "Write the book name."})
    author = StringField(label="Author", validators=[DataRequired()],
                         render_kw={"class": "form-control", "placeholder": "Write the author name."})
    rating = DecimalField(label="Rating", validators=[DataRequired(), NumberRange(min=0, max=10)],
                          render_kw={"class": "form-control", "placeholder": "Rate from 0 to 10."})
    submit = SubmitField(label="Submit", render_kw={"class": "btn btn-primary"})


app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config["SECRET_KEY"] = "Somekey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Library.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Books(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[str] = mapped_column(nullable=False)

@app.route('/')
def home():
    with app.app_context():
        db.create_all()
        result = db.session.execute(db.select(Books).order_by(Books.id))
        all_books = [book for book in result.scalars()]
    return render_template("index.html", all_books=all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    form = BookForm()
    if form.is_submitted():
        print("submitted")
    if form.validate():
        print("valid")
    else:
        print(form.errors)
    if form.validate_on_submit():
        with app.app_context():
            db.create_all()
            new_row = Books(title=form.book.data, author=form.author.data, rating=f"{form.rating.data}/10")  # id can be omitted due to its primary key nature=
            db.session.add(new_row)
            db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=form)


@app.route("/edit/<int:_id>", methods=["POST", "GET"])
def edit(_id):
    form = BookForm()

    # Disable validators
    form.book.validators = []
    form.author.validators = []

    if form.is_submitted():
        print("submitted")
    if form.validate():
        print("valid")
    else:
        print(form.errors)
    if form.validate_on_submit():
        with app.app_context():
            db.create_all()
            book_to_update = db.session.execute(db.select(Books).where(Books.id == _id)).scalar()
            book_to_update.rating = f"{form.rating.data}/10"
            db.session.commit()

        # Enable validators
        form.book.validators = [DataRequired()]
        form.author.validators = [DataRequired()]
        return redirect(url_for("home"))
    return render_template("edit.html", form=form, _id=_id)

@app.route("/delete/<int:_id>")
def delete(_id):
    with app.app_context():
        db.create_all()
        book_to_delete = db.session.execute(db.select(Books).where(Books.id == _id)).scalar()
        db.session.delete(book_to_delete)
        db.session.commit()
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)
    db.session.close()

