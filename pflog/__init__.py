import os

from flask import Flask, app, render_template
from sqlalchemy import select, text

from common.consts import CONN_STR
from common.models import Post
from db.flask_db import db_session
from db.sqlite import run_query, get_session


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = CONN_STR
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def index():
        session = get_session()
        query = select(Post).order_by(Post.id.desc())
        posts = run_query(query, session=session)
        return render_template('index.html', posts=posts)

    @app.route('/post/<int:post_id>')
    def view(post_id):
        session = get_session()
        query = select(Post).where(Post.id == post_id)
        post = run_query(query, session=session).first()
        return render_template('post.html', post=post)

    return app


def shutdown_session(exception=None):
    db_session.remove()
