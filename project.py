from models import Base, User, Category, Item
from flask import Flask, jsonify, request, make_response, render_template
from flask import redirect, jsonify, url_for
from flask import session as login_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, desc
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import random
import string
import httplib2
import json
import requests


CLIENT_ID = json.loads(
            open('client_secrets.json', 'r').read())['web']['client_id']


engine = create_engine('sqlite:///itemcatalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(
        string.ascii_uppercase+string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
        % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesnt match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID doesnt match given user ID."), 401)
        print "Token's client ID doesn not match app's"
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id
    login_session['provider'] = 'google'
    response = make_response(json.dumps('Successfully connected user.', 200))

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    print output
    return output


@app.route('/gdisconnect')
def gdisconnect():
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

    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    app_id = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token'
    '?grant_type=fb_exchange_token&client_id=%s&client_secret=%s'
    '&fb_exchange_token=%s' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    userinfo_url = "https://graph.facebook.com/v2.8/me"
    data = json.loads(result)
    token = 'access_token=' + data['access_token']

    url = 'https://graph.facebook.com/v2.8/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
        login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    url = 'https://graph.facebook.com/%s/permissions' % facebook_id
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']

        del login_session['username']
        del login_session['email']
        del login_session['user_id']
        del login_session['provider']
        return redirect(url_for('showCategoriesAndLatest'))
    else:
        redirect(url_for('showCategoriesAndLatest'))


@app.route('/')
def showCategoriesAndLatest():
    categories = session.query(Category).all()
    latest_items = session.query(Item).order_by(desc(Item.id))
    return render_template(
        'home.html',
        categories=categories,
        latest_items=latest_items)


@app.route('/catalog/<int:category_id>/')
def showCategoryItems(category_id):
    categories = session.query(Category).all()
    items = session.query(Item).filter_by(category_id=category_id)
    category = session.query(Category).filter_by(id=category_id).one()
    return render_template(
        'items.html',
        items=items,
        categories=categories,
        category=category)


@app.route('/catalog/<int:category_id>/<string:item_name>/')
def showItemDescription(category_id, item_name):
    item = session.query(Item).filter_by(
        category_id=category_id, title=item_name).one()
    if ('username' not in login_session or
            item.user_id != login_session['user_id']):
        return render_template('publicitem.html', item=item)
    else:
        return render_template('item.html', item=item)


@app.route('/catalog/new/', methods=['GET', 'POST'])
def addNewItem():
    categories = session.query(Category).all()
    if 'username' not in login_session:
        return render_template('notauthorized.html')
    else:
        if request.method == 'POST':
            newItem = Item(
                title=request.form['title'],
                description=request.form['description'],
                category_id=request.form['category_id'],
                user_id=login_session['user_id'])
            session.add(newItem)
            session.commit()
            return redirect(
                url_for('showCategoryItems', category_id=newItem.category_id))
        else:
            return render_template('newitem.html', categories=categories)


@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name):
    categories = session.query(Category).all()
    editedItem = session.query(Item).filter_by(title=item_name).one()
    if editedItem.user_id == login_session['user_id']:
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            category_id = request.form['category_id']
            if title != editedItem.title:
                editedItem.title = title
            if description != editedItem.description:
                editedItem.description = description
            if category_id != editedItem.category_id:
                editedItem.category_id = category_id
            session.add(editedItem)
            session.commit()
            return redirect(url_for(
                'showCategoryItems', category_id=editedItem.category_id))
        else:
            return render_template(
                'edititem.html', categories=categories, item=editedItem)
    else:
        return render_template('notauthorized.html')


@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
def deleteItem(item_name):
    deleteItem = session.query(Item).filter_by(title=item_name).one()
    if deleteItem.user_id == login_session['user_id']:
        if request.method == 'POST':
            session.delete(deleteItem)
            session.commit()
            return redirect(url_for('showCategoriesAndLatest'))
        else:
            return render_template('deleteitem.html', item_name=deleteItem)
    else:
        return render_template('notauthorized.html')


@app.route('/catalog/<string:item_name>/json/')
def catelogJSON(item_name):
    item = session.query(Item).filter_by(title=item_name).one()
    return jsonify(item.serialize)


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def createUser(login_session):
    newUser = User(
        name=login_session['username'], email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

