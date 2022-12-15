"""CRUD operations."""
# interaction with the database

from model import db, User, Skill, UserSkill, Post, PostSkill, connect_to_db
from random import sample


def create_user(user_name, email, password, interest, bio):
    """Create and return a new user."""

    user = User(user_name=user_name, email=email, password=password, interest=interest, bio=bio)

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

    


if __name__ == '__main__':
    from server import app
    connect_to_db(app)