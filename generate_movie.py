import requests
import random
import datetime
import os

class GenerateMovie:

    # API CALL TO SEARCH RANDOM PAGE AND RETURN RANDOM RESULT
    # OF ALL ENGLISH-LANGUAGE MOVIES IN THE TOP 2000 MOST POPULAR

    def __init__(self):
        super().__init__( )
        self.api_key = os.environ["API_KEY"]
        self.endpoint = "https://api.themoviedb.org/3/discover/movie"
        self.today = datetime.datetime.now().strftime("%m/%d/%Y")

    def get_movie(self):
        n = random.randint(1, 100)
        result = random.randint(0, 19)
        params = {
            "api_key": self.api_key,
            "sort_by": "popularity.desc",
            "page": n
        }
        response = requests.get(url=self.endpoint, params=params)
        todays_movie = response.json()['results'][result]

        # WRITE SELECTION TO TEXT FILE

        with open("todays_movie.txt", mode="w") as file:
            file.write(str(todays_movie['id']))

        with open("used_ids.txt", mode="a") as file:
            file.write(f"{str(todays_movie['id'])}\n")
