import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

df = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
    encoding='ISO-8859-1',
    dtype={'Div1Airport': str, 'Div1TailNum': str, 'Div2Airport': str, 'Div2TailNum': str}
)

data = df.sample(n=2000, random_state=42)

app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO, "https://use.fontawesome.com/releases/v5.15.4/css/all.css"])

COLORS = {
    'primary': '#1E88E5',
    'secondary': '#7C4DFF',
    'success': '#00C853',
    'danger': '#FF5252',
    'warning': '#FFD600',
    'info': '#00BCD4',
    'dark': '#263238',
    'light': '#ECEFF1'
}

card_style = {
    'backgroundColor': 'white',
    'borderRadius': '15px',
    'padding': '25px',
    'margin': '15px',
    'boxShadow': '0 8px 32px rgba(0,0,0,0.1)',
    'border': 'none'
}

header_style = {
    'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'padding': '40px 20px',
    'borderRadius': '0 0 30px 30px',
    'marginBottom': '30px',
    'boxShadow': '0 4px 20px rgba(0,0,0,0.15)'
}

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-plane-departure fa-3x", style={'color': 'white', 'marginRight': '15px'}),
                    html.H1('Airline Performance Dashboard', style={'color': 'white', 'display': 'inline', 'verticalAlign': 'middle', 'margin': '0'}),
                ], style={'textAlign': 'center', 'marginBottom': '10px'}),
                html.P('Comprehensive Analytics & Insights', style={'color': 'rgba(255,255,255,0.8)', 'fontSize': '18px', 'textAlign': 'center', 'margin': '0'}),
            ], width=12)
        ], style=header_style),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5('Controls', style={'fontWeight': 'bold', 'color': COLORS['dark'], 'marginBottom': '15px'}),
                    html.Label('Select Year:', style={'color': '#666', 'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='year-selector',
                        options=[{'label': y, 'value': y} for y in sorted(data['Year'].unique())],
                        value=data['Year'].unique()[0],
                        style={'marginBottom': '20px'}
                    ),
                    html.Label('Select Month Range:', style={'color': '#666', 'fontWeight': 'bold'}),
                    dcc.RangeSlider(
                        id='month-slider',
                        min=1, max=12, step=1,
                        value=[1, 12],
                        marks={i: str(i) for i in range(1, 13)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    html.Br(),
                    html.Label('Select Airlines:', style={'color': '#666', 'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='carrier-selector',
                        options=[{'label': c, 'value': c} for c in sorted(data['Reporting_Airline'].unique())],
                        value=sorted(data['Reporting_Airline'].unique())[:3],
                        multi=True,
                        style={'marginBottom': '20px'}
                    ),
                    html.Label('Min Delay Threshold:', style={'color': '#666', 'fontWeight': 'bold'}),
                    dcc.Slider(
                        id='delay-slider',
                        min=-50, max=100, step=5,
                        value=30,
                        marks={-50: '-50', 0: '0', 50: '50', 100: '100'}
                    ),
                    html.Div(id='delay-output', style={'marginTop': '10px', 'color': COLORS['primary'], 'fontWeight': 'bold'})
                ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '15px', 'margin': '10px'})
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.Div([html.I(className="fas fa-plane fa-2x", style={'color': COLORS['primary']})], style={'textAlign': 'center'}),
                    html.H4(id='stat-flights', style={'color': COLORS['primary'], 'margin': '0', 'fontSize': '24px', 'fontWeight': 'bold', 'textAlign': 'center'}),
                    html.P('Total Flights', style={'color': '#666', 'margin': '0', 'textAlign': 'center'})
                ])
            ], style={**card_style, 'textAlign': 'center'}, className="text-center"), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.Div([html.I(className="fas fa-clock fa-2x", style={'color': COLORS['warning']})], style={'textAlign': 'center'}),
                    html.H4(id='stat-depdelay', style={'color': COLORS['warning'], 'margin': '0', 'fontSize': '24px', 'fontWeight': 'bold', 'textAlign': 'center'}),
                    html.P('Avg Dep Delay', style={'color': '#666', 'margin': '0', 'textAlign': 'center'})
                ])
            ], style={**card_style, 'textAlign': 'center'}, className="text-center"), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.Div([html.I(className="fas fa-hourglass-half fa-2x", style={'color': COLORS['danger']})], style={'textAlign': 'center'}),
                    html.H4(id='stat-arrdelay', style={'color': COLORS['danger'], 'margin': '0', 'fontSize': '24px', 'fontWeight': 'bold', 'textAlign': 'center'}),
                    html.P('Avg Arr Delay', style={'color': '#666', 'margin': '0', 'textAlign': 'center'})
                ])
            ], style={**card_style, 'textAlign': 'center'}, className="text-center"), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.Div([html.I(className="fas fa-building fa-2x", style={'color': COLORS['success']})], style={'textAlign': 'center'}),
                    html.H4(id='stat-carriers', style={'color': COLORS['success'], 'margin': '0', 'fontSize': '24px', 'fontWeight': 'bold', 'textAlign': 'center'}),
                    html.P('Airlines', style={'color': '#666', 'margin': '0', 'textAlign': 'center'})
                ])
            ], style={**card_style, 'textAlign': 'center'}, className="text-center"), width=3)
        ]),
        
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5('Distance Groups by Selected Airlines', style={'fontWeight': 'bold', 'color': COLORS['dark']}), style={'backgroundColor': 'white', 'border': 'none'}),
                dbc.CardBody([dcc.Graph(id='carrier-chart', style={'height': '400px'})])
            ], style={**card_style, 'padding': '10px'}), width=5),
            
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5('Delay Comparison by Carrier', style={'fontWeight': 'bold', 'color': COLORS['dark']}), style={'backgroundColor': 'white', 'border': 'none'}),
                dbc.CardBody([dcc.Graph(id='delay-chart', style={'height': '400px'})])
            ], style={**card_style, 'padding': '10px'}), width=7)
        ]),
        
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5('Flight Distance Distribution', style={'fontWeight': 'bold', 'color': COLORS['dark']}), style={'backgroundColor': 'white', 'border': 'none'}),
                dbc.CardBody([dcc.Graph(id='distance-chart', style={'height': '350px'})])
            ], style={**card_style, 'padding': '10px'}), width=4),
            
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5('Top 10 Busiest Routes', style={'fontWeight': 'bold', 'color': COLORS['dark']}), style={'backgroundColor': 'white', 'border': 'none'}),
                dbc.CardBody([dcc.Graph(id='routes-chart', style={'height': '350px'})])
            ], style={**card_style, 'padding': '10px'}), width=4),
            
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5('Cancellation Reasons', style={'fontWeight': 'bold', 'color': COLORS['dark']}), style={'backgroundColor': 'white', 'border': 'none'}),
                dbc.CardBody([dcc.Graph(id='cancel-chart', style={'height': '350px'})])
            ], style={**card_style, 'padding': '10px'}), width=4)
        ]),
        
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5('Monthly Flight Trends', style={'fontWeight': 'bold', 'color': COLORS['dark']}), style={'backgroundColor': 'white', 'border': 'none'}),
                dbc.CardBody([dcc.Graph(id='monthly-chart', style={'height': '320px'})])
            ], style={**card_style, 'padding': '10px'}), width=6),
            
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5('Flights by US State', style={'fontWeight': 'bold', 'color': COLORS['dark']}), style={'backgroundColor': 'white', 'border': 'none'}),
                dbc.CardBody([dcc.Graph(id='map-chart', style={'height': '320px'})])
            ], style={**card_style, 'padding': '10px'}), width=6)
        ]),
        
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5('Delay Distribution Analysis', style={'fontWeight': 'bold', 'color': COLORS['dark']}), style={'backgroundColor': 'white', 'border': 'none'}),
                dbc.CardBody([dcc.Graph(id='violin-chart', style={'height': '300px'})])
            ], style={**card_style, 'padding': '10px'}), width=12)
        ])
        
    ], fluid=True, style={'backgroundColor': '#F5F7FA', 'minHeight': '100vh'})
])

@app.callback(
    [Output('stat-flights', 'children'),
     Output('stat-depdelay', 'children'),
     Output('stat-arrdelay', 'children'),
     Output('stat-carriers', 'children'),
     Output('carrier-chart', 'figure'),
     Output('delay-chart', 'figure'),
     Output('distance-chart', 'figure'),
     Output('routes-chart', 'figure'),
     Output('cancel-chart', 'figure'),
     Output('monthly-chart', 'figure'),
     Output('map-chart', 'figure'),
     Output('violin-chart', 'figure')],
    [Input('year-selector', 'value'),
     Input('month-slider', 'value'),
     Input('carrier-selector', 'value'),
     Input('delay-slider', 'value')]
)
def update_dashboard(year, month_range, carriers, delay_threshold):
    filtered = data[(data['Year'] == year) & 
                   (data['Month'] >= month_range[0]) & 
                   (data['Month'] <= month_range[1])]
    
    if carriers:
        if not isinstance(carriers, list):
            carriers = [carriers]
        filtered = filtered[filtered['Reporting_Airline'].isin(carriers)]
    
    filtered = filtered[filtered['DepDelay'] <= delay_threshold]
    
    stat_flights = f"{len(filtered):,}"
    stat_depdelay = f"{filtered['DepDelay'].mean():.1f} min" if len(filtered) > 0 else "N/A"
    stat_arrdelay = f"{filtered['ArrDelay'].mean():.1f} min" if len(filtered) > 0 else "N/A"
    stat_carriers = str(filtered['Reporting_Airline'].nunique()) if len(filtered) > 0 else "0"
    
    pie_fig = px.pie(filtered, values='Flights', names='DistanceGroup', hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Pastel)
    
    delay_by_carrier = filtered.groupby('Reporting_Airline')[['DepDelay', 'ArrDelay']].mean().reset_index()
    delay_fig = go.Figure(data=[
        go.Bar(name='Departure Delay', x=delay_by_carrier['Reporting_Airline'], 
               y=delay_by_carrier['DepDelay'], marker_color=COLORS['primary']),
        go.Bar(name='Arrival Delay', x=delay_by_carrier['Reporting_Airline'], 
               y=delay_by_carrier['ArrDelay'], marker_color=COLORS['danger'])
    ]).update_layout(barmode='group', template='plotly_white', height=380,
                     legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5))
    
    dist_fig = px.histogram(filtered, x='Distance', nbins=25, 
                           color_discrete_sequence=[COLORS['success']])
    dist_fig.update_layout(template='plotly_white', height=350, xaxis_title='Distance (miles)')
    
    routes = filtered.groupby(['OriginCityName', 'DestCityName']).size().reset_index(name='Flights')
    routes = routes.nlargest(10, 'Flights').assign(Route=lambda x: x['OriginCityName'].str.split(',').str[0] + ' → ' + x['DestCityName'].str.split(',').str[0])
    routes_fig = px.bar(routes, x='Flights', y='Route', orientation='h', color='Flights', 
                        color_continuous_scale='Blues', text='Flights')
    routes_fig.update_layout(template='plotly_white', height=350, showlegend=False, yaxis={'autorange': 'reversed'})
    routes_fig.update_traces(textposition='outside')
    
    cancel_fig = px.pie(filtered.dropna(subset=['CancellationCode']), names='CancellationCode', 
                        hole=0.5, color_discrete_sequence=px.colors.qualitative.Bold)
    cancel_fig.update_layout(template='plotly_white', height=350)
    
    monthly = filtered.groupby('Month')['Flights'].count().reset_index()
    monthly_fig = px.line(monthly, x='Month', y='Flights', markers=True, 
                          line_shape='spline', color_discrete_sequence=[COLORS['secondary']])
    monthly_fig.update_layout(template='plotly_white', height=320, xaxis=dict(tickmode='linear'))
    
    state_data = filtered.groupby('OriginState').size().reset_index(name='Flights')
    map_fig = px.choropleth(state_data, locations='OriginState', locationmode='USA-states', 
                           color='Flights', color_continuous_scale='Ice', scope='usa')
    map_fig.update_layout(template='plotly_white', height=320, geo=dict(bgcolor='rgba(0,0,0,0)'))
    
    violin_fig = go.Figure(data=[
        go.Violin(name='Departure Delay', y=filtered['DepDelay'].dropna(), 
                 box_visible=True, line_color=COLORS['primary'], fillcolor=f"rgba(30,136,229,0.4)", meanline_visible=True),
        go.Violin(name='Arrival Delay', y=filtered['ArrDelay'].dropna(), 
                 box_visible=True, line_color=COLORS['danger'], fillcolor=f"rgba(255,82,82,0.4)", meanline_visible=True)
    ]).update_layout(template='plotly_white', height=300, violinmode='group')
    
    return stat_flights, stat_depdelay, stat_arrdelay, stat_carriers, pie_fig, delay_fig, dist_fig, routes_fig, cancel_fig, monthly_fig, map_fig, violin_fig

if __name__ == '__main__':
    app.run(debug=True, port=8050)
