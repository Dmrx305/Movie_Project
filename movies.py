import random
from movie_storage_sql import add_movie as add_movie_to_db
from movie_storage_sql import list_movies as list_movies_from_db
from movie_storage_sql import delete_movie
from movie_storage_sql import update_movie

def menu():
    """printing the main menu"""
    print("\n********** My Movies Database **********")
    print("\nMenu:")
    print("0. Exit")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Stats")
    print("6. Random movie")
    print("7. Search movie")
    print("8. Movies sorted by rating")
    print("9. Generate Website")


def list_movies():
    """list and print all the movies"""
    movies = list_movies_from_db()
    print(f"*** {len(movies)} movies in total ***")
    print()
    for title, info in movies.items():
        print(f"{title} ({info['year']}): {info['rating']}")


def add_movie():
    """adding a new movie"""
    movies = list_movies_from_db()
    while True:
        title = input("Name a movie to add: ")
        if title == "":
            print("Title may not be empty!")
        break
    add_movie_to_db(title)
    print(f"'{title}'has been successfully added")


def delete_movie_in_db():
    """deleting a movie"""
    title = input("Name a movie to delete: ")
    movies = list_movies_from_db()
    if title in movies:
        delete_movie(title)
        print(f"{title} has been removed!")
    else:
        print("Movie not in database.")


def update_movie_in_db():
    """updating a movies rating"""
    title = input("Name a movie to update: ")
    movies = list_movies_from_db()
    if title not in movies:
        print(f"Sry {title} not in the database!")
        return
    while True:
        try:
            rating = float(input("\nWhats's the new rating? "))
            break
        except ValueError:
            print("Rating must be a number!")
    update_movie(title, rating)
    print(f"\nUpdated rating for '{title}' to {rating}")


def movie_stats():
    """printing the combined movie stats"""
    movies = list_movies_from_db()
    ratings = []
    for movie in movies:
        ratings = [info["rating"] for info in movies.values()]
    print(f"Average rating is: {round(sum(ratings) / len(ratings), 1)}")  # rounded for similar stat appearance
    print(f"Highest rating is: {max(ratings)}")
    print(f"Lowest rating is: {min(ratings)}")


def random_movie():
    """Prints a random movie from the database"""
    movies = list_movies_from_db()
    title, details = random.choice(list(movies.items()))
    print(f"\n{title} ({details["year"]}) - Rating: {details["rating"]}")


def search_movie():
    """searching for a specific movie"""
    prompt = input("What movie are you looking for? ")
    movies = list_movies_from_db()
    found = False
    for title in movies:
        if prompt.lower() == title.lower():
            print(f"\n{title}({movies[title]["year"]}) {movies[title]["rating"]}")
            found = True
            break
    if not found:
        print("Movie not found!")


def sorted_movies():
    """sorting the movies by rank descending"""
    movies = list_movies_from_db()
    sorted_movies_by_rank = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)
    for title, info in sorted_movies_by_rank:
        print(f"{title} ({info["year"]}) - Rating: {info["rating"]}")


def generate_website():
    """Generates an HTML website using the movie template."""
    try:
        with open("index_template.html", "r", encoding="utf-8") as template_file:
            template_content = template_file.read()

        movies = list_movies_from_db()
        movie_items = ""
        for title, info in movies.items():
            poster = info['poster_url'] or "https://via.placeholder.com/150"
            movie_items += f"""
            <li>
                <div class="movie">
                    <img class="movie-poster" src="{poster}" alt="{title} poster">
                    <div class="movie-title">{title}</div>
                    <div class="movie-year">({info['year']}) - Rating: {info['rating']}</div>
                </div>
            </li>
            """

        final_content = template_content.replace("{{ movie_list }}", movie_items)

        with open("index.html", "w", encoding="utf-8") as output_file:
            output_file.write(final_content)

        print("Website generated successfully as 'index.html'!")

    except FileNotFoundError:
        print("Template file 'index_template.html' not found!")


def main():
    print()
    while True:
        menu()

        try:
            choice = int(input("\nEnter choice (1-9): "))
            print()

            if choice == 1:
                list_movies()
            elif choice == 2:
                add_movie()
            elif choice == 3:
                delete_movie_in_db()
            elif choice == 4:
                update_movie_in_db()
            elif choice == 5:
                movie_stats()
            elif choice == 6:
                random_movie()
            elif choice == 7:
                search_movie()
            elif choice == 8:
                sorted_movies()
            elif choice == 0:
                print("Bye!")
                break
            elif choice > 9:
                print("Only numbers from 0 to 9 possible!")
            elif choice == 9:
                generate_website()


        except ValueError:
            print("Invalid input! Please enter a number from 0 to 9. ")


if __name__ == "__main__":
    main()
