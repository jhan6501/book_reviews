import os

from flask import Flask, session, render_template, request, jsonify, Blueprint
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests 


api = Blueprint("api", __name__, static_folder = "static", template_folder = "templates")

engine = create_engine(os.getenv("DATABASE_URL_BOOK_REVIEWS"))
db = scoped_session(sessionmaker(bind=engine))

@api.route("/api/books/<string:book_isbn>")
def book_api(book_isbn):
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": book_isbn}).fetchone()

    if book is None: 
        return jsonify({"error": "Invalid book isbn"}),422

    return jsonify({
        "book_id": book.id,
        "book_isbn": book.isbn,
        "book_title": book.title,
        "book_author": book.author,
        "book_year": book.year
    })


