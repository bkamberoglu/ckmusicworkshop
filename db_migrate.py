#!flask/bin/python
import imp
from migrate.versioning import api
from app import app, db
#from config import SQLALCHEMY_DATABASE_URI
#from config import SQLALCHEMY_MIGRATE_REPO
from config import config

v = api.db_version(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO'])
migration = app.config['SQLALCHEMY_MIGRATE_REPO'] + ('/versions/%03d_migration.py' % (v+1))
tmp_module = imp.new_module('old_model')
old_model = api.create_model(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO'])
exec(old_model, tmp_module.__dict__)
script = api.make_update_script_for_model(app.config['SQLALCHEMY_DATABASE_URI'],
                                          app.config['SQLALCHEMY_MIGRATE_REPO'],
                                          tmp_module.meta, db.metadata)
open(migration, "wt").write(script)
api.upgrade(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO'])
v = api.db_version(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO'])
print('New migration saved as ' + migration)
print('Current database version: ' + str(v))


