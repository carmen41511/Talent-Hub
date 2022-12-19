"""Models for talent hub."""
# defining the database

from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_ckeditor import CKEditorField



db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_name = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    # should I include the password attribute?
    password = db.Column(db.String)
    interest = db.Column(db.String)
    bio = db.Column(db.String)
    
    # users.skills return the related Skill object
    # should I still include db.relationship for skills? can include or not, or access the information from UserSkills class
    skills = db.relationship("Skill", secondary="user_skills", back_populates="user")
    posts = db.relationship("Post", back_populates="user")

    def __repr__(self):
        return f'<User user_id={self.user_id} user_name={self.user_name} email={self.email} \npassword={self.password} \ninterest={self.interest} \nbio={self.bio}>'


class Skill(db.Model):
    """A bunch of skills."""

    __tablename__ = 'skills'

    skill_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    skill = db.Column(db.String)

    # skills.users return the User object related to the skill
    user = db.relationship("User", secondary="user_skills", back_populates="skills")
    posts = db.relationship("Post", secondary="post_skills", back_populates="skills")

    def __repr__(self):
        return f'<Skills skill_id={self.skill_id} skill={self.skill}>'


class UserSkill(db.Model):
    """A bunch of skills."""

    __tablename__ = 'user_skills'

    user_skill_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey("skills.skill_id"),nullable=False)


    def __repr__(self):
        return f'<UserSkill user_skill_id={self.user_skill_id} user_id={self.user_id} skill_id={self.skill_id}>'


class Post(db.Model):
    """A post."""

    __tablename__ = 'posts'

    post_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    post_date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),nullable=False)
    # email = db.Column(db.String, db.ForeignKey('users.email'), unique=True)
    
    skills = db.relationship("Skill", secondary="post_skills", back_populates="posts")  
    user = db.relationship("User", back_populates="posts", foreign_keys=[user_id])

    def __repr__(self):
        return f'<Post post_id={self.post_id} title={self.title} post_date={self.post_date} \n description={self.description}>'


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = CKEditorField('Content', Validators=[DataRequired()])
    skills = SelectMultipleField("Related Skills", choices=['Customer Service','Sales','Accounting','Businesses Development','Marketing', 'Leadership','Communication', 'Agile Project Management','Web Development','Digital Marketing','Cybersecurity', 'Innovation Management','Digital Marketing','Engineering','SQL'])
    submit = SubmitField("Submit")




class PostSkill(db.Model):
    """association table with Post and Skill"""

    __tablename__ = 'post_skills'

    post_skill_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'),nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.skill_id'),nullable=False)

    def __repr__(self):
        return f'<PostSkill post_skill_id={self.post_skill_id} post_id={self.post_id} skill_id={self.skill_id}>'



def connect_to_db(flask_app, db_uri="postgresql:///talents", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)