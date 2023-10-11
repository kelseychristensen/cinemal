import requests
import os

class GetGuessDetails:

    def __init__(self, guess_id):
        # COLLECT THE CORRECT MOVIE FROM RESULTS BASED ON USER'S FEEDBACK ON LIST OF RESULTS
        self.movie_id = guess_id
        self.api_key = os.environ["API_KEY"]

        # API CALL FOR MOVIE USER SELECTED
        self.new_endpoint = f"https://api.themoviedb.org/3/movie/{self.movie_id}"
        self.response = requests.get(url=self.new_endpoint, params={"api_key": self.api_key})
        self.movie = self.response.json()

        # API CALL FOR MOVIE CREDITS OF MOVIE USER SELECTED

        self.credits_endpoint = f"{self.new_endpoint}/credits"
        self.creds_response = requests.get(url=self.credits_endpoint, params={"api_key": self.api_key})
        self.creds = self.creds_response.json()
        directors = [crew_member['name'] for crew_member in self.creds['crew'] if crew_member['job'] == "Director"]
        self.movie_details = {
            "id": self.movie_id,
            "title": self.movie['title'],
            "release_year": self.movie['release_date'].split("-")[0],
            "studio": [company['name'] for company in self.movie['production_companies']],
            "actor": [actor['name'] for actor in self.creds['cast']],
            "director": [crew_member['name'] for crew_member in self.creds['crew'] if crew_member['job'] == "Director"],
            "writer": [crew_member['name'] for crew_member in self.creds['crew'] if crew_member['job'] == "Screenplay"],
        }


