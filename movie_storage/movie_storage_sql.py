from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import requests
import os


DB_URL = "sqlite:///movies.db"
load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

engine = create_engine(DB_URL, echo=True)

# Create the movies table if it does not exist
with engine.begin() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_url TEXT
        )
    """))
    connection.commit()


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster_url FROM movies"))
        movies = result.fetchall()
    return {row[0]: {"year": row[1], "rating": row[2], "poster_url": row[3]} for row in movies}


def add_movie(title):
    """Fetch a new movie from OMDB to the database."""
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()
    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to OMDB API.")
        return

    if data.get("Response") == "True":
        movie_title = data.get("Title")
        movie_year = int(data.get("Year", 0))
        movie_rating = float(data.get("imdbRating", 0.0))
        poster_url = data.get("Poster", "")

        with engine.connect() as connection:
            try:
                connection.execute(
                    text("INSERT INTO movies ("
                         "title, year, rating, poster_url)"
                         " VALUES ("
                         ":title, :year, :rating, :poster_url)"),
                                   {"title": title,
                                    "year":movie_year,
                                    "rating":movie_rating,
                                    "poster_url": poster_url})
                connection.commit()
                print(f"Movie '{title}' added successfully.")
            except Exception as e:
                print(f"Error: {e}")
    else:
        print(f"Movie '{title}' not found in OMDB.")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("DELETE FROM movies WHERE title = :title"),
                                    {"title": title})
        connection.commit()
        if result.rowcount :
            print(f"Movie '{title}' deleted successfully.")
        else:
            print(f"Movie '{title}' not found.")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("UPDATE movies SET rating = :rating WHERE title = :title"),
                                    {"rating": rating, "title": title})
        connection.commit()
        if result.rowcount :
            print(f"Movie '{title}' updated successfully.")
        else:
            print(f"Movie '{title}' not found.")
