from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db, db, User,Skill, UserSkill, Post, PostSkill
from jinja2 import StrictUndefined
import crud
import json
from datetime import datetime


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

def get_current_user():
    username = session.get("username")

    if username:
        user = crud.get_user_by_username(username)  
        return user
    else:
        return None


@app.route('/')
def homepage():
    """View homepage."""

    user = get_current_user()

    return render_template('homepage.html', user=user)

    

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


@app.route('/edit-skills', methods=['POST'])
def edit_skills():

    # print(request.form)
    skill_set = request.form.getlist('skills')
    # updated_skills_ls = json.loads(updated_skills)
    print(f"updated_skills: {skill_set}")

    username = session.get("username")
    user = crud.get_user_by_username(username)

    crud.delete_all_user_skills(user)

    for skill_id in skill_set:
        skill_obj = crud.get_skill_by_id(skill_id)
        # print(f'skill_obj: {skill_obj.skill}')

        skill = crud.create_skill(skill_id, skill_obj.skill)
        print(f'skill: {skill}')

        user_skill = crud.create_user_skill(user, skill)
        db.session.add(user_skill)
        db.session.commit()

        print(f'user_skill: {user_skill}')
        print(f'user.skills: {user.skills}')


    return redirect('/profile')
    # return jsonify({'user_skill_ls': user_skill_ls})
    # user.skills = updated_skills
    # print(user.skills)
    # db.session.commit()

    # return jsonify({'skills': updated_skills})

# @app.route('/edit-skills')
# def get_skills():
#   # Get the currently logged-in user
#   username = session.get("username")
#   user = crud.get_user_by_username(username)
#   print(user)

#   skill_set = request.form.getlist('skills')
  
#   print(f'skill_set; {skill_set}')
#   # Get the skills for the user
#   user_skills = user.skills
#   skills = [skill.skill for skill in user_skills]
#   print(f'skills: {skills}')
  
#   # Return the skills as a JSON object
#   return jsonify({'skills': skills})


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

    user = get_current_user()

    return render_template("login.html", user=user)


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

    user = get_current_user()

    return render_template("signup.html", user=user)


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
    # print(f"user: {user}")

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

    username = session.get("username")
    user = crud.get_user_by_username(username)


    return render_template('add_post.html', user=user)


@app.route('/add_post', methods=["POST"])
def add_post():
    """Add a post.
        Maybe look up the user based on who's currently creating the form
       Need to store the post information to the user account
    """

    title = request.form.get("title")
    print(f'title: {title}')

    skill_set = request.form.getlist('skills')
    print(f'skill_set: {skill_set}')
    # skill_set: ['b2b','3d']

    description = request.form.get("description")
    # print(f'description: {description}')

    post_date = datetime.now()
    # print(f'post_date: {post_date}')

    username = session.get("username")
    user = crud.get_user_by_username(username)
    # print(f'user: {user}')

    post = crud.create_post(title, post_date, description, user)
    # post_id
    db.session.add(post)
    db.session.commit()
    print(f'post: {post}')

    for skill_id in skill_set:

        # <Skills skill_id=backend skill=Backend Development>
        skill_obj = crud.get_skill_by_id(skill_id)
        print(skill_obj.skill_id)
        print(f'skill_obj: {skill_obj}')  

        post_skill = crud.create_post_skill(post, skill_obj)
        db.session.add(post_skill)
        db.session.commit()
        print(f'post_skill: {post_skill}')
        
    # if post:
    if title and skill_set and description:
        # db.session.add(post)
        # db.session.commit()
        return redirect('/detail')
    else:
        flash("Please enter all information.")


@app.route('/detail/<post_id>')
def show_detail(post_id):
    """Show detail page of a post
    FROM THE COMMUNITY PAGE, THERE COULD BE A SAME POST_ID
    FROM DIFFERENT USER
    
    """

    user = get_current_user()
    post = crud.get_post_by_id(post_id)
    all_posts = crud.get_all_posts()
    
    return render_template('detail.html', user=user,post=post)


@app.route('/profile')
def show_profile():
    """View user profile page."""

    all_skills = crud.return_skills()

    username = session.get("username")
    user = crud.get_user_by_username(username)

    all_userSkill = crud.get_all_user_skills(user)
    # print(f'all_userSkill: {all_userSkill}')
    # print(f'show_profile() user: {user}')
    # print(f'show_profile() user.skills: {user.skills}')

    return render_template('profile.html', user=user, all_skills=all_skills, all_userSkill=all_userSkill)


@app.route('/community')
def show_community():
    """View community page with all posts"""

    username = session.get("username")
    user = crud.get_user_by_username(username)

    posts = crud.get_posts()


    return render_template('community.html', user=user, posts=posts)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
