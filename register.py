import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def register(username, password):
    inputUser = username
    inputPassword = password
    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                    {"username":inputUser, "password": inputPassword})

    print("you have registered!")
    db.commit()


def main():
    username = str(input("\nUsername: "))
    password = str(input("\nPassword: "))
    register(username, password)


if __name__ == "__main__":
    main()

