import os
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SERECT_KEY = 'supersecret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FACEBOOK_OAUTH_CLIENT_ID= os.environ.get("FACEBOOK_OAUTH_CLIENT_ID")
    FACEBOOK_OAUTH_CLIENT_SECRET = os.environ.get("FACEBOOK_OAUTH_CLIENT_SECRET") 