from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# CREATE TABLE


class books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'{self.title} - {self.author} - {self.rating}/10'


db.create_all()


@app.route('/')
def home():
    all_books_in_database = db.session.query(books).all()
    return render_template("index.html", books=all_books_in_database)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":

        # collecting form (which will be in form of dictonary)
        data = request.form

        # creating new row in database by creating an object of 'books' class
        new_book = books(title=data['title'], author=data['author'], rating=data['rating'])

        # Adding book in created database
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template("add.html")


@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit_rating(id):
    if request.method == "POST":
        book_id = id
        book_to_update = books.query.get(book_id)
        print(book_to_update)
        book_to_update.rating = request.form["new_rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book = books.query.get(id)
    return render_template("edit.html", book_id=id, book=book)


@app.route('/delete/<int:id>')
def delete_book(id):
    book_id = id
    book_to_delete = books.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
