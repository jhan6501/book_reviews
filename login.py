import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def login(username, password):
    user = db.execute("SELECT * FROM users WHERE (username = :username) AND (password = :password)", 
                        {"username":username, "password": password}).fetchone()
    if user is None:
        print ("no such user exists")
        return
    print (user)
    print ("you have entered a valid username and password!")

def main():
    username = str(input("\nUsername: "))
    password = str(input("\nPassword: "))
    login(username, password)

    

if __name__ == "__main__":
    main()

