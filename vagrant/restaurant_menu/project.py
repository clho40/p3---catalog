from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import database_service
app = Flask(__name__)

@app.route('/')
@app.route('/restaurants/<int:rid>/menu/')
def restaurantMenu(rid):
    rest = database_service.GetRestaurant(rid)
    menu = database_service.GetMenuItemByRestaurant(rid)
    return render_template('menu.html',restaurant=rest, menu=menu)

@app.route('/restaurants/<int:rid>/menu/new/', methods=['GET','POST'])
def newMenuItem(rid):
    if request.method == 'POST':
        database_service.NewMenuItem(rid,request.form['name'],request.form['desc'],request.form['price'],request.form['course'])
        flash('New menu item created!')
        return redirect(url_for('restaurantMenu',rid=rid))
    else:
        return render_template('newmenuitem.html',rid=rid)

@app.route('/restaurants/<int:rid>/menu/<int:mid>/edit/', methods=['GET','POST'])
def editMenuItem(rid,mid):
    if request.method == 'POST':
        database_service.EditMenuItem(mid,request.form['name'],request.form['desc'],request.form['price'],request.form['course'],rid)
        flash('Menu item updated!')
        return redirect(url_for('restaurantMenu',rid=rid))
    else:
        item = database_service.GetMenuItem(mid)
        return render_template('editmenuitem.html',rid=rid,item=item,)

@app.route('/restaurants/<int:rid>/menu/<int:mid>/delete/', methods=['GET','POST'])
def deleteMenuItem(rid,mid):
    if request.method == 'POST':
        database_service.DelMenuItem(mid)
        flash('Menu item deleted!')
        return redirect(url_for('restaurantMenu',rid=rid))
    else:
        item = database_service.GetMenuItem(mid)
        return render_template('deletemenuitem.html',rid=rid,item=item)

#Making an API Endpoint (GET Request)
@app.route('/restaurants/<int:rid>/menu/JSON')
def restaurantMenuJSON(rid):
    rest = database_service.GetRestaurant(rid)
    menu = database_service.GetMenuItemByRestaurant(rid)
    return jsonify(MenuItem=[i.serialize for i in menu])

@app.route('/restaurants/<int:rid>/menu/<int:mid>/JSON')
def MenuItemJSON(rid,mid):
    item = database_service.GetMenuItem(mid)
    return jsonify(MenuItem=item.serialize)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
