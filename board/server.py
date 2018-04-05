from flask import Flask
from flask_restful import marshal_with, fields, Resource, Api
from time import sleep

app_serv = Flask(__name__)
api = Api(app_serv)



status = {
    'pump': 0,
}




class Switch(Resource):

    @marshal_with({
        'status': fields.Integer(default=0)
    })
    def get(self):
        global status
        new_state = status['pump'] ^ 1
        sleep(2)
        status['pump'] = new_state
        return {'status': status['pump']}

api.add_resource(Switch, '/switch')

@app_serv.route('/start')
def start():
    return 'Старт'


# @app_serv.route('/switch')
# def switch():
#     global status
#     new_state = status['pump'] ^ 1
#     sleep(2)
#     status['pump'] = new_state
#     return status['pump']


@app_serv.route('/stop')
def stop():
    return 'Стоп'

if __name__ == '__main__':
    app_serv.run(debug=True, port=5001)
