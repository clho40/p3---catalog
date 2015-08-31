from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def NewRestaurant(restaurant_name):
    new_restaurant = Restaurant(name = restaurant_name)
    session.add(new_restaurant)
    session.commit()

def GetRestaurant(rid):
    item = session.query(Restaurant).filter_by(id=rid).one()
    return item

def GetAllRestaurant():
    item = session.query(Restaurant).all()
    return item

def EditRestaurant(restaurant_id,update_name):
    rest = session.query(Restaurant).filter_by(id=restaurant_id).one()
    rest.name = update_name
    session.add(rest)
    session.commit()

def DelRestaurant(restaurant_id):
    rest = session.query(Restaurant).filter_by(id=restaurant_id).one()
    session.delete(rest)
    session.commit()

def NewMenuItem(rid,item_name,desc,n_price,n_course):
    new_item = MenuItem(name = item_name,restaurant_id=rid,description=desc, price=n_price, course=n_course)
    session.add(new_item)
    session.commit()

def GetMenuItemByRestaurant(rid):
    item = session.query(MenuItem).filter_by(restaurant_id=rid).all()
    return item

def GetMenuItem(mid):
    item = session.query(MenuItem).filter_by(id=mid).one()
    return item

def EditMenuItem(menuitem_id,update_name,update_desc,update_price,update_course,rest_id):
    item = session.query(MenuItem).filter_by(id=menuitem_id).one()
    item.name = update_name
    item.description = update_desc
    item.price = update_price
    item.course = update_course
    item.restaurant_id=rest_id
    session.add(item)
    session.commit()

def DelMenuItem(menuitem_id):
    item = session.query(MenuItem).filter_by(id=menuitem_id).one()
    session.delete(item)
    session.commit()
