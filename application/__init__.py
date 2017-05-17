# -*-coding: utf-8-*-
# time: 2015/09/16 22:43
# author: liukaizeng

import os

import redis

from flask import Flask, url_for, sessions, g
from flask_login import LoginManager, AnonymousUserMixin, current_user
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_session import RedisSessionInterface

from application.configure import setting

app = Flask(setting.APP_NAME)
app.config.from_object(setting)
db = SQLAlchemy(app)
Bootstrap(app)


def configure_url_for_with_timestamp(app):
    @app.context_processor
    def override_url_for():
        return dict(url_for=dated_url_for)

    def dated_url_for(endpoint, **values):
        if endpoint != 'static':
            return url_for(endpoint, **values)

        filename = values.get('filename', None)
        if not filename:
            return url_for(endpoint, **values)

        file_path = os.path.join(app.root_path, endpoint, filename)
        values['q'] = int(os.stat(file_path).st_mtime)

        return url_for(endpoint, **values)


configure_url_for_with_timestamp(app)


from application.models.user import User


def configure_login_manager(app):
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"

    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(user_id):
        if user_id:
            return User.query.get(user_id)
        else:
            return AnonymousUserMixin()


configure_login_manager(app)

##configure_redis_session_interface(_app)
##configure_subdomain(_app)


from . import views
Blueprints = (
    (views.index_bp, ''),
    (views.auth_bp, '/auth')
)


def configure_blueprints(app, blueprints):
    for view, url_prefix in blueprints:
        app.register_blueprint(view, url_prefix=url_prefix)

    # test subDomain
    #app.register_blueprint(views.test_bp)


configure_blueprints(app, Blueprints)


def configure_redis_session_interface(app):
    redis_client = redis.Redis(setting.REDIS_HOST, setting.REDIS_PORT)
    app.session_interface = RedisSessionInterface(redis_client, 'session:')


def configure_subdomain(app):
    @app.url_value_preprocessor
    def add_subdomain_to_global(endpoint, values):
        g.subdomain = values.pop('subdomain', None)

    @app.url_defaults
    def add_subdomain_to_url_params(endpoint, values):
        if 'subdomain' not in values:
            values['subdomain'] = g.subdomain


@app.before_request
def before_request():
    g.user = current_user



if __name__ == '__main__':
    app.run()
