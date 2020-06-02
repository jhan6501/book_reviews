import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL_BOOK_REVIEWS"))

#engine = create_engine("postgres://postgres:sparkyman173@127.0.0.1:5432/book_review")
#engine = create_engine("postgres://crhbfecjtgmrgq:8161b1edd8331f4d286fa058856318c9ce67379d22ea0bd28d921b4e615163a5@ec2-18-214-211-47.compute-1.amazonaws.com:5432/d7j2ftublem89d")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    print("hai before loop")
    for isbn, title, author, year in reader:
   
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added book with isn {isbn} called {title} by {author} written in {year}")
        print ("survived")
    db.commit()

if __name__ == "__main__":
    main()
