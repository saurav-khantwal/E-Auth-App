from flask import Flask

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True

else:
    app.debug = False

app.config['SECRET_KEY'] = '5252ff2ac905b9acd329d6e2'

from MAIN_APP import routes

