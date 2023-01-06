"""Script to seed database."""

import os
import json
from random import choice, sample
from datetime import datetime

import crud
import model
import server

os.system("dropdb talents")
os.system("createdb talents")

model.connect_to_db(server.app)
model.db.create_all()


with open("skills.txt") as file:
    for line in file:
        (skill_id, skill) = line.strip().split("|")
        # print(f"skill_id: {skill_id}")
        # print(f"skill: {skill}")

        new_skill = model.Skill(skill_id=skill_id, skill=skill)

        model.db.session.add(new_skill)


model.db.session.commit()


# with open('data/posts.json') as f:
#     post_data = json.loads(f.read())
    
#     # Create posts, store them in list so we can use them to create fake skills later???
# posts_in_db = []
# for post in post_data:
#     # get the title, description, post_date from the post dictionary.
#     title, description, post_date = (post["title"], post["description"], post["post_date"])

#     # create a post here and append it to posts_in_db
#     db_post = crud.create_post(title, description, post_date)
#     posts_in_db.append(db_post)

# model.db.session.add_all(posts_in_db)
# model.db.session.commit()


# interests = ['running', 'yoga', 'puzzles', 'reading', 'cooking']


# skills = ['Customer Service','Sales','Accounting',
# 'Businesses Development','Marketing', 'Leadership',
# 'Communication', 'Agile Project Management',
# 'Web Development','Digital Marketing','Cybersecurity', 'Innovation Management',
# 'Digital Marketing','Engineering','SQL']


# skill_ls = []
# for skill in skills:
#     skill_ls.append(crud.create_skill(skill))

# for n in range(10):
#     username = f'user{n}'
#     email = f'user{n}@test.com'
#     password = 'test'
#     interest = choice(interests)
#     bio = f'I am user{n}'

#     user = crud.create_user(username, email, password, interest, bio)

#     # each user has 5 posts,each post has 5 skills
#     for i in range(5):
#         # skill_set = sample(skills, 5)
        

#         # model.db.session.add_all(skill_ls)
#         post = crud.create_post(f'title{i}', f'description{i}', datetime.now(), user, sample(skill_ls, 5))
#         model.db.session.add(post)

        

#     model.db.session.add(user)
    

