from . import dash as app, db
from . import models
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import random
from board import page
from board.bootstrap_dash import *
import plotly.graph_objs as go
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect, text

rnd = random.Random()

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
                    html.Button('Насос', id='Nasos', style={
                        'width': '15%', 'display': 'inline-block', 'margin': '1%'}),
                    html.Button('Нагреватель1', id='Nagrev', style={
                        'width': '15%', 'display': 'inline-block', 'margin': '1%'}),
                    html.Button('Нагреватель2', id='Nagrev', style={
                        'display': 'inline-block', 'width': '15%', 'margin': '1%'}),
                    html.Button('Нагреватель3', id='Nagrev', style={
                        'display': 'inline-block', 'width': '15%', 'margin': '1%'}),
                    html.Button('Клапан', id='Klap', style={
                        'display': 'inline-block', 'width': '15%', 'margin': '1%'}),
                    html.Button('Вентиль', id='Valve', style={
                        'display': 'inline-block', 'width': '13%', 'margin': '1%'})
                ])
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(212, 232, 241)',
            'padding': '15px 5px'
        }),

        html.Div([
            dcc.Graph(id='history-graph', animate=True),
        ],
        ),
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
        counter=1)
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

    x = [i['time'] for i in query]
    y = [float(i['val']) for i in query]

    return {
        'data': [go.Scatter(
            # тут я хочу привязать данные из списка к history
            # пытаюсь вывести это на график
            # x=x,
            y=y,
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(

            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }
