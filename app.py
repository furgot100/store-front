from flask import Flask, render_template, redirect, url_for
from pymongo import MongoClient
# from bson.objectid import ObjectId

client = MongoClient()
db = client.Store
item = db.items


app = Flask(__name__)

@app.route('/')
def index():
    '''Returns the homepage'''
    return render_template('index.html', items=item.find())

@app.route('/item/new')
def new_item():
    return render_template('new_item.html')





if __name__ == '__main__':
    app.run()
