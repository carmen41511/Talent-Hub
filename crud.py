"""CRUD operations."""
# interaction with the database

from model import db, User, Skill, UserSkill, Post, PostSkill, connect_to_db
from random import sample


def create_user(username, email, password, interest, bio):
    """Create and return a new user."""

    user = User(username=username, email=email, password=password, interest=interest, bio=bio)

    return user


def create_post(title, post_date, description, user):
    """Create and return a new post."""
    
    print("In create_post", title, description, post_date, user)
    
    post = Post(title=title, description=description, post_date=post_date, user_id=user.user_id)

    
    return post

def create_post_skill(post, skill):

    skill_obj = get_skill_by_id(skill.skill_id)
    if skill_obj is not None:
        # Create the post_skill object
        post_skill = PostSkill(post_id=post.post_id, skill_id=skill.skill_id)
        return post_skill
    else:
        # Return None if the skill_id does not exist in the skills table
        return None

def create_user_skill(user, skill):

    skill_obj = get_skill_by_id(skill.skill_id)

    if skill_obj is not None:
        # Create the user_skill object
        user_skill = UserSkill(user_id=user.user_id, skill_id=skill.skill_id)
        return user_skill
    else:
        # Return None if the skill_id does not exist in the skills table
        return None


def create_skill(skill_id, skill):

    skill = Skill(skill_id=skill_id, skill=skill)

    return skill


def return_skills():
    """return all skills."""

    return Skill.query.all()


def get_user_by_id(user_id):

    return User.query.get(user_id)

def get_user_by_username(username):

    user = User.query.filter(User.username == username).first()
    # print(f"user: {user}")

    return user

def get_users():
    """Return all users."""

    return User.query.all()

def get_posts():
    """Return all posts"""
    
    return Post.query.all()

def read_skills_from_file(filepath):

    skill_dict = {}

    with open(filepath) as file:
        for line in file:
            (skill_id, skill) = line.strip().split("|")
            # print(f"skill_id: {skill_id}")
            # print(f"skill: {skill}")
            skill_dict[skill_id] = Skill(skill_id=skill_id, skill=skill)

    return skill_dict

skill_dict = read_skills_from_file("skills.txt")

def get_skill_by_id(skill_id):

    return skill_dict[skill_id]

def get_all_user_skills(user):

    all_userSkill = [skill for skill in UserSkill.query.all() if skill.user_id == user.user_id]

    return all_userSkill

def delete_all_user_skills(user):
    # Get all of the user's skills
    all_userSkill = [skill for skill in UserSkill.query.all() if skill.user_id == user.user_id]
    # print(f"all_userSkill: {all_userSkill}")

    for skill in all_userSkill:
        db.session.delete(skill)

    db.session.commit()

    return 

if __name__ == '__main__':
    from server import app
    connect_to_db(app)