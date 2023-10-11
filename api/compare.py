def compare_crew(crew_type, guess, answer):
    crew_feedback = []
    number = [len(answer[crew_type]), len(guess[crew_type])]
    common_members = []
    if max(number) == len(answer[crew_type]):
        for crew in answer[crew_type]:
            if crew in guess[crew_type]:
                common_members.append(crew)
    else:
        for crew in guess[crew_type]:
            if crew in answer[crew_type]:
                common_members.append(crew)
    if len(common_members) > 0:
        for i in range(len(common_members)):
            if crew_type == "studio":
                crew_feedback.append(f"One of the studios that made the answer, {common_members[i]}, "
                                     f"also made '{guess['title']}'.")
            if crew_type == "actor":
                crew_feedback.append(
                    f"One of the actors that appeared in the answer, {common_members[i]}, "
                    f"also appeared in '{guess['title']}'.")
            elif crew_type == "director":
                crew_feedback.append(f"The director of the answer, {common_members[i]}, "
                                     f"also directed '{guess['title']}'.")
            elif crew_type == "writer":
                crew_feedback.append(f"The writer of the answer, {common_members[i]}, also wrote '{guess['title']}'.")
    return crew_feedback


class Compare:

    def __init__(self, guess, answer):
        self.feedback = {
            "answered": [],
            "release_year": [],
            "studio": [],
            "actor": [],
            "director": [],
            "writer": [],
            "year_info": {"Before": "", "After": "", "Released": ""}
        }
        self.movie_is_guessed = False

        # CHECK WHETHER GUESS IS THE MOVIE
        if int(answer['id']) == int(guess['id']):
            self.feedback["answered"].append(f"You guessed the movie! The correct movie is {answer['title']}.")
            self.movie_is_guessed = True
        else:
            self.feedback["answered"].append("Hmm, that's not it...")

            # CHECK WHETHER GUESS HAS THE SAME RELEASE YEAR AS THE ANSWER
            if answer['release_year'] == guess['release_year']:
                self.feedback['release_year'].append(f"The release year of the answer is the same as as the release "
                                                     f"year of '{guess['title']}.'")
                self.feedback['year_info']['Released'] = guess['release_year']
            if answer['release_year'] > guess['release_year']:
                self.feedback['release_year'].append(f"The answer was released after '{guess['title']}.'")
                self.feedback['year_info']['After'] = guess['release_year']
            if answer['release_year'] < guess['release_year']:
                self.feedback['release_year'].append(f"The answer was released before '{guess['title']}.'")
                self.feedback['year_info']['Before'] = guess['release_year']

            # CHECK WHETHER ANY STUDIOS ARE THE SAME
            for item in compare_crew("studio", guess, answer):
                self.feedback['studio'].append(item)

            # CHECK WHETHER ANY CAST MEMBERS ARE THE SAME
            for item in compare_crew("actor", guess, answer):
                self.feedback['actor'].append(item)

            # CHECK WHETHER DIRECTOR IS THE SAME
            for item in compare_crew("director", guess, answer):
                self.feedback['director'].append(item)

            # CHECK WHETHER WRITER IS THE SAME
            for item in compare_crew("writer", guess, answer):
                self.feedback["writer"].append(item)

            if self.feedback["actor"] == [] and self.feedback["studio"] == [] and self.feedback["director"] == [] \
                    and self.feedback["writer"] == []:
                self.feedback["no_common_items"] = ["None of the top-billed cast, directors, writers, or studios of "
                                                    "the answer are associated with your guess."]
                