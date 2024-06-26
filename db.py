import sqlite3

from flask import g

__db = 'voles.db'


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(__db)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)