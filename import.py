import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
#engine = create_engine("postgres://bwqjnotesaxrki:386d9a8f30a5f9786baaf0a7a2c2b5f4da90e88b2501d77ddd26110edf9440be@ec2-35-174-127-63.compute-1.amazonaws.com:5432/dd0madk3d6q450")
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
