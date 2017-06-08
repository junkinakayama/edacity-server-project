# -*- coding: utf-8 -*-
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, index=True)
    email = Column(String(250), nullable=False)


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    @property
    def _get_items(self):
        return db.sessionsession(self).query(Item).with_parent(self).filter_by(category_id=id).all()
    items = property(_get_items)

    # Add a property decorator to serialize information from this database
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'Item': self._get_items
        }


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    description = Column(Integer)
    title = Column(Integer)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # Add a property decorator to serialize information from this database
    @property
    def serialize(self):
        return {
            'description': self.description,
            'title': self.title,
            'category_id': self.category_id,
            'user_id': self.user_id,
            'id': self.id
        }

engine = create_engine('sqlite:///itemcatalog.db')


Base.metadata.create_all(engine)
