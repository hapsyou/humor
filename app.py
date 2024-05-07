# -*- coding: utf-8 -*-

from random import choice
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

humor_list = []

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Wit(db.Model):
    __tablename__ = 'wit'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(300), nullable=False)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '%s' % self.title


def cache_humors():
    humor_list.extend([wit.title for wit in Wit.query.with_entities(Wit.title).all()])


@app.route('/index')
def humors():
    if not humor_list:
        cache_humors()

    return choice(humor_list)


if __name__ == '__main__':
    app.run()
