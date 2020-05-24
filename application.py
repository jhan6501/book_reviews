import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# # Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# # Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/register_page", methods = ["post"])
def registerPage():
    return render_template("register.html")

@app.route("/register", methods=["post"])
def register():
    inputUser = request.form.get("user")
    inputPassword = request.form.get("password")
    if (db.execute("SELECT * FROM users WHERE username = :username", {"username":inputUser}).fetchone() is None):
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                    {"username":inputUser, "password": inputPassword})
        db.commit()
        return render_template("new_account.html")
    return render_template("username_in_use.html")
    

@app.route("/login", methods=["post"])
def login():
    inputUser = str(request.form.get("user"))
    inputPassword = str(request.form.get("password"))

    user = db.execute("SELECT * FROM users WHERE (username = :username) AND (password = :password)", 
                        {"username":inputUser, "password": inputPassword}).fetchone()

    if user is None:
        return render_template("invalid.html")

    return render_template("success.html", user = user)

@app.route("/list_book", methods=["post"])
def search():
    user = str(request.form.get("user"))
    book_input = str(request.form.get("title"))
    query_convert = "'%" + book_input + "%'"
    query_convert = "SELECT * FROM books WHERE title LIKE " + query_convert
    books = db.execute(query_convert).fetchall()
    
    return render_template("bookInfo.html", user = user, books = books)

@app.route("/book_selection/<string:input>/<string:username>")
def book(input, username):
    
    # get the book
    book_isbn = ''
    user = ''
    firstRun = True
    for i in input:
        if i != ',' and firstRun:
            book_isbn = book_isbn + i
        elif i == ',' and firstRun:
            firstRun = False
        elif not firstRun:
            user = user + i
            
    print ("input is: " + input)
    print ("username is: " + username)
    print ("user is: " + user)
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": book_isbn}).fetchone()

    if book is None: 
        return render_template("error.html", message = "book does not exist")
    
    return render_template("book.html", book = book, username = user)


# @app.route("/book_selection/<string:input>/<string:username>")
# def book(input, username):
    
#     # get the book
#     book_isbn = ''
#     user = ''
#     firstRun = True
#     for i in input:
#         if i != ',' and firstRun:
#             book_isbn = book_isbn + i
#         elif i == ',' and firstRun:
#             firstRun = False
#         elif not firstRun:
#             user = user + i
            
#     print ("input is: " + input)
#     print ("username is: " + username)
#     print ("user is: " + user)
#     book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": book_isbn}).fetchone()

#     if book is None: 
#         return render_template("error.html", message = "book does not exist")
    
#     return render_template("book.html", book = book, username = user)


