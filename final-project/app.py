import os
import imdb
import random

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

moviesDB = imdb.IMDb()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        movie_request = request.form.get("movie")

        if not movie_request:
            return apology("missig movie title", 400)

        movies = moviesDB.search_movie(movie_request)

        if not movies:
            return apology("empty search", 400)

        return render_template("search.html", movies = movies)
    else:
        return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":

        user_id = session["user_id"]

        movie_request = request.form.get("movie_select")

        if not movie_request:
            return apology("missig movie title", 400)

        movie_year = movie_request[movie_request.find('(')+1:movie_request.find(')')]
        movie_title = movie_request[0:movie_request.find('(')-1]

        movie = moviesDB.search_movie(movie_title)

        for i in range(len(movie)):
            if movie_title == movie[i]['title'] and str(movie_year) == str(movie[i]['year']):
                movie_id = movie[i].movieID
                series = moviesDB.get_movie(movie_id)
                movie_genre = series.data['genres']

        if request.form['action'] == "watchlist":

            check = db.execute("SELECT title FROM watchlist WHERE movie_id = ? AND id = ?", movie_id, user_id)

            if check:
                return apology("already in watchlist", 400)

            genres = movie_genre[0]
            db.execute("INSERT INTO watchlist (id, movie_id, title, genre, year) VALUES(?, ?, ?, ?, ?)", user_id, movie_id, movie_title, genres, movie_year)

            flash("Added!")
            return redirect("/")

        elif request.form['action'] == "diary":

            check_watchlist = db.execute("SELECT title FROM watchlist WHERE movie_id = ? AND id = ?", movie_id, user_id)
            check_diary = db.execute("SELECT title FROM diary WHERE movie_id = ? AND id = ?", movie_id, user_id)

            if check_watchlist:
                db.execute("DELETE FROM watchlist WHERE id = ? AND title = ? AND year = ?", user_id, movie_title, movie_year)

            if check_diary:
                db.execute("UPDATE diary SET title = ? WHERE id = ? AND movie_id = ?", movie_title + " (Re-Watched)", user_id, movie_id)
                flash("Added!")
                return redirect("/")

            db.execute("INSERT INTO diary (id, movie_id, title, genre, year) VALUES(?, ?, ?, ?, ?)", user_id, movie_id, movie_title, movie_genre[0], movie_year)

            flash("Added!")
            return redirect("/")

    else:
        return render_template("search.html")


@app.route("/watchlist", methods=["GET", "POST"])
@login_required
def watchlist():

        user_id = session["user_id"]
        list = db.execute("SELECT * FROM watchlist WHERE id = ?", user_id)

        return render_template("watchlist.html", list = list)


@app.route("/diary", methods=["GET", "POST"])
@login_required
def diary():

        user_id = session["user_id"]
        list = db.execute("SELECT * FROM diary WHERE id = ?", user_id)

        return render_template("diary.html", list = list)


@app.route("/rate", methods=["GET", "POST"])
@login_required
def rate():
    user_id = session["user_id"]
    list = db.execute("SELECT * FROM diary WHERE id = ?", user_id)

    if request.method == "POST":
        selected_movie = request.form.get("movie")
        rating_score = request.form.get("score")

        if not selected_movie:
            return apology("missing movie", 400)
        if not rating_score:
            return apology("missing score(s)", 400)
        if int(rating_score) < 1 or int(rating_score) > 10 or not rating_score.isnumeric():
            return apology("invalid rating score", 400)

        movie_year = selected_movie[selected_movie.find('(')+1:selected_movie.find(')')]

        if movie_year == "Re-Watched":
            selected_movie = selected_movie.replace('(Re-Watched)', '')
            movie_year = selected_movie[selected_movie.find('(')+1:selected_movie.find(')')]
            movie_title = selected_movie[0:selected_movie.find('(')-1][:-1]
            movie_id = db.execute("SELECT movie_id FROM diary WHERE year = ? AND title = ? AND id = ?", movie_year, movie_title + " (Re-Watched)", user_id)
        else:
            movie_title = selected_movie[0:selected_movie.find('(')-1]
            movie_id = db.execute("SELECT movie_id FROM diary WHERE year = ? AND title = ? AND id = ?", movie_year, movie_title, user_id)

        rating_score = str(rating_score) + "/10"
        db.execute("UPDATE diary SET rating = ? WHERE id = ? AND movie_id = ?", rating_score, user_id, movie_id[0]["movie_id"])

        flash("Rated!")
        return redirect("/")

    else:
        return render_template("rate.html", list = list)

@app.route("/recommendation", methods=["GET", "POST"])
@login_required
def recommendation():

    user_id = session["user_id"]

    if request.method == "GET":
        db.execute("DELETE FROM recommendation")

        check_watched_movies = db.execute("SELECT COUNT(title) FROM diary WHERE id = ?", user_id)
        check_genres = db.execute("SELECT COUNT(genre) FROM watchlist WHERE id = ? GROUP BY genre", user_id)

        if len(check_watched_movies) < 3 or len(check_genres) < 3:
            search = moviesDB.get_top250_movies()
            #gets 3 random movies from 250-top IMDb dataset
            for i in range(3):
                random_num = random.randint(1,251)
                movie_title = str(search[random_num])
                score = str(search[random_num]['rating'])
                movie_year = str(search[random_num]['year'])
                db.execute("INSERT INTO recommendation (id, rating, title) VALUES (?, ?, ?)", user_id, score, movie_title)

        database = db.execute("SELECT * FROM recommendation WHERE id = ?", user_id)

        return render_template("recommendation.html", database = database)

    else:
        database = db.execute("SELECT * FROM recommendation WHERE id = ?", user_id)

        title_list = database
        for i in range(len(title_list)):
            search = moviesDB.get_top250_movies()
            for j in range(len(search)):
                if title_list[i]["title"] == search[j]['title'] and str(title_list[i]['rating']) == str(search[j]['rating']):
                    movie_id = search[j].movieID
                    movie_year = search[j]['year']
                    series = moviesDB.get_movie(movie_id)
                    movie_title = series.data['title']
                    movie_genre = series.data['genres']
                    genres = movie_genre[0]
                    db.execute("INSERT INTO watchlist (id, movie_id, title, genre, year) VALUES(?, ?, ?, ?, ?)", user_id, movie_id, movie_title, genres, movie_year)

        flash("Added!")
        return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()

    # User reached route via POST (as by clicking a link or via redirect)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted to registration form
        if not username:
            return apology("must provide username")

        if db.execute("SELECT username FROM users WHERE username = ?", username):
            return apology("username is taken")

        # Ensure password was submitted to registration form
        if not password:
            return apology("must provide password")

        # Ensure confirmation password was submitted to registration form
        if not confirmation:
            return apology("must provide password again")

        # Ensure confirmation password and password was equal
        if password != confirmation:
            return apology("must provide same password again")

        hashed_password = generate_password_hash(password)

        # Inserting users data into database called users
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashed_password)

        flash("Registered!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash("Logged In!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():

    if request.method == "POST":
        user_id = session["user_id"]

        password = request.form.get("password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        rows = db.execute("SELECT hash FROM users WHERE id = ?", user_id)

        if not password or not new_password or not confirmation:
            return apology("must provide password", 403)

        if not check_password_hash(rows[0]["hash"], password):
            return apology("wrong password", 403)

        if confirmation != new_password:
            return apology("must provide same password again", 403)

        hashed_password = generate_password_hash(new_password)

        db.execute("UPDATE users SET hash = ? WHERE id = ?", hashed_password, user_id)
        flash("Password Changed!")
        return redirect("/")

    else:
        return render_template("change_password.html")


@app.route("/change_username", methods=["GET", "POST"])
@login_required
def change_username():

    if request.method == "POST":
        user_id = session["user_id"]

        password = request.form.get("password")
        new_username = request.form.get("new_username")
        confirmation = request.form.get("confirmation")

        rows = db.execute("SELECT username FROM users WHERE id = ?", user_id)

        if not password or not new_username or not confirmation:
            return apology("must provide password", 403)

        if not check_password_hash(rows[0]["hash"], password):
            return apology("wrong password", 403)

        if confirmation != new_username:
            return apology("must provide same password again", 403)

        db.execute("UPDATE users SET username = ? WHERE id = ?", new_username, user_id)
        flash("Username Changed!")
        return redirect("/")

    else:
        return render_template("change_username.html")
