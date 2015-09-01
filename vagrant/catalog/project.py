from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import database_service
app = Flask(__name__)

@app.route('/')
def IndexPage():
    catagories = database_service.GetAllCatagory()
    return render_template('index.html',catagories=catagories)

@app.route('/catagory/<int:cid>')
def showProducts(cid):
    catagories = database_service.GetAllCatagory()
    sel_catagory = database_service.GetCatagoryByID(cid)
    products = database_service.GetProductByCatagory(cid)
    return render_template('products.html',catagories=catagories,sel_catagory=sel_catagory, products=products)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
