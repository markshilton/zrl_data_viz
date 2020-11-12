# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import logging

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('../data/race_data.csv')
rounds = df['round'].unique().tolist()
row_count = len(rounds * 2)

app.layout = html.Div(children=[
    html.H1(children="Watts occurring"),
    html.Div(children="A visualisation of all the power I put out in the first WTRL/Zwift Racing League season"),
    html.Label('Choose your metric'),
    dcc.RadioItems(
        id='metric-chooser',
        options=[
            {'label': 'Watts', 'value': 'watts'},
            {'label': u'Watts/kg', 'value': 'watts-kg'},
        ],
        value='watts'),
    dcc.Graph(id='race_summary')
    ])

def build_round_viz(fig, selected_metric, df, round_num, row_num, zmin, zmax):
    fig.add_trace(go.Scatter(x=df[df['round'] == round_num]["dist_cumulative"], 
                            y=df[df['round'] == round_num]["elevation"], 
                            fill='tozeroy'), 
                            row=row_num * 2 - 1, 
                            col=1)
    fig.add_trace(go.Heatmap(
        x=df[df['round'] == round_num]['dist_cumulative'],
        y=[''],
        z=[df[df['round'] == round_num][selected_metric].values],
        zmin=zmin,
        zmax=zmax,
        showscale=True,
        colorscale='YlOrRd'), row=row_num * 2, col=1)
    
    return fig

@app.callback(
    Output('race_summary', 'figure'),
    [Input('metric-chooser', 'value')])
def update_figure(selected_metric):

    if selected_metric == 'watts':
        zmin = 100
        zmax = 450
    else:
        zmin = 1.5
        zmax = 7

    fig = make_subplots(rows = row_count, cols = 1, shared_xaxes=True)
    i = 1
    for round in rounds:
        fig = build_round_viz(fig, selected_metric, df, round, i, zmin, zmax)
        i += 1

    fig.update_layout(transition_duration=500, height=len(rounds)*200, width=800, showlegend=False)
    
    for row_num in [1,3,5,7]:
        fig.update_yaxes(range=[-10, 150], row=row_num, col=1)
    
    logging.info(fig)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
