"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from datetime import datetime
from model import User
# from model import Rating
from model import Movie

from model import connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print("Users")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    # >>> date_str6 = "01-Jan-1995"
    # >>> format6 = "%d-%b-%Y"
    # >>> date6 = datetime.strptime(date_str6, format6)
    # >>> date6
    # datetime.datetime(1995, 1, 1, 0, 0)
    # >>> date6.year
    # 1995

    print("Movies")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Movie.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.item"):
        row = row.rstrip()
        movie_data = row.split("|")

        title = movie_data[1].split()
        title.pop()
        title = ' '.join(title)

        released_at = movie_data[2]
        format_released_at = "%d-%b-%Y"
        date_released = datetime.strptime(released_at, format_released_at)



        movie = Movie(movie_id=movie_data[0],
                    title=title,
                    released_at=date_released,
                    imdb_url = movie_data[4])

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
