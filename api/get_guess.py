import requests
import os

class GetGuessedMovie:

    def __init__(self, guess):

        # API CALL TO SEARCH USERS INPUT
        self.api_key = os.environ["API_KEY"]
        self.endpoint = "https://api.themoviedb.org/3/search/movie"
        self.response = requests.get(url=self.endpoint, params={"api_key": self.api_key, "query": guess})
        self.results = self.response.json()['results']

        # ESTABLISHING VARIABLES USED IN GET GUESS FUNCTION BELOW
        self.new_response = ""
        self.movie_details = ""
        self.creds = ""
        self.creds_response = ""
        self.credits_endpoint = ""
        self.movie = ""
        self.new_endpoint = ""
        self.correct_movie = ""

        # CREATE LIST OF RESULTS TO MAKE SURE USERS INPUT IS CORRECT MOVIE TO COMPARE FOR FEEDBACK
        self.options = [[f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}", movie['title'], movie['release_date'].split("-")[0], movie['id']] for movie in self.results]

    def get_guess(self, correct_result_id):

        # COLLECT THE CORRECT MOVIE FROM RESULTS BASED ON USER'S FEEDBACK ON LIST OF RESULTS
        movie_id = correct_result_id

        # API CALL FOR MOVIE USER SELECTED
        self.new_endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}"
        self.new_response = requests.get(url=self.new_endpoint, params={"api_key": self.api_key})
        self.movie = self.new_response.json()

        # API CALL FOR MOVIE CREDITS OF MOVIE USER SELECTED

        self.credits_endpoint = f"{self.new_endpoint}/credits"
        self.creds_response = requests.get(url=self.credits_endpoint, params={"api_key": self.api_key})
        self.creds = self.creds_response.json()
        self.movie_details = {
            "id": movie_id,
            "title": self.correct_movie['title'],
            "release_year": self.correct_movie['release_date'].split("-")[0],
            "studio": [company['name'] for company in self.movie['production_companies']],
            "actor": [actor['name'] for actor in self.creds['cast']],
            "director": [crew_member['name'] for crew_member in self.creds['crew'] if crew_member['job'] == "Director"],
            "writer": [crew_member['name'] for crew_member in self.creds['crew'] if crew_member['job'] == "Screenplay"],
        }
        return self.movie_details
