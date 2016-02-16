from flask import render_template, request, flash, redirect, url_for
from app import app
from models import Player, Tournament, Game
from forms import ChooseTournament, CreateTournament, AddPlayers, RoundResults
from datetime import date
import sys


#PLAYERS = []
PLAYERS= [('John', 'john@gmail.com'), ('Bob', 'bob@gmail.com')]

@app.route('/', methods = ['GET', 'POST'])
def home():
	# page 1
	form = ChooseTournament(request.form)
		
	if request.method == 'POST':
		if request.form['choice'] == 'create':	
			return redirect(url_for("create_tournament"))

		elif request.form['choice'] == 'load':
			# go to load pages and pull in all tournament entries from the database
			flash("Let's load it up")
			return redirect(url_for("load_tournament"))

	return render_template('index.html', form=form, title="Choose")


@app.route('/load_tournament', methods = ['GET', 'POST'])
def load_tournament():
	# page 2
	# connect to database and list all tournaments by name
	#tourns = Tournament.query.all()
	tourns = {'January':[], 'february':[]}
	return render_template('load_tournament.html', tourns=tourns)
	# submit button load 



@app.route('/create_tournament', methods = ['GET','POST'])
def create_tournament():
	# page 3
    form = CreateTournament(request.form)
    if request.method == 'POST' and form.validate_on_submit():
    	return redirect(url_for('add_players'))
    	# pull tournamentID from db and redirect to proper page
    	# return redirect('/<tournamentID>/add_players')

    #if request.method == 'POST' and form.validate():
    return render_template('create_tournament.html', title='Home',form=form)



#@app.route('/<tournamentID>/add_players', methods = ['GET', 'POST'])
@app.route('/add_players', methods = ['GET', 'POST'])
def add_players():
	form = AddPlayers(request.form)
	if request.method == 'POST':
		if request.form['send'] == 'Add player':
			new = (request.form['name'], request.form['email'])
			PLAYERS.append(new)

		elif request.form['send'] == 'Start playing':
			return redirect(url_for("round"))

	return render_template('add_players.html',form=form, PLAYERS=PLAYERS)
	


#@app.route('/<tournamentID>/<round_c>', methods = ['GET', 'POST'])
# <round_c> will be passed in as variable
@app.route('/round', methods = ['GET', 'POST'])
def round():
	"""gets the round number, PLAYERS' names and round match schedule, pass it into the rendered template 

	make a template to enter results and proceed to the next round """

	round_c = 4 # take from the database
	players = ['bob', 'john', 'colin', 'adam', 'ana', 'petr'] # need a list of names, where opponents are 2 
	# a global number of games per round, that will be calculated for each tournament 
	NUM_GAMES = len(players)

	if request.method == 'POST':
		return redirect(url_for("standings"))

	return render_template('round.html', round_c=round_c, NUM_GAMES=NUM_GAMES, players=players)
    	

# pass tournament ID and round counter into the path
#@app.route('/<tournamentID>/<round_c>/standings', methods = ['GET', 'POST'])

@app.route('/standings', methods = ['GET', 'POST'])
def standings():
	round_c = 4 # take from the database
	NUM_ROUNDS = 5
	if request.method == 'POST':
		if request.form['button'] == "Final result":
			return redirect(url_for('final'))
	return render_template('standings.html', round_c=round_c, NUM_ROUNDS=NUM_ROUNDS, PLAYERS=PLAYERS)


@app.route('/final_results', methods = ['GET', 'POST'])
def final_results():
	if request.method == 'POST':
		# send email to all participants with final standings and round results 
		pass


	return render_template('final_results.html')
