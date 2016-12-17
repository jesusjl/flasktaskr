import os

# grab the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = 'flasktaskr.db'
CSRF_ENABLED = True
DEBUG = True
# use random key generator instead
# https://github.com/rjw57/hdcp-genkey
SECRET_KEY = "my_precious"

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# the database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:////' + DATABASE_PATH
