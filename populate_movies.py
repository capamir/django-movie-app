import requests
import random
import json

# API base URL
BASE_URL = "http://127.0.0.1:8000/api"

# Authentication credentials (replace with your superuser credentials)
USERNAME = "admin"
PASSWORD = "admin123"

# Sample data for genres and actors
GENRES = [
    "Action", "Drama", "Comedy", "Sci-Fi", "Horror", "Romance", "Thriller",
    "Adventure", "Fantasy", "Mystery", "Crime", "Animation", "Biography"
]
ACTORS = [
    "Leonardo DiCaprio", "Meryl Streep", "Brad Pitt", "Scarlett Johansson",
    "Denzel Washington", "Tom Hanks", "Natalie Portman", "Robert Downey Jr.",
    "Jennifer Lawrence", "Chris Hemsworth", "Margot Robbie", "Will Smith",
    "Viola Davis", "Johnny Depp", "Emma Stone"
]

# Sample movie titles and plot summaries (for simplicity, we'll generate variations)
MOVIE_TITLES = [
    "The Shadow Realm", "Echoes of Time", "Starlight Chronicles", "Midnight Run",
    "Lost Horizon", "The Silent Storm", "Cosmic Voyage", "Eternal Flame",
    "City of Ghosts", "The Last Frontier"
]
PLOT_SUMMARY = "In a {genre} tale, a {character} embarks on a journey to {goal}, facing {challenge} along the way."

# Helper function to get JWT token
def get_jwt_token():
    url = f"{BASE_URL}/users/login/"
    payload = {"username": USERNAME, "password": PASSWORD}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get("access")
    else:
        raise Exception(f"Login failed: {response.text}")

# Helper function to create genres
def create_genres(token):
    url = f"{BASE_URL}/movies/genres/"
    headers = {"Authorization": f"Bearer {token}"}
    genre_ids = {}
    for genre in GENRES:
        response = requests.post(url, json={"name": genre}, headers=headers)
        if response.status_code == 201:
            genre_ids[genre] = response.json().get("id")
        else:
            print(f"Failed to create genre {genre}: {response.text}")
    return genre_ids

# Helper function to create actors
def create_actors(token):
    url = f"{BASE_URL}/movies/actors/"
    headers = {"Authorization": f"Bearer {token}"}
    actor_ids = {}
    for actor in ACTORS:
        response = requests.post(url, json={"name": actor}, headers=headers)
        if response.status_code == 201:
            actor_ids[actor] = response.json().get("id")
        else:
            print(f"Failed to create actor {actor}: {response.text}")
    return actor_ids

# Helper function to create movies
def create_movies(token, genre_ids, actor_ids):
    url = f"{BASE_URL}/movies/"
    headers = {"Authorization": f"Bearer {token}"}
    for i in range(100):
        title = f"{random.choice(MOVIE_TITLES)} {i + 1}" if i >= len(MOVIE_TITLES) else MOVIE_TITLES[i]
        genre_names = random.sample(GENRES, random.randint(1, 3))
        genre_ids_list = [genre_ids[name] for name in genre_names if name in genre_ids]
        actor_names = random.sample(ACTORS, random.randint(2, 5))
        actor_ids_list = [actor_ids[name] for name in actor_names if name in actor_ids]
        rating = round(random.uniform(0.5, 5.0), 1)
        plot = PLOT_SUMMARY.format(
            genre=genre_names[0].lower(),
            character="hero" if random.choice([True, False]) else "group",
            goal="save the world" if random.choice([True, False]) else "uncover a secret",
            challenge="unexpected dangers" if random.choice([True, False]) else "formidable enemies"
        )

        payload = {
            "title": title,
            "plot_summary": plot,
            "rating": rating,
            "genres": genre_ids_list,
            "actors": actor_ids_list
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            print(f"Created movie: {title}")
        else:
            print(f"Failed to create movie {title}: {response.text}")

# Main function
def main():
    try:
        # Get JWT token
        token = get_jwt_token()
        print("Authenticated successfully")

        # Create genres
        genre_ids = create_genres(token)
        print(f"Created {len(genre_ids)} genres")

        # Create actors
        actor_ids = create_actors(token)
        print(f"Created {len(actor_ids)} actors")

        # Create movies
        create_movies(token, genre_ids, actor_ids)
        print("Finished creating 100 movies")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()