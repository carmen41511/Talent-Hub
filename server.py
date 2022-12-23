from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db, db, User,Skill, UserSkill, Post, PostSkill
from jinja2 import StrictUndefined
import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route("/users")
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("all_users.html", users=users)

@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)

# @app.route("/edit-bio")
# def show_bio_modal():
#     """Show modal for editing About Me"""

#     # get the current user's username from the session
#     username = session.get("username")

#     # get the user object for the current user
#     user = crud.get_user_by_username(username)

#     #  what template should I render?
#     return render_template("edit_bio_modal.html", user=user)

@app.route('/edit-bio', methods=['POST'])
def edit_bio():
    # Get the updated bio from the request
    updated_bio = request.form['bio']
    # updated_bio = request.get_json('bio')

    username = session.get("username")
    user = crud.get_user_by_username(username)

    # Update the user's bio in the database
    user.bio = updated_bio
    db.session.commit()

    # Return a success message
    return jsonify({'success': True})


@app.route('/edit-interest', methods=['POST'])
def edit_interest():
    updated_interest = request.form['interest']
    username = session.get("username")
    user = crud.get_user_by_username(username)
    user.interest = updated_interest
    db.session.commit()

    return jsonify({'success': True})




@app.route('/login', methods=['GET'])
def show_login():
    """Show Login Page"""

    return render_template("login.html")

@app.route('/login', methods=['POST'])
def handle_login():
    """Log in user"""

    username = request.form.get('username')
    password = request.form.get('password')

    user = crud.get_user_by_username(username)

    if not user or user.password != password:
        print(f"username:{user}")
        flash("The username or password you entered was incorrect.")
    else:
        # log in user by storing the username in session
        session["username"] = user.username
        flash(f"Welcome back, {user.username}")
        
    # may change redirect route to community page later
    return redirect('/profile')

@app.route('/signup', methods=['GET'])
def show_signup():
    """Show Sign Up Page"""

    return render_template("signup.html")

@app.route('/signup', methods=['POST'])
def handle_signup():
    """Sign Up User"""

    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    interest = request.form.get('interest')
    bio = request.form.get('bio')

    # check if a user with the username from request.form already exists.
    user = crud.get_user_by_username(username)
    print(f"user: {user}")

    if user:
        flash("Username already exist. Please try again.")
        return render_template('signup.html')
    else:
        user = crud.create_user(username, email, password, interest, bio)
        db.session.add(user)
        db.session.commit()
        flash("Account created. Please log in.")
    
    return redirect('/')



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
    else:
        flash("Please enter all information.")


@app.route('/detail')
def show_detail():
    """Show detail page of a post"""

    return render_template('detail.html')


@app.route('/profile')
def show_profile():
    """View user profile page."""

    # get the current user's username from the session
    username = session.get("username")

    # get the user object for the current user
    user = crud.get_user_by_username(username)

    return render_template('profile.html', user=user)



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
