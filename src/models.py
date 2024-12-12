import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False, unique=True)
    firstname = Column(String(30))
    lastname = Column(String(30))
    email = Column(String, nullable=False, unique=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
        }

class Posts(Base):
    __tablename__ = 'posts'   
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users', back_populates='posts')

class Comments(Base):
    __tablename__ = 'comments'  
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    user = relationship('Users', back_populates='comments')
    post = relationship('Posts', back_populates='comments')

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Posts', back_populates='media')

# Relaciones inversas
Users.posts = relationship('Posts', back_populates='user')
Users.comments = relationship('Comments', back_populates='user')
Posts.comments = relationship('Comments', back_populates='post')
Posts.media = relationship('Media', back_populates='post')

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
