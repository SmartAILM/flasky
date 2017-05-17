# -*-coding: utf-8-*-
# time: 2015/09/16 22:38
# author: liukaizeng

from flask_script import Manager
from application import app, db
from application.models import User

manager = Manager(app)

@manager.command
def create_db():
    db.create_all()


@manager.command
def drop_db():
    db.drop_all()


@manager.command
def create_admin():
    db.session.add(User('admin@smartai.com', 'smart', 'admin123'))
    db.session.commit()



if __name__ == '__main__':
    manager.run()
