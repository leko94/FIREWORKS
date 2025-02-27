# Import necessary libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from flask import Response
import logging

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True, assets_folder='assets')
server = app.server  # Expose the server for WSGI

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Load your CSV dataset
data = pd.read_csv('DASH_ZA27022025.csv')

# Handle favicon.ico requests without a file
@server.route('/favicon.ico')
def favicon():
    # Return an empty response for favicon requests
    return Response(status=204)  # 204 No Content

# Paths for images (assuming they're in the assets folder)
logo1_path = '/assets/logo1.png'
logo2_path = '/assets/logo2.png'
logo3_path = '/assets/logo3.png'

# Top bar with logos
top_bar = html.Div([
    html.Img(src=logo1_path, style={'height': '300%', 'width': '300%', 'float': 'left'}),
    html.Img(src=logo3_path, style={'height': '300%', 'width': '300%', 'text-align': 'center'}),
    html.Img(src=logo2_path, style={'height': '300%', 'width': '300%', 'float': 'right'})
], style={'display': 'flex', 'justify-content': 'space-between'})

# Gauge for Total Number of Household Contacted
hh_num_count = data['hh_num'].count()
gauge1 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=hh_num_count,
    title={'text': "Total Number of Household Contacted and had Completed Interviews"},
    gauge={'axis': {'range': [0, 1500]}, 'bar': {'color': '#FF4500'}},  # Orange Red
    number={'valueformat': ','}
))

# Update the layout of the Dash App to make the gauge chart take up the full width
app.layout = html.Div([
    html.H1("Nutrint Dashboard", style={'text-align': 'center'}),
    top_bar,

    # Embed the fireworks video
    html.Video(
        src='/assets/fireworks.mp4',
        autoPlay=True,
        loop=True,
        muted=True,
        style={'width': '100%', 'height': 'auto', 'position': 'absolute', 'z-index': '-1'}
    ),

    # Add the Congratulations text with animation
    html.Div("Congratulations! You have reached your target Sample Size for Nutrint!",
             className="animated-text",
             style={
                 'position': 'relative',
                 'text-align': 'center',
                 'font-size': '48px',
                 'color': 'gold',
                 'z-index': '1',
                 'margin-top': '20px',
             }),

    # Add the gauge chart, modify to fit the full width
    dcc.Graph(figure=gauge1, style={'width': '105%', 'height': '400px', 'margin': '0', 'padding': '0'}),
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=False, port=8050)
