 # -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 12:22:38 2022

"""
#%%
import pandas as pd
import plotly.express as px
from dash import dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from plotly.offline import plot
#%%
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"

df = pd.read_csv(url)
pd.set_option('display.max_columns', None)
df.head()

dd1options = [{'label': value, 'value': value} for value in sorted(df['Launch Site'].unique())]


#%% start app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

#%% components
dd1options = [{'label': value, 'value': value} for value in sorted(df['Launch Site'].unique())]
dd1options.append({'label':'All Sites', 'value':'all'})
print(dd1options)
dropdown1 = dcc.Dropdown(id = 'dd1', multi=False, searchable = True, value='all', options = dd1options, className="m-5")

@app.callback(Output(component_id='piechart', component_property='figure'), 
              Input(component_id='dd1', component_property='value'))
def get_pie_chart(dd1value):
    if dd1value == 'all':
        dff = df.groupby('Launch Site').agg({'class':'sum'}).reset_index()
        fig = px.pie(dff, values = 'class', names ='Launch Site', title = 'success % by site')
        return fig
    else:
        dff = df[df['Launch Site']==dd1value]['class'].value_counts().rename_axis('unique_values').reset_index(name='counts')
        fig = px.pie(dff, values = 'counts', names ='unique_values', title = 'success percent in %s' % (dd1value))
        return fig
pie1 = dcc.Graph(id = 'piechart', figure={})

rangeslider1 = dcc.RangeSlider(id = 'rs1', min=0, max=10000, step=1000, 
                               marks={0:'0', 2500:'2500', 5000:'5000', 7500:'7500', 10000:'10000'}, 
                               value=[0, 100])

@app.callback(Output(component_id='scatter', component_property='figure'), 
              Input(component_id='dd1', component_property='value'),
              Input(component_id='rs1', component_property='value'))
def get_scatter(dd1value, rs1value):
    if dd1value == 'all':
        dff = df[df['Payload Mass (kg)'].between(rs1value[0], rs1value[1])]
        fig = px.scatter(dff, y = 'class', x = 'Payload Mass (kg)', color = 'Booster Version')
        return fig
    else:
        dff = df[(df['Launch Site']==dd1value) & (df['Payload Mass (kg)'].between(rs1value[0], rs1value[1]))]
        fig = px.scatter(dff, y = 'class', x = 'Payload Mass (kg)', color = 'Booster Version')
        return fig
scatter1 = dcc.Graph(id = 'scatter', figure={})

#%% layout
app.layout = dbc.Container([
    dbc.Row([dbc.Col([dropdown1], width={'size' : 6, 'offset' : 3})]),
    dbc.Row([dbc.Col([pie1], width = {'size': 6, 'offset': 3})]),
    dbc.Row([dbc.Col([rangeslider1], width = {'size': 6, 'offset': 3})]),
    dbc.Row([dbc.Col([scatter1], width = {'size': 12, 'offset': 0})])
    ])


#%% run
if __name__=='__main__':
    app.run_server(port=8000, debug = True)
