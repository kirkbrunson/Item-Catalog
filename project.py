import requests
import random
import string
import httplib2
import json
import os
import xml.etree.ElementTree as ET
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response
from flask import session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Categories, subCategories, Items, Inventory, Users, Sales, Reviews, Base
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask.ext.seasurf import SeaSurf


# General readme:
# ---------------
# Using Flask-Seasurf to generate Nonces & prevent CSRF
# https://flask-seasurf.readthedocs.org/en/latest/

# Learned how to handle flask file uploads here:
# http://code.runnable.com/UiPcaBXaxGNYAAAL/
# how-to-upload-a-file-to-the-server-in-flask-for-python

# Soon to implement user profile that has previous orders, reviews & wishlist


# op err on cat/new
# lgin dec. login state
# readme
# setup script


app = Flask(__name__)
csrf = SeaSurf(app)
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])


APPLICATION_NAME = "FSND-P3"
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


'''
TODO
------
last card/ side bar issue

- cart backend
- cart template render dynamic

user profile backend
- getters/ setters ^
- user profile template

- add reveiws backend
- add reviews to templates [user and items]

- image resizing: handle images too large/ not optimized/ wrong dims

- issue with login session... getting 304 from google.
- Error page templates
- Err handling. && blnk form vals

DRY image add
DRY func [getters- ext and pass qs parse args.]
'''

# Global var used as sig val for templates
global loginState
loginState = False


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


# Connect to DB and create DB session
# ===========================================================================
engine = create_engine('sqlite:///samplestore.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# ===========================================================================
# User Auth. Login/ Logout
# Code from oauth class teaching g openid login

# Create anti-forgery state token
@csrf.exempt
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state, login=loginState)


@csrf.exempt
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
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials']= credentials.to_json()
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    global loginState
    loginState = True

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

    # DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/logout')
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        global loginState
        loginState = False

        # response = make_response(json.dumps('Successfully disconnected.'), 200)
        # response.headers['Content-Type'] = 'application/json'
        return redirect('/')
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# ===========================================================================
# Provides JSON and XML API endpoints
# Route schema: /category/[json, xml]
#               /category/subcategory/[json, xml]

# JSON endpoints
@app.route('/women/json/')
def json_Women():
    subCat = session.query(subCategories).filter_by(category_id=1).all()
    return jsonify(subCategories=[i.serialize for i in subCat])


@app.route('/men/json/')
def json_Men():
    subCat = session.query(subCategories).filter_by(category_id=2).all()
    return jsonify(subCategories=[i.serialize for i in subCat])


@app.route('/women/<int:subcategory_id>/json/')
@app.route('/men/<int:subcategory_id>/json/')
def json_subCategory(subcategory_id):
    # add Not found if nothing ret from session.query?
    products = session.query(Items).filter_by(subCategory=subcategory_id).all()
    return jsonify(products=[i.serialize for i in products])


# XML endpoints
@app.route('/women/xml/')
def xml_Women():
    data = session.query(subCategories).filter_by(category_id=1).all()

    # Create xml tree: (same for rest of api... skipping comments)
    root = ET.Element("root", categories="categories")

    # add res from query to xml tree
    for i in data:
        j = ET.SubElement(root, "Category")
        a = ET.SubElement(j, "id")
        a.text = "%r" % i.id

        b = ET.SubElement(j, "name")
        b.text = "%s" % i.name
        c = ET.SubElement(j, "category_id")
        c.text = "%r" % i.category_id

        d = ET.SubElement(j, "description")
        d.text = "%s" % i.description

    # create and send response
    response = app.response_class(
        ET.tostring(root), mimetype='application/xml')
    return response


@app.route('/men/xml/')
def xml_Men():
    data = session.query(subCategories).filter_by(category_id=2).all()
    root = ET.Element("root", categories="categories")

    for i in data:
        j = ET.SubElement(root, "Category")
        a = ET.SubElement(j, "id")
        a.text = "%r" % i.id

        b = ET.SubElement(j, "name")
        b.text = "%s" % i.name
        c = ET.SubElement(j, "category_id")
        c.text = "%r" % i.category_id

        d = ET.SubElement(j, "description")
        d.text = "%s" % i.description

    response = app.response_class(
        ET.tostring(root), mimetype='application/xml')
    return response


@app.route('/women/<int:subcategory_id>/xml/')
@app.route('/men/<int:subcategory_id>/xml/')
def xml_SubCategory(subcategory_id):
    data = session.query(Items).filter_by(subCategory=subcategory_id).all()
    root = ET.Element("root", categories="Products")

    for i in data:
        j = ET.SubElement(root, "Item")
        a = ET.SubElement(j, "id")
        a.text = "%r" % i.id

        b = ET.SubElement(j, "name")
        b.text = "%s" % i.name

        c = ET.SubElement(j, "Category")
        c.text = "%r" % i.category

        d = ET.SubElement(j, "subCategory")
        d.text = "%r" % i.subCategory

        e = ET.SubElement(j, "description")
        e.text = "%s" % i.description

        f = ET.SubElement(j, "price")
        f.text = "%s" % i.price

    response = app.response_class(
        ET.tostring(root), mimetype='application/xml')
    return response


# ===========================================================================
# Getter functions for Home, Categories: Men/Women, sub categories, and items
# Route schema: /category/subcategory/productID

@app.route('/')
def home():
    return render_template('index.html', login=loginState)


# Get top level categories. Displays the subCat(s) for that category.
@app.route('/women/')
def getWomen():
    categories = session.query(subCategories).filter_by(category_id=1).all()
    return render_template('category.html', categories=categories, login=loginState)


@app.route('/men/')
def getMen():
    categories = session.query(subCategories).filter_by(category_id=2).all()
    return render_template('category.html', categories=categories, login=loginState)


# Get Sub categories. Displays the item(s) for that sub category.
@app.route('/women/<int:subcategory_id>/')
def getSubCategory_Women(subcategory_id):
    categories = session.query(subCategories).filter_by(category_id=1).all()
    items = session.query(Items).filter_by(
        category=1).filter_by(subCategory=subcategory_id).all()
    return render_template('subCategory.html', items=items, categories=categories, login=loginState)


@app.route('/men/<int:subcategory_id>/')
def getSubCategory_Men(subcategory_id):
    categories = session.query(subCategories).filter_by(category_id=2).all()
    items = session.query(Items).filter_by(
        category=2).filter_by(subCategory=subcategory_id).all()
    return render_template("subCategory.html", items=items, categories=categories, login=loginState)


# Get a single product
@app.route('/women/<int:subcategory_id>/<int:item_id>/')
@app.route('/men/<int:subcategory_id>/<int:item_id>/')
def getItem(subcategory_id, item_id):
    item = session.query(Items).filter_by(id=item_id).one()
    return render_template("item.html", item=item, login=loginState)


# =======================================================================
# Setter functions for Categories: Men/Women, sub categories, and items
# Route schema: .../operation from [new, edit, delete]

# New subCategories
@app.route('/women/new', methods=['GET', 'POST'])
def newWomensSubCategory():

    # Check if login is valid.
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        newSubCategory = subCategories(
            category_id=1, name=request.form['name'], description=request.form['description'])

        # Get the name of the uploaded file
        file = request.files['file']
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            fileExt = str(file.filename).split('.')[1]
            filename = str(session.query(subCategories).order_by(
                subCategories.id.desc()).first().id+1) + '.' + fileExt


            file.save(os.path.join('static/img/category/', filename))

        # Add and commit
        session.add(newSubCategory)

        # edit flash msg
        flash('New SubCategory %s Successfully Created' % newSubCategory.name)
        session.commit()
        return redirect('/women/')
    else:
        return render_template('newSubCategory.html', login=loginState)


@app.route('/men/new', methods=['GET', 'POST'])
def newMensSubCategory():

    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        newSubCategory = subCategories(
            category_id=2, name=request.form['name'], description=request.form['description'])

        # Get the name of the uploaded file
        file = request.files['file']
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):

            # Make the filename safe, remove unsupported chars
            fileExt = str(file.filename).split('.')[1]
            filename = str(session.query(subCategories).order_by(
                subCategories.id.desc()).first().id+1) + '.' + fileExt

            print filename
            file.save(os.path.join('static/img/category/', test))

        # Add and commit
        session.add(newSubCategory)

        # edit flash msg
        flash('New SubCategory %s Successfully Created' % newSubCategory.name)
        session.commit()
        return redirect('/men/')
    else:
        return render_template('newSubCategory.html', login=loginState)


# New item
@app.route('/women/<int:subcategory_id>/new', methods=['GET', 'POST'])
def new_wItem(subcategory_id):
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        newItem = Items(category=1, subCategory=subcategory_id, name=request.form[
                        'name'], description=request.form['description'], price=request.form['price'])

        # Get the name of the uploaded file
        file = request.files['file']
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            fileExt = str(file.filename).split('.')[1]
            filename = str(session.query(Items).order_by(
                Items.id.desc()).first().id+1) + '.' + fileExt

            file.save(os.path.join('static/img/product/', filename))

        # Add and commit
        session.add(newItem)

        # edit flash msg
        flash('New Item %s Successfully Created' % newItem.name)
        session.commit()
        return redirect('/women/%r' % subcategory_id)
    else:
        return render_template('newItem.html', login=loginState)


@app.route('/men/<int:subcategory_id>/new', methods=['GET', 'POST'])
def new_mItem(subcategory_id):
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        newItem = Items(category=2, subCategory=subcategory_id, name=request.form[
                        'name'], description=request.form['description'], price=request.form['price'])

        # Get the name of the uploaded file
        file = request.files['file']
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            fileExt = str(file.filename).split('.')[1]
            filename = str(session.query(Items).order_by(
                Items.id.desc()).first().id+1) + '.' + fileExt

            file.save(os.path.join('static/img/product/', filename))

        # Add and commit
        session.add(newItem)

        # edit flash msg
        flash('New Item %s Successfully Created' % newItem.name)
        session.commit()
        return redirect('/men/%r' % subcategory_id)
    else:
        return render_template('newItem.html', login=loginState)


# Edit subCategories
@app.route('/women/<int:subcategory_id>/edit', methods=['GET', 'POST'])
@app.route('/men/<int:subcategory_id>/edit', methods=['GET', 'POST'])
def editMensSubCategory(subcategory_id):

    if 'username' not in login_session:
        return redirect('/login')

    editSubCategory = session.query(
        subCategories).filter_by(id=subcategory_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editSubCategory.name = request.form['name']

        if request.form['description']:
            editSubCategory.description = request.form['description']

        # # Add and commit
        session.add(editSubCategory)

        # edit flash msg
        flash('SubCategory %s Successfully Edited' % editSubCategory.name)
        session.commit()

        # redirect to proper category
        if subCategory.category_id == 1:
            return redirect('/women')
        elif subCategory.category_id == 2:
            return redirect('/men')
        else:
            redirect('/')

    else:
        return render_template('editSubCategory.html', subCategory=editSubCategory, login=loginState)


# Edit Item
@app.route('/women/<int:subcategory_id>/<int:item_id>/edit', methods=['GET', 'POST'])
@app.route('/men/<int:subcategory_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def editMensItem(subcategory_id, item_id):

    if 'username' not in login_session:
        return redirect('/login')

    item = session.query(Items).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']

        if request.form['description']:
            item.description = request.form['description']

        if request.form['price']:
            item.price = request.form['price']

        # # Add and commit
        session.add(item)

        # edit flash msg
        flash('SubCategory %s Successfully Edited' % item.name)
        session.commit()

        # redirect to proper subCategory
        if item.category == 1:
            return redirect('/women/%r' % subcategory_id)
        elif item.category == 2:
            return redirect('/men/%r' % subcategory_id)
        else:
            return redirect('/')
    else:
        return render_template('edititem.html', item=item, login=loginState)


# Delete SubCategory
@app.route('/women/<int:subcategory_id>/delete', methods=['GET', 'POST'])
@app.route('/men/<int:subcategory_id>/delete', methods=['GET', 'POST'])
def deleteSubCategory(subcategory_id):
    if 'username' not in login_session:
        return redirect('/login')

    subCategory = session.query(
        subCategories).filter_by(id=subcategory_id).one()
    if request.method == 'POST':
        session.delete(subCategory)
        flash('%s Successfully Deleted' % subCategory.name)
        session.commit()

        # redirect to proper category
        if subCategory.category_id == 1:
            return redirect('/women')
        elif subCategory.category_id == 2:
            return redirect('/men')
        else:
            redirect('/')
    else:
        return render_template('deleteSubCategory.html', subCategory=subCategory, login=loginState)


# Delete Item
@app.route('/women/<int:subcategory_id>/<int:item_id>/delete', methods=['GET', 'POST'])
@app.route('/men/<int:subcategory_id>/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(subcategory_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')

    item = session.query(Items).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(item)
        flash('%s Successfully Deleted' % item.name)
        session.commit()

        # redirect to proper category
        if item.category == 1:
            return redirect('/women/%r' % item.subCategory)
        elif item.category == 2:
            return redirect('/men/%r' % item.subCategory)
        else:
            redirect('/')
    else:
        return render_template('deleteItem.html', item=item, login=loginState)


# =======================================================================
# Cart and checkout:
@app.route('/cart')
def getCart():

    # Will implement
    # render cart for user bsaed on a session.
    return render_template("cart.html", login=loginState)


# =======================================================================
# User profile: basic info. Orders, reviews and wishlast


# @app.route('/user/<int:user_id>')
# def getUser():

    # set name and prof pic as from g+ login. where login sessin == user.id
    # get unique user id in db
    # get user previous orders, reviews and wishlist.

    # return "profile.html"
    # setters for user functions?


# =======================================================================
# Review functions:


# =======================================================================


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
