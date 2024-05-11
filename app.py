# -*- coding: utf-8 -*-

from random import choice
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)

username = ""
password = ""
host = ""
dbname = ""

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{username}:{password}@{host}/{dbname}?charset=utf8'.format(
    username=username, password=password, host=host, dbname=dbname
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

data = []


class Wit(db.Model):
    __tablename__ = 'wit'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(300), nullable=False)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '%s' % self.title


def cache_humors():
    return data.extend([wit.title for wit in Wit.query.with_entities(Wit.title).all()])


@app.route('/index/msg')
def humors():
    if not data:
        cache_humors()
    return choice(data)


@app.route('/')
def humors_index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
