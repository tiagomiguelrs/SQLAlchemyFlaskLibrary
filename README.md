# Book Library Application

## Description
This project is a web application built using the Flask framework. It allows users to add, edit, and delete books in a library database. Each book entry includes the book's title, author, and a rating. The application uses SQLAlchemy for database management and Flask-WTF for form handling and validation.

## Features
Add Books: Users can add new books to the library by filling out a form with the book's title, author, and rating.

Edit Books: Users can edit the rating of existing books in the library.

Delete Books: Users can delete books from the library.

Data Storage: Stores book data in a SQLite database.

Bootstrap Integration: Uses Flask-Bootstrap to style the application.

Form Validation: Validates form inputs using Flask-WTF and WTForms.

## How It Works
Home Page: The home page displays a list of all books in the library.

Add Book: The /add route displays a form where users can enter details about a new book. The form includes fields for the book title, author, and rating. The data is validated and then added to the database.

Edit Book: The /edit/<int:_id> route displays a form where users can update the rating of an existing book. The book's ID is passed as a parameter to identify which book to update.

Delete Book: The /delete/<int:_id> route deletes a book from the database based on its ID.

Database Management: Uses SQLAlchemy to manage the SQLite database, including creating tables and handling CRUD operations.
