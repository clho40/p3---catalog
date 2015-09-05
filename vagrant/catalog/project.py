from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask import session as login_session
from flask import make_response
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import random,string
import database_service
import requests
import os
from werkzeug import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

CLIENT_ID = json.loads(open('client_secrets.json','r').read())['web']['client_id']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def CheckUserLoggedIn():
    user_loggedin = False
    if 'username' in login_session:
        user_loggedin = True
    return user_loggedin

def getSessionUsername():
    username = ''
    if CheckUserLoggedIn():
        username = login_session['username']
    return username

def getSessionUserID():
    user_id = ''
    if CheckUserLoggedIn():
        user_id = login_session['user_id']
    return user_id

def getSessionUserPic():
    pic = ''
    if CheckUserLoggedIn():
        pic = login_session['picture']
    return pic

@app.route('/')
def IndexPage():
    catagories = database_service.GetAllCatagory()
    logged_in = CheckUserLoggedIn()
    username = getSessionUsername()
    picture = getSessionUserPic()
    return render_template('index.html',catagories=catagories,logged_in=logged_in,username=username,picture=picture)

@app.route('/catagory/new', methods=['GET','POST'])
def newCatagory():
    logged_in = CheckUserLoggedIn()
    if not logged_in:
        return redirect('/login')
    username = getSessionUsername()
    catagories = database_service.GetAllCatagory()
    picture = getSessionUserPic()
    if request.method == 'POST':
        user_id=getSessionUserID()
        database_service.NewCatagory(request.form['name'],request.form['desc'],user_id)
        flash('New catagory created!','alert-success')
        return redirect(url_for('newCatagory'))
    else:
        return render_template('newcatagory.html',catagories=catagories,logged_in=logged_in,username=username,picture=picture)

@app.route('/catagory/<int:cid>/edit', methods=['GET','POST'])
def editCatagory(cid):
    logged_in = CheckUserLoggedIn()
    if not logged_in:
        return redirect('/login')
    username = getSessionUsername()
    user_id=getSessionUserID()
    catagories = database_service.GetAllCatagory()
    picture = getSessionUserPic()
    if database_service.hasCatagoryPermission(cid,user_id):
        if request.method == 'POST':
            database_service.EditCatagory(cid,request.form['name'],request.form['desc'])
            flash('Catagory updated!','alert-success')
            return redirect(url_for('showProducts',cid=cid))
        else:
            sel_catagory = database_service.GetCatagoryByID(cid)
            return render_template('editcatagory.html',catagories=catagories,sel_catagory=sel_catagory,logged_in=logged_in,username=username,picture=picture)
    else:
            flash('No permission to modify this catagory!','alert-danger')
            return redirect(url_for('showProducts',cid=cid))

@app.route('/catagory/<int:cid>/delete', methods=['GET','POST'])
def deleteCatagory(cid):
    logged_in = CheckUserLoggedIn()
    if not logged_in:
        return redirect('/login')
    username = getSessionUsername()
    user_id=getSessionUserID()
    catagories = database_service.GetAllCatagory()
    picture = getSessionUserPic()
    if database_service.hasCatagoryPermission(cid,user_id):
        if request.method == 'POST':
            database_service.DeleteCatagory(cid)
            flash('Catagory deleted!','alert-success')
            return redirect(url_for('IndexPage'))
        else:
            sel_catagory = database_service.GetCatagoryByID(cid)
            return render_template('deletecatagory.html',catagories=catagories,sel_catagory=sel_catagory,logged_in=logged_in,username=username,picture=picture)
    else:
        flash('No permission to delete this catagory!','alert-danger')
        return redirect(url_for('showProducts',cid=cid))

@app.route('/catagory/<int:cid>')
def showProducts(cid):
    username = getSessionUsername()
    catagories = database_service.GetAllCatagory()
    sel_catagory = database_service.GetCatagoryByID(cid)
    products = database_service.GetProductByCatagory(cid)
    user_id = getSessionUserID()
    logged_in = CheckUserLoggedIn()
    picture = getSessionUserPic()
    return render_template('products.html',catagories=catagories,sel_catagory=sel_catagory, products=products,logged_in=logged_in,username=username,user_id=user_id,picture=picture)

@app.route('/product/new', methods=['GET','POST'])
def newProduct():
    logged_in = CheckUserLoggedIn()
    if not logged_in:
        return redirect('/login')
    username = getSessionUsername()
    catagories = database_service.GetAllCatagory()
    picture = getSessionUserPic()
    if request.method == 'POST':
        pic_path = ''
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            pic_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            file.save(pic_path)
        user_id = getSessionUserID()
        database_service.NewProduct(request.form['name'],request.form['desc'],request.form['price'],request.form['flavour'],pic_path,request.form['catagory'],user_id)
        flash('New product created!','alert-success')
        return redirect(url_for('newProduct'))
    else:
        return render_template('newproduct.html',catagories=catagories,logged_in=logged_in,username=username,picture=picture)

@app.route('/catagory/<int:cid>/product/<int:pid>/edit', methods=['GET','POST'])
def editProduct(cid,pid):
    logged_in = CheckUserLoggedIn()
    if not logged_in:
        return redirect('/login')
    username = getSessionUsername()
    user_id=getSessionUserID()
    catagories = database_service.GetAllCatagory()
    picture = getSessionUserPic()
    if database_service.hasProductPermission(pid,user_id):
        if request.method == 'POST':
            database_service.EditProduct(pid,request.form['name'],request.form['desc'],request.form['price'],request.form['flavour'],request.form['catagory'])
            flash('Product updated!','alert-success')
            return redirect(url_for('showProducts',cid=cid))
        else:
            sel_catagory = database_service.GetCatagoryByID(cid)
            sel_product = database_service.GetProductByID(pid)
            return render_template('editproduct.html',catagories=catagories,sel_catagory=sel_catagory, sel_product=sel_product,logged_in=logged_in,username=username,picture=picture)
    else:
        flash('No permission to modify this product!','alert-danger')
        return redirect(url_for('showProducts',cid=cid))

@app.route('/catagory/<int:cid>/product/<int:pid>/delete', methods=['GET','POST'])
def deleteProduct(cid,pid):
    logged_in = CheckUserLoggedIn()
    if not logged_in:
        return redirect('/login')
    username = getSessionUsername()
    user_id=getSessionUserID()
    catagories = database_service.GetAllCatagory()
    picture = getSessionUserPic()
    if database_service.hasProductPermission(pid,user_id):
        if request.method == 'POST':
            database_service.DeleteProduct(pid)
            flash('Product deleted!','alert-success')
            return redirect(url_for('showProducts',cid=cid))
        else:
            sel_catagory = database_service.GetCatagoryByID(cid)
            sel_product = database_service.GetProductByID(pid)
            return render_template('deleteproduct.html',catagories=catagories,sel_catagory=sel_catagory,sel_product=sel_product,logged_in=logged_in,username=username,picture=picture)
    else:
        flash('No permission to delete this product!','alert-danger')
        return redirect(url_for('showProducts',cid=cid))

@app.route('/sidebar')
def sidebar():
    return render_template('sidebar.html')

@app.route('/login')
def showLogin():
    logged_in = CheckUserLoggedIn()
    picture = getSessionUserPic()
    if logged_in:
        username = getSessionUsername()
        flash('You are already logged in as %s' %username,'alert-success')
        return redirect(url_for('IndexPage'))
    catagories = database_service.GetAllCatagory()
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html',catagories=catagories, STATE=state,picture=picture)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),200)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['user_id'] = database_service.CheckUserExist(login_session)
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'],'alert-success')
    print "done!"
    return output

@app.route("/gdisconnect")
def gdisconnect():
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user not connected'),401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' %access_token
    h = httplib2.Http()
    result = h.request(url,'GET')[0]

    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash('Successfully Disconnected','alert-success')
        #response = make_response(json.dumps('Successfully disconnected'),200)
        #response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('IndexPage'))
    else:
        flash('Failed to revoke token for given user.','alert-danger')
        #response = make_response(json.dumps('Failed to revoke token for given user.'),400)
        #response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('IndexPage'))

@app.route("/fbconnect", methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    login_session['user_id'] =  database_service.CheckUserExist(login_session)

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'], 'alert-success')
    return output

@app.route("/fbdisconnect", methods=['POST'])
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    url = 'https://graph.facebook.com/%s/permissions' %facebook_id
    h=httplib2.Http()
    result = h.request(url,'DELETE')[1]
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['facebook_id']
    flash('Successfully Disconnected','alert-success')
    #response = make_response(json.dumps('Successfully disconnected'),200)
    #response.headers['Content-Type'] = 'application/json'
    return redirect(url_for('IndexPage'))

@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        if login_session['provider'] == 'facebook':
            fbdisconnect()
    return redirect(url_for('IndexPage'))

def getThumbnail():
    if 'picture' in login_session:
        return login_session['picture']

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
