from os import path, getenv
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = getenv('SECRET_KEY') or 'you-will-never-guess'

    NLU_APIKEY = getenv('NLU_APIKEY')
    NLU_URL = getenv('NLU_URL')
    #NLU_MODEL_ID = getenv('NLU_MODEL_ID')
