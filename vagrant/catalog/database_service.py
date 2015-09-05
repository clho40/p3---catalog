from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Catagory,Product,User
import os
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def NewCatagory(c_name,c_desc,c_user_id):
    item = Catagory(name = c_name,description=c_desc,user_id=c_user_id)
    session.add(item)
    session.commit()

def GetCatagoryByID(cid):
    item = session.query(Catagory).filter_by(id=cid).one()
    return item

def GetAllCatagory():
    item = session.query(Catagory).all()
    return item

def EditCatagory(cid,c_name,c_desc):
    item = session.query(Catagory).filter_by(id=cid).one()
    item.name = c_name
    item.description = c_desc
    session.add(item)
    session.commit()

def DeleteCatagory(cid):
    item = session.query(Catagory).filter_by(id=cid).one()
    session.delete(item)
    session.commit()

def NewProduct(p_name,p_desc,p_price,p_flavour,p_path,cid,c_user_id):
    item = Product(name = p_name,description=p_desc, price=p_price, flavour=p_flavour,image=p_path,catagory_id=cid,user_id=c_user_id)
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
    os.remove(item.image)
    session.delete(item)
    session.commit()

def CreateUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def GetUserInfobyID(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def GetUserIDbyEmail(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

def CheckUserExist(login_session):
    user_id = GetUserIDbyEmail(login_session['email'])
    if not user_id:
        user_id = CreateUser(login_session)
    return user_id

def hasCatagoryPermission(cid,c_user_id):
    catagory = session.query(Catagory).filter_by(id=cid).one()
    if catagory.user_id == c_user_id:
        return True
    else:
        return False

def hasProductPermission(pid,p_user_id):
    product = session.query(Product).filter_by(id=pid).one()
    if product.user_id == p_user_id:
        return True
    else:
        return False
    
    
                   
