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
from sqlalchemy import inspect

rnd = random.Random()

app.css.append_css({
    "external_url": ['/static/css/bootstrap.css', '/static/css/bootstrap-theme.css']})

#Метод нужен для первоначальной отрисовки страицы

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
                    options=[{'label': i['name'], 'value': i['id_counters']} for i in db.engine.execute('Select * from Counters')],
                    value=0
                ),
            ],
                style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                html.H3('Показания'),
                dcc.Dropdown(
                    id='Parametrs',
                    options=[{'label': i['name'], 'value': i['id_parametrs']} for i in db.engine.execute('Select * from Parametrs')],
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


# Это пример коллбека, выполняется по таймеру и обновляет страницу без ее перезагрузки (декораток творит магию)
@app.callback(Output('history-graph', 'figure'),
              [Input('Interval', 'n_intervals'), Input('Counter', 'value'),Input('Parametrs', 'value')])
def get_history(tick,param):
    new = models.History(value=rnd.random(),
                         counters_parametr=rnd.choice(db.session.query(models.CountersParametr).all()))
    db.session.add(new)
    db.session.commit()
    return {
        'data': [
            {
                'y': [record.value for record in df.filter(db.id_counters_parametrs==param).order_by(df.time.desc()).limit(20).all()],

                'type': 'scatter',
            }
        ],
        'layout': {
            'margin': {
                'l': 30,
                'r': 0,
                'b': 30,
                't': 0
            },
            'legend': {'x': 0, 'y': 1}
        }
    }