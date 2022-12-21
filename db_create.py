
#!flask/bin/python
from migrate.versioning import api
#from config import SQLALCHEMY_DATABASE_URI
#from config import SQLALCHEMY_MIGRATE_REPO
from app import app, db
#from flask import current_app
import os.path

#from app import create_app

#from app.config import configure_app

#app = create_app(os.getenv('FLASK_CONFIG') or 'default')

#print("app.config['SQLALCHEMY_DATABASE_URI'] ", app.config['SQLALCHEMY_DATABASE_URI'])

#print("app.config['SQLALCHEMY_MIGRATE_REPO'] ", app.config['SQLALCHEMY_MIGRATE_REPO'])


db.create_all()
if not os.path.exists(app.config['SQLALCHEMY_MIGRATE_REPO']):
    api.create(app.config['SQLALCHEMY_MIGRATE_REPO'], 'database repository')
    api.version_control(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO'])
else:
    api.version_control(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO'],
                        api.version(app.config['SQLALCHEMY_MIGRATE_REPO']))

'''

#!flask/bin/python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path

print("SQLALCHEMY_DATABASE_URI ", SQLALCHEMY_DATABASE_URI)

print("SQLALCHEMY_MIGRATE_REPO ", SQLALCHEMY_MIGRATE_REPO)

db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,
                        api.version(SQLALCHEMY_MIGRATE_REPO))


'''
