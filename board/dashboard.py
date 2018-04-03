from time import sleep

from . import dash as app, db
from . import models
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import datetime
from board import page
from board.bootstrap_dash import *
import plotly.graph_objs as go
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect, text
import numpy as np


app.css.append_css({
    "external_url": ['/static/css/bootstrap.css', '/static/css/bootstrap-theme.css']})


# Метод нужен для первоначальной отрисовки страицы

def render():
    return page.get_layout(html.Div([
        dcc.Interval(
            id='Interval',
            interval=2 * 1000,  # in milliseconds
            n_intervals=0
        ),
        html.Div([
            html.Div([
                html.H3('Счетчик'),
                dcc.Dropdown(
                    id='Counter',
                    options=[{'label': i['name'], 'value': i['id_counters']} for i in db.engine.execute(
                        'SELECT * FROM counters')],
                    value=0
                ),
            ],
                style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                html.H3('Показания'),
                dcc.Dropdown(
                    id='parametr',
                    options=[],
                    value=0
                ),
            ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),

            html.Div(
                [
                    html.Button('Насос', id='Nasos', className="btn btn-primary", style={
                        'width': '15%', 'display': 'inline-block', 'margin': '1%'}),
                    html.Button('Нагреватель1', className="btn btn-primary", id='Nagrev1', style={
                        'width': '15%', 'display': 'inline-block', 'margin': '1%'}),
                    html.Button('Нагреватель2', className="btn btn-primary", id='Nagrev2', style={
                        'display': 'inline-block', 'width': '15%', 'margin': '1%'}),
                    html.Button('Нагреватель3', className="btn btn-primary", id='Nagrev3', style={
                        'display': 'inline-block', 'width': '15%', 'margin': '1%'}),
                    html.Button('Клапан', className="btn btn-primary", id='Klap', style={
                        'display': 'inline-block', 'width': '15%', 'margin': '1%'}),
                    html.Button('Вентиль', className="btn btn-primary", id='Valve', style={
                        'display': 'inline-block', 'width': '13%', 'margin': '1%'})
                ])
        ], ),

        html.Div([
            dcc.Graph(id='history-graph', animate=True),
        ],
        ),
        html.Div(id='live-update-text'),
    ]))


# Это описание веб страницы
app.layout = render

callback_init()


@app.callback(Output('parametr', 'options'),
              [Input('Counter', 'value')])
def get_param(counter):
    q = db.engine.execute(text(
        """SELECT name, unit, counters_parametrs.id_counters_parametrs AS id_parametrs 
            FROM counters_parametrs JOIN parametrs ON counters_parametrs.id_parametrs = parametrs.id_parametrs
            WHERE id_counters = :counter
        """),
        counter=counter)
    buf = [{
        'label': '{name} ({unit})'.format(**i),
        'value': i['id_parametrs']
    }
        for i in q]
    return buf

# Это пример коллбека, выполняется по таймеру и обновляет страницу без ее перезагрузки (декораток творит магию)
@app.callback(Output('history-graph', 'figure'),
              [Input('Interval', 'n_intervals'),
               Input('parametr', 'value')])
def get_history(tick, param):
    # тут осуществляю связь многие ко многим ,чтоб параметры могли быть равны value=values and time = time
    query = db.engine.execute(text("""
    select time, `values` as val from history WHERE id_counters_parametrs = :param
    """), param=param)

    query = list(query)

    x = list([i['time'] for i in query])
    y = [i['val'] for i in query]
    return {
        'data': [go.Scatter(
            # тут я хочу привязать данные из списка к history
            # пытаюсь вывести это на график
            x=x,
            y=y,
            mode='lines+markers',
            marker={
                'size': 10,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'black'}
            }
        )],
        'layout': go.Layout(

            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            yaxis={
                'range': [min(0, min(y or [0])), max(50, max(y or [50]) + 3)]
            },
            xaxis={
                'range': [min(x or [datetime.datetime.today()]) - datetime.timedelta(days=1),
                          max(x or [datetime.datetime.today()]) + datetime.timedelta(days=1)]
            },
        ),

    }


# тут пытаюсь обновить текст , но как то скудно
@app.callback(Output('live-update-text', 'children'),
              [Input('Interval', 'n_intervals'),
               Input('parametr', 'value')],
              )
def update_metrics(n_intervals, param):
    # a = db.engine.execute(text("""
    # select `counters_parametrs.id_counters_parametrs` AS id_counters_parametrs,`value` as val from counters_parametrs val join
    # on countres_parametrs.id_counters_parametrs = val.id_counters_parametrs  where id_counters_parametrs :=val"""),
    # val=val)

    query = db.engine.execute(text('select `value` as val from val WHERE id_counters_parametrs=:param'), param=param)
    y = [i['val'] for i in query]
    if len(y) > 0:
        y = y[0]
    else:
        y = 0
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Значение: {0}'.format(y), style=style)
    ]

@app.callback(Output('btn-pump', 'className'),
              [Input('Interval', 'n_intervals'),
               Input('btn-pump', 'n_clicks')])
def btn_pump_update(n_clicks, n_intervals):
    state = 1
#
# @app.callback(Input('Nasos', 'n_clicks'))
# def but(a):
#     print('test1')
#     sleep(3)
#     print('test1')
#
#
# @app.callback(Input('Nagrev1', 'n_clicks'))
# def but(a):
#     print('test2')
#     sleep(3)
#     print('test2')
#
#
# @app.callback(Input('Nagrev2', 'n_clicks'))
# def but(a):
#     print('test3')
#     sleep(3)
#     print('test3')
#
#
# @app.callback(Input('Nagrev3', 'n_clicks'))
# def but(a):
#     print('test4')
#     sleep(3)
#     print('test4')
#
#
# @app.callback(Input('Klap', 'n_clicks'))
# def but(a):
#     print('test5')
#     sleep(3)
#     print('test5')
#
#
# @app.callback(Input('Valve', 'n_clicks'))
# def but(a):
#     print('test6')
#     sleep(3)
#     print('test6')