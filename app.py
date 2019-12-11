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
    return render_template('index.html', items=items.find())

@app.route('/item/new')
def new_item():
    """Create new item"""
    return render_template('new_item.html')

@app.route('/item', methods=['POST'])
def item_submit():
    """submit a new item"""
    item = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'image': request.form.get('image')
    }
    items.insert_one(item)
    return redirect(url_for('index'))

@app.route('/item/<item_id>')
def item_show(item_id):
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('show_item.html', item=item)

if __name__ == '__main__':
    app.run()
