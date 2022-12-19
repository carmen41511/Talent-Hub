from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/add_post', methods=["GET"])
def show_add_post():
    """Show add post page"""

    return render_template('add_post.html')


@app.route('/add_post', methods=["POST"])
def add_post():
    """Add a post.
        Maybe look up the user based on who's currently creating the form
       Need to store the post information to the user account
    """

    title = request.form.get("title")
    skills = request.form.get("skills")
    description = request.form.get("description")

    if title and skills and description:
        return redirect('/detail')


@app.route('/detail')
def show_detail():
    """Show detail page of a post"""

    return render_template('detail.html')


@app.route('/profile')
def profile():
    """View user profile page."""

    return render_template('profile.html')



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
