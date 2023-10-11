from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from get_todays_movie import GetTodaysMovie
from get_guess import GetGuessedMovie
from get_guess_details import GetGuessDetails
from compare import Compare

# TODO: Make it so app will generate new movie if ID has been used before
# TODO: Make results shareable
# TODO: Make it so app will detect if user has visited the puzzle for that day
# TODO: Prevent resubmission of form
# TODO: Save user stats

app = Flask(__name__)
Bootstrap(app)

# TODAY'S MOVIE

answer = GetTodaysMovie()
answer_details = answer.movie_details
guesses_made = 0
guesses_list = []
game_on = True
actors_identified = []
directors_identified = []
release_year = {'Before': '', 'After': '', 'Released': ''}
writers_identified = []
studios_identified = []


def save_historic_feedback(dict_name):
    global actors_identified, directors_identified, release_year, writers_identified, studios_identified
    for item in dict_name['actor']:
        if item.split(',')[1] not in actors_identified:
            actors_identified.append(item.split(',')[1])
    for item in dict_name['director']:
        if item.split(',')[1] not in directors_identified:
            directors_identified.append(item.split(',')[1])
    for item in dict_name['writer']:
        if item.split(',')[1] not in writers_identified:
            writers_identified.append(item.split(',')[1])
    for item in dict_name['studio']:
        if item.split(',')[1] not in studios_identified:
            studios_identified.append(item.split(',')[1])
    for item in dict_name['year_info']:
        if dict_name['year_info'][item] != '':
            if item == 'Before':
                if release_year['Before'] == '' or dict_name['year_info'][item] < release_year['Before']:
                    release_year['Before'] = dict_name['year_info'][item]
            if item == "After":
                if release_year['After'] == '' or dict_name['year_info'][item] > release_year['After']:
                    release_year['After'] = dict_name['year_info'][item]
            if item == "Released":
                if release_year['Released'] == '':
                    release_year['Released'] = dict_name['year_info'][item]


@app.route("/", methods=["GET", "POST"])
def home():
    # GETTING FIRST GUESS
    global guesses_made, guesses_list, game_on
    text = 'Guess a movie!'
    feedback = []
    if request.method == 'POST':
        text = 'Did you mean...'
        user_input = request.values.get('guess')
        guess = GetGuessedMovie(user_input)
        options = guess.options
        options_exist = True
        if len(options) == 0:
            text = 'Hmm... there were no results for that search. Please try again.'
        guesses_made += 1
        return render_template('index.html', guess=guess, text=text, options=options, options_exist=options_exist,
                               game_on=game_on, guesses_made=guesses_made, release_year=release_year,
                               feedback_len=len(feedback))

    return render_template('index.html', text=text, game_on=game_on, guesses_made=guesses_made,
                           release_year=release_year, feedback_len=len(feedback))


@app.route("/<correct_result>", methods=['GET', 'POST'])
def result(correct_result):
    global guesses_made, guesses_list, game_on, actors_identified, directors_identified, \
        writers_identified, studios_identified, release_year
    text = 'Guess a movie!'
    guess = GetGuessDetails(correct_result)
    if f"Guess #{guesses_made}: {guess.movie_details['title']}" not in guesses_list:
        guesses_list.append(f"Guess #{guesses_made}: {guess.movie_details['title']}")
    comparison = Compare(guess.movie_details, answer_details)
    feedback = comparison.feedback
    save_historic_feedback(feedback)

    if comparison.movie_is_guessed:
        game_on = False
    if request.method == 'POST':
        text = 'Did you mean...'
        user_input = request.values.get('guess')
        guess = GetGuessedMovie(user_input)
        options = guess.options
        options_exist = True
        if len(options) == 0:
            text = 'Hmm... there were no results for that search. Please try again.'
        guesses_made += 1
        return render_template('index.html', guesses_list=guesses_list, guess=guess, text=text, options=options,
                               options_exist=options_exist, feedback=feedback, feedback_len=len(feedback),
                               game_on=game_on, guesses_made=guesses_made, actors_identified=actors_identified,
                               directors_identified=directors_identified, release_year=release_year,
                               writers_identified=writers_identified, studios_identified=studios_identified)
    return render_template('index.html', guesses_list=guesses_list,  text=text, feedback=feedback, game_on=game_on,
                           guesses_made=guesses_made, feedback_len=len(feedback), actors_identified=actors_identified,
                           directors_identified=directors_identified, release_year=release_year,
                           writers_identified=writers_identified, studios_identified=studios_identified)


@app.route("/how-to-play")
def how_to():
    # GIVE HOW-TO-PLAY DIRECTIONS
    return render_template('how_to.html')


if __name__ == '__main__':
    app.run(debug=True)
