from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client.Store
items = db.items


app = Flask(__name__)

@app.route('/')
def index():
    '''Returns the homepage'''
    item = items.find()
    return render_template('index.html', item=item)

@app.route('/item/new')
def new_item():
    return render_template('new_item.html')


@app.route('/item', methods=['POST'])
def item_submit():
    """Submit new item"""
    item = {
        'title' : request.form.get('title'),
        'description' : request.form.get('description'),
        'price': request.form.get('price'),
        'url': request.form.get('url')
    }
    item_id = items.insert_one(item).inserted_id
    return redirect(url_for('index', item_id=item_id))


@app.route('/item/<item_id>')
def show_item(item_id):
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('show_item.html', item=item)


@app.route('/item/<item_id>', methods=['POST'])
def update_item(item_id):
    
    new_item = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'price' : request.form.get('price'),
        'img_url': request.form.get('img_url')
    }
    items.update_one(
        {'_id': ObjectId(item_id)},
        {'$set': new_item}
    )
    return redirect(url_for('show_item', item_id=item_id))

@app.route('/edit/<item_id>', methods=['GET'])
def edit_item(item_id):
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('edit_item.html', item=item)





if __name__ == '__main__':
    app.run()
