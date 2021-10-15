#%%
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dash
from dash import html
from dash import dcc
from sklearn import preprocessing as pp
import os
#%%

app = dash.Dash(__name__)
server = app.server

# %%


ada = pd.read_csv('D:\Exploratory DA projects\ADA analysis\DATA\ADA_HistoricalData_1634132336365.csv')
ada['Date'] = pd.to_datetime(ada['Date'], format='%m/%d/%Y')
ada.columns = ada.columns.str.lower()

btc = pd.read_csv('D:\Exploratory DA projects\ADA analysis\DATA\BTC_HistoricalData_1634132449777.csv')
btc['Date'] = pd.to_datetime(btc['Date'], format='%m/%d/%Y')
btc.columns = btc.columns.str.lower()
#%%


ada.drop(columns='volume', inplace=True)
btc.drop(columns='volume', inplace=True)

#%%

ada.rename(columns={'close/last':'close'}, inplace=True)
btc.rename(columns={'close/last':'close'}, inplace=True)

#%%
min_max_scaler = pp.MinMaxScaler()
ada[['close_norm']] = pd.DataFrame(min_max_scaler.fit_transform(ada[['close']]))
btc[['close_norm']] = pd.DataFrame(min_max_scaler.fit_transform(btc[['close']]))

# %%


fig = go.Figure()
fig.add_trace(go.Scatter(x=ada.date, y=ada.close, mode='lines', name='CLOSE'))
#%%
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=ada.date, y=ada.close, mode='lines', name='CLOSE'))
fig2.add_trace(go.Scatter(x=ada.date, y=ada.high, mode='lines', name='HIGH'))
fig2.add_trace(go.Scatter(x=ada.date, y=ada.low, mode='lines', name='LOW'))

#%%
fig3=go.Figure()
fig3.add_trace(go.Scatter(x=ada.date, y=ada['close_norm'], mode='lines', name='ADA CLOSE'))
fig3.add_trace(go.Scatter(x=btc.date, y=btc['close_norm'], mode='lines', line=dict(color="darkmagenta"), name='BTC CLOSE'))


#%%
app.layout = html.Div(children=[
        html.Div([
                html.Div([
                        html.H1('ADA Analysis Dashboard', 
                            style={'textAlign' : 'center'})
                        ]),
                html.Div([
                        html.Div([
                                html.H2('ADA Closing Price', 
                                        style={'textAlign' : 'center', 
                                                'color' : '#503D36', 
                                                'font-size' : 30}), 
                                html.P('ADA price in USD',
                                        style={'textAlign' : 'center', 
                                                'color' : '#503D36', 
                                                'font-size' : 20}), 
                                dcc.Graph(figure=fig)],
                                className='six columns'),
                        

                        html.Div([
                                html.H2('ADA Daily Price Flactuations', 
                                        style={'textAlign' : 'center', 
                                                'color' : '#503D36', 
                                                'font-size' : 30}), 
                                html.P('ADA Price in USD',
                                        style={'textAlign' : 'center', 
                                                'color' : '#503D36', 
                                                'font-size' : 20}), 
                                dcc.Graph(figure=fig2)],
                                className='six columns'),
                        ], 
                                className='row'),

                html.Div([
                                html.H2('ADA vs BTC Trend Analysis', 
                                        style={'textAlign' : 'center', 
                                                'color' : '#503D36', 
                                                'font-size' : 30}), 
                                html.P('Prices Scaled from 0 to 1 for comparison',
                                        style={'textAlign' : 'center', 
                                                'color' : '#503D36', 
                                                'font-size' : 20}), 
                                dcc.Graph(figure=fig3)],                        
                                className='row')

                ])
                 
                
                        

        ])
        



                 


#%%                 
if __name__ == '__main__':
    app.run_server(debug=True)

