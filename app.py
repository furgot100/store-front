from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import os


host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/wishlist')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
items = db.items


app = Flask(__name__)

@app.route('/')
def index():
    '''Returns the homepage'''
    return render_template('index.html', items=items.find())

@app.route('/item/new')
def new_item():
    """Create new item"""
    return render_template('item_new.html')

@app.route('/item', methods=['POST'])
def item_submit():
    """submit a new item"""
    item = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'image': request.form.get('image')
    }
    item_id = items.insert_one(item).inserted_id
    return redirect(url_for('index', item_id=item_id))

@app.route('/item/<item_id>')
def item_show(item_id):
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('show_item.html', item=item)

@app.route('/item/<item_id>', methods=['POST'])
def item_update(item_id):
    updated_item = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'image': request.form.get('image')
    }
    items.update_one(
        {'_id': ObjectId(item_id)},
        {'$set': updated_item})
    return redirect(url_for('index', item_id=item_id))

@app.route('/item/<item_id>/edit')
def item_edit(item_id):
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('item_edit.html', item=item, title='Edit Item')

@app.route('/item/<item_id>/delete', methods=['POST'])
def item_delete(item_id):
    items.delete_one({'_id': ObjectId(item_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
