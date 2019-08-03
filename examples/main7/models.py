import asyncio
from enum import Enum

from gino import Gino
from sqlalchemy_utils import ChoiceType

run = asyncio.get_event_loop().run_until_complete

db = Gino()

# create instance
# create with not null and defaults
# required args and kv
# positional and kv
# spread operator
# class vs objects functions
# create with class method
# create with children
# create enums
# choice type


run(db.set_bind('postgresql://fastapieguser:secret@localhost/fastapieg'))

class Gender(Enum):
    Male = "M"
    Female = "F"

class User(db.Model):
     __tablename__ = "users"
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String)
     age = db.Column(db.Integer, nullable=False, default=50)
     gender = db.Column(ChoiceType(Gender))


class Contribution(db.Model):
    __tablename__ = "contribution"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))


user = User()
user.username = "foo"
user.age = 30
user.gender = Gender.Female
run(user.create())

#run(Contribution.create(name="nick", amount=5, user_id=4))



#
#run(db.gino.create_all())
#
# user1 = User()
# user1.username = "another bob"
# run(user1.create())




#run(db.gino.create_all())

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String)
#     age = db.Column(db.Integer)
#     gender = db.Column(db.String)
#
# run(db.set_bind('postgresql://fastapieguser:secret@localhost/fastapieg'))
# run(db.gino.create_all())
#
#
# user = User()
# user.username = "bart"
#
# run(user.create())
#run(db.gino.create_all())

#do nullable=False
#do default=
#do unique

#user = run(User.create(username="Larry", age=22, gender="M"))
# @classmethod
# def create(cls, username, age, gender):
#     user = User()
#     user.username = username
#     user.age = age
#     user.gender = gender

#1
# def print_user(name, age=0, gender="F"):
#     print(f'User {name} is a {age} year old {gender}')

# user_dict = {
#     "age": 33,
#     "gender": "M",
#     "name": "Bernie"
# }

#print_user(**user_dict)

#5 switch around props
#print_user(**user_dict)

#6 switch around vals
#val_list = ["Bernie", "Ambiguous", 37]
#print_user(*val_list)






# class Gender(Enum):
#     Male = "M"
#     Female = "F"
# ChoiceType(Gender)
