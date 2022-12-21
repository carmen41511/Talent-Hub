"""CRUD operations."""
# interaction with the database

from model import db, User, Skill, UserSkill, Post, PostSkill, connect_to_db
from random import sample


def create_user(username, email, password, interest, bio):
    """Create and return a new user."""

    user = User(username=username, email=email, password=password, interest=interest, bio=bio)

    return user


def create_post(title, description, post_date, user, skill_set):
    """Create and return a new post."""

    post = Post(title=title, description=description, post_date=post_date, user=user, skills=skill_set)

    return post

def create_skill(skill):

    skill = Skill(skill=skill)

    return skill


def return_skills():
    """return all skills."""

    return Skill.query.all()


def get_user_by_id(user_id):

    return User.query.get(user_id)

def get_user_by_username(username):

    user = User.query.filter(User.username == username).first()
    print(f"user: {user}")

    return user

def get_users():
    """Return all users."""

    return User.query.all()
    


if __name__ == '__main__':
    from server import app
    connect_to_db(app)