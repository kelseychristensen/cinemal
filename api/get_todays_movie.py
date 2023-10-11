from datetime import datetime
from generate_movie import GenerateMovie
import requests
import os

class GetTodaysMovie:

    def __init__(self):
        self.today = datetime.now().strftime("%m-%d-%Y")
        self.api_key = os.environ["API_KEY"]

        with open("last_date.txt", mode="r") as file:
            last_date = file.read()

        if self.today != last_date:
            movie = GenerateMovie()
            movie.get_movie()

        with open("last_date.txt", mode="w") as file:
            file.write(self.today)

        with open("todays_movie.txt", mode="r") as file:
            self.todays_movie_id = file.read()

        self.endpoint = f"https://api.themoviedb.org/3/movie/{self.todays_movie_id}"
        self.response = requests.get(url=self.endpoint, params={"api_key": self.api_key})
        self.movie = self.response.json()

        self.credits_endpoint = f"{self.endpoint}/credits"
        self.creds_response = requests.get(url=self.credits_endpoint, params={"api_key": self.api_key})
        self.creds = self.creds_response.json()

        self.similar_movie_endpoint = f"{self.endpoint}/similar"
        self.similar_movie_response = requests.get(url=self.similar_movie_endpoint, params={"api_key": self.api_key})
        self.similar_movie = self.similar_movie_response.json()['results']
        self.movie_details = {
            "id": self.movie['id'],
            "title": self.movie['title'],
            "release_year": self.movie['release_date'].split("-")[0],
            "genres": [genre['name'] for genre in self.movie['genres']],
            "tagline": [self.movie['tagline']],
            "similar_movie": [movie['title'] for movie in self.similar_movie[:3]],
            "studio": [company['name'] for company in self.movie['production_companies']],
            "actor": [actor['name'] for actor in self.creds['cast']],
            "director": [crew_member['name'] for crew_member in self.creds['crew'] if crew_member['job'] == "Director"],
            "writer": [crew_member['name'] for crew_member in self.creds['crew'] if crew_member['job'] == "Screenplay"],
        }

