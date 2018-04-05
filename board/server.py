from flask import Flask
from flask_restful import marshal_with, fields, Resource, Api
from time import sleep

app_serv = Flask(__name__)
api = Api(app_serv)

status = {
    'pump': 0,
    'heater1': 0,
    'heater2': 0,
    'heater3': 0,
    'klap': 0,
    'valve': 0
}


class Switch_pump(Resource):
    @marshal_with({
        'status': fields.Integer(default=0)
    })
    def get(self):
        global status
        pump = status['pump'] ^ 1
        sleep(2)
        status['pump'] = pump
        return {'status': status['pump']}


api.add_resource(Switch_pump, '/switch-pump')


class Switch_heater1(Resource):
    @marshal_with({
        'status': fields.Integer(default=0)
    })
    def get(self):
        global status
        heater1 = status['heater1'] ^ 1
        sleep(2)
        status['heater1'] = heater1
        return {'status': status['heater1']}


api.add_resource(Switch_heater1, '/switch-heater1')


class Switch_heater2(Resource):
    @marshal_with({
        'status': fields.Integer(default=0)
    })
    def get(self):
        global status
        heater1 = status['heater2'] ^ 1
        sleep(2)
        status['heater2'] = heater1
        return {'status': status['heater2']}


api.add_resource(Switch_heater2, '/switch-heater2')


class Switch_heater3(Resource):
    @marshal_with({
        'status': fields.Integer(default=0)
    })
    def get(self):
        global status
        heater1 = status['heater3'] ^ 1
        sleep(2)
        status['heater3'] = heater1
        return {'status': status['heater3']}


api.add_resource(Switch_heater3, '/switch-heater3')


class Switch_klap(Resource):
    @marshal_with({
        'status': fields.Integer(default=0)
    })
    def get(self):
        global status
        heater1 = status['klap'] ^ 1
        sleep(2)
        status['klap'] = heater1
        return {'status': status['klap']}


api.add_resource(Switch_klap, '/switch-klap')


class Switch_valve(Resource):
    @marshal_with({
        'status': fields.Integer(default=0)
    })
    def get(self):
        global status
        heater1 = status['valve'] ^ 1
        sleep(2)
        status['valve'] = heater1
        return {'status': status['valve']}


api.add_resource(Switch_valve, '/switch-valve')


@app_serv.route('/start')
def start():
    return 'Старт'


@app_serv.route('/stop')
def stop():
    return 'Стоп'


if __name__ == '__main__':
    app_serv.run(debug=True, port=5001)
