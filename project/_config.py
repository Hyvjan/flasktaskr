import os

#Grab the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
USERNAME = 'admin'
PASSWORD = 'admin'
WTF_CSRF_ENABLED = True
SECRET_KEY = '/O@{L/FK+-aI^Cg9cDa56Y7Qdjl01t'

#define the full path for database
DATABASE_PATH = os.path.join(basedir, DATABASE)

#The database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH