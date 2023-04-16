class Hint:

    def __init__(self, answer):

        hints = []

        # GIVE GENRE
        for item in answer['genres']:
            genres = ""
            idx = answer['genres'].index(item)
            if len(answer['genres']) == 1:
                genres += f'{item}'
            elif idx < len(answer['genres']) - 1:
                genres += f'{item}, '
            else:
                genres += f'and {item}.'
        hints.append(f"First Hint: The genre of the answer is: {genres}")

        # GIVE SIMILAR MOVIES
        similar_movies = ""
        for item in answer['similar_movie']:
            idx = answer['similar_movie'].index(item)
            if idx < len(answer['similar_movie']) - 1:
                similar_movies += f'{item}, '
            else:
                if item[-1] == "!" or item[-1] == "?":
                    similar_movies += f'and {item}'
                else:
                    similar_movies += f'and {item}.'
            hints.append(f"Second Hint: Some similar movies to the answer are {similar_movies}")

        # GIVE TAGLINE
        hints.append(f"Third Hint: The tagline of the answer is {answer['tagline'][0]}")