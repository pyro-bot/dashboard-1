from flask import Flask

app_serv = Flask(__name__)


@app_serv.route('/page')
def hello_world():
    return 'Старт'


@app_serv.route('/page')
def hello_world():
    return 'Переключение'


@app_serv.route('/page2')
def hello_world():
    return 'Стоп'
