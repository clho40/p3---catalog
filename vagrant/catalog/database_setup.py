########## Header ##########
import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()
############################

########## Body ##########
class Catagory(Base):
    __tablename__ = 'catagory'
    id = Column(Integer,primary_key = True)
    name = Column(String(250),nullable=False)
    description = Column(String(250))
    updated_on = Column(DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    updated_by = Column(String(250),nullable=True)
    created_on = Column(DateTime,default=datetime.datetime.now())
    created_by = Column(String(250),nullable=True)
    
    @property
    def serialize(self):
        return {
            'id'            : self.id,
            'name'          : self.name,
            }
    
class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer,primary_key = True)
    name = Column(String(100),nullable=False)
    description = Column(String(250))
    price = Column(String(10))
    flavour = Column(String(250))
    catagory_id = Column(Integer,ForeignKey('catagory.id'))
    catagory = relationship(Catagory)
    updated_on = Column(DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    updated_by = Column(String(250),nullable=True)
    created_on = Column(DateTime,default=datetime.datetime.now())
    created_by = Column(String(250),nullable=True)

    @property
    def serialize(self):
        return {
            'id'            : self.id,
            'name'          : self.name,
            'description'   : self.description,
            'price'         : self.price,
            'flavour'       : self.flavour,
            }
    
############################

########## Footer ##########
engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
############################
