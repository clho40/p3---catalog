########## Header ##########
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()
############################

########## Body ##########
class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer,primary_key = True)
    name = Column(String(100),nullable=False)
    
class MenuItem(Base):
    __tablename__ = 'menu_item'
    id = Column(Integer,primary_key = True)
    name = Column(String(100),nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer,ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'id'            : self.id,
            'name'          : self.name,
            'description'   : self.description,
            'price'         : self.price,
            'course'        : self.course,
            }
    
############################

########## Footer ##########
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
############################