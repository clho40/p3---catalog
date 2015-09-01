from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Catagory,Product
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def NewCatagory(c_name):
    item = Catagory(name = c_name)
    session.add(item)
    session.commit()

def GetCatagoryByID(cid):
    item = session.query(Catagory).filter_by(id=cid).one()
    return item

def GetAllCatagory():
    item = session.query(Catagory).all()
    return item

def EditCatagory(cid,c_name):
    item = session.query(Catagory).filter_by(id=cid).one()
    item.name = c_name
    session.add(item)
    session.commit()

def DeleteCatagory(cid):
    item = session.query(Catagory).filter_by(id=cid).one()
    session.delete(item)
    session.commit()

def NewProduct(p_name,p_desc,p_price,p_flavour,cid):
    item = Product(name = p_name,description=p_desc, price=p_price, flavour=p_flavour,catagory_id=cid)
    session.add(item)
    session.commit()

def GetProductByCatagory(cid):
    item = session.query(Product).filter_by(catagory_id=cid).all()
    return item

def GetProductByID(pid):
    item = session.query(Product).filter_by(id=pid).one()
    return item

def EditProduct(pid,p_name,p_desc,p_price,p_flavour,cid):
    item = session.query(Product).filter_by(id=pid).one()
    item.name = p_name
    item.description = p_desc
    item.price = p_price
    item.flavour = p_flavour
    item.catagory_id=cid
    session.add(item)
    session.commit()

def DeleteProduct(pid):
    item = session.query(Product).filter_by(id=pid).one()
    session.delete(item)
    session.commit()
