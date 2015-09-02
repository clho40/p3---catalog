from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import database_service
app = Flask(__name__)

@app.route('/')
def IndexPage():
    catagories = database_service.GetAllCatagory()
    return render_template('index.html',catagories=catagories)

@app.route('/catagory/new', methods=['GET','POST'])
def newCatagory():
    catagories = database_service.GetAllCatagory()
    if request.method == 'POST':
        database_service.NewCatagory(request.form['name'],request.form['desc'])
        flash('New catagory created!')
        return redirect(url_for('newCatagory',catagories=catagories))
    else:
        return render_template('newcatagory.html',catagories=catagories)

@app.route('/catagory/<int:cid>/edit', methods=['GET','POST'])
def editCatagory(cid):
    catagories = database_service.GetAllCatagory()
    if request.method == 'POST':
        database_service.EditCatagory(cid,request.form['name'],request.form['desc'])
        flash('Catagory updated!')
        return redirect(url_for('showProducts',cid=cid))
    else:
        sel_catagory = database_service.GetCatagoryByID(cid)
        return render_template('editcatagory.html',catagories=catagories,sel_catagory=sel_catagory)

@app.route('/catagory/<int:cid>/delete')
def deleteCatagory(cid):
    catagories = database_service.GetAllCatagory()
    if request.method == 'POST':
        database_service.DeleteCatagory(cid)
        flash('Catagory deleted!')
        return redirect(url_for('IndexPage'))
    else:
        sel_catagory = database_service.GetCatagoryByID(cid)
        return render_template('deletecatagory.html',catagories=catagories,sel_catagory=sel_catagory)

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
