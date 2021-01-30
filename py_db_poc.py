# https://in.finance.yahoo.com/quote/%5ENSEI/components?p=%5ENSEI

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import pandas_datareader.data as web
from datetime import datetime
import pandas

app = dash.Dash()
server = app.server
nsdq = pandas.read_csv('data/NASDAQcompanylist.csv')
nsdq.set_index('Symbol',inplace=True)
options = []
for tic in nsdq.index:
    mydict = {}
    mydict['label'] = '{0} (1)'.format(str(nsdq.loc[tic]['Name']),tic)
    mydict['value'] = tic
    options.append(mydict)
app.layout = html.Div([
                html.H1('Stock ticker Dashboard'),
                html.Div([html.H3('Enter a stock symbol:',style={'paddingRight':'30px'}),
                dcc.Dropdown(id='my_stock_picker',
                          options=options,
                          value = ['TSLA'],
                            multi=True
                          )],
                         style={'display':'inline-block','verticalAlign':'top','width':'30%'}),
                html.Div([html.H3('Select a start and end date:'),
                          dcc.DatePickerRange(id='my_date_picker',
                                              min_date_allowed=datetime(2015,1,1),
                                              max_date_allowed=datetime.today(),
                                              start_date=datetime(2018,1,1),
                                              end_date=datetime.today())],
                         style={'display':'inline-block'}),
                html.Div([html.Button(id='submit-button',
                                      n_clicks=0,
                                      children='Submit',
                                      style={'fontSize':24, 'marginLeft':'30'})]
                         ,style={'display':'inline-block'}),
                dcc.Graph(id='my_graph',
                          figure={'data':[{'x':[1,2], 'y':[3,1]}],
                                  'layout':{'title':'Default Title'}})

])
@app.callback(Output('my_graph','figure'),
              [Input('submit-button','n_clicks')],
              [State('my_stock_picker','value'),
               State('my_date_picker','start_date'),
               State('my_date_picker', 'end_date')])
def update_graph(n_clicks,stock_ticker,start_date,end_date):
    start = datetime.strptime(start_date[:10],'%Y-%m-%d')
    end = datetime.strptime(end_date[:10],'%Y-%m-%d')
    traces = []
    for tic in stock_ticker:
        df = web.DataReader(tic, 'yahoo', start, end)
        traces.append({'x':df.index,'y':df['Adj Close'],'name':tic})

    fig = {'data':traces,
           'layout':{'title':stock_ticker}}
    return  fig


if __name__ == "__main__":
    app.run_server()