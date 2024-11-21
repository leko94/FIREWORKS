# -*- coding: utf-8 -*-
"""Untitled69.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lgizKdOAZ2qqqTsgpTKypSntshEQjxfI
"""

# Import necessary libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import logging

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True, assets_folder='assets')
server = app.server  # Expose the server for WSGI

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Load your CSV dataset
data = pd.read_csv('Nutrint_ZA21112024.csv')

# Paths for images - make sure your images are placed in the 'assets' folder
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

# Define the target sample size
TARGET_SAMPLE_SIZE = 1500

# Layout of the Dash App
app.layout = html.Div([
    html.H1("Nutrint Dashboard", style={'text-align': 'center'}),
    top_bar,
    dcc.Graph(figure=gauge1),

    # Fireworks container (hidden initially)
    html.Div(
        id="fireworks-container",
        children=[
            html.Div(
                "Congratulations! You have reached your target Sample Size for Nutrint!",
                id="congratulations-text",
                style={"display": "none"}  # Initially hidden
            )
        ],
        style={
            "position": "absolute", "top": 0, "left": 0, "width": "100%", "height": "100%",
            "z-index": 10, "background-color": "rgba(0, 0, 0, 0.5)", "display": "none"
        }  # Hidden initially
    ),
])

# Callback to show fireworks and congratulations text when target is reached
@app.callback(
    [Output("fireworks-container", "style"),
     Output("congratulations-text", "style")],
    [Input('gauge1', 'figure')]
)
def update_fireworks(gauge_figure):
    # Extract the gauge value (number of households contacted)
    value = gauge1.data[0]['value']

    # If the value meets or exceeds the target
    if value >= TARGET_SAMPLE_SIZE:
        # Show fireworks and blinking text
        return (
            {"display": "block"},  # Show fireworks container
            {"display": "block"}  # Show blinking text
        )
    # Hide both if target is not reached
    return ({"display": "none"}, {"display": "none"})

# Add CSS for animations
app.index_string = '''
<!DOCTYPE html>
<html>
<head>
    <title>Nutrint Dashboard</title>
    <style>
        /* Fireworks CSS */
        #fireworks-container {
            background: url('/assets/fireworks.gif') center no-repeat;
            background-size: cover;
        }

        /* Blinking text animation */
        @keyframes blinking-text {
            0% { opacity: 1; }
            50% { opacity: 0; }
            100% { opacity: 1; }
        }

        #congratulations-text {
            color: white;
            font-size: 2em;
            text-align: center;
            margin-top: 20%;
            animation: blinking-text 1s infinite;
        }
    </style>
</head>
<body>
    <div id="fireworks-container">
        <div id="congratulations-text"></div>
    </div>
    <div id="app">
        {%app_entry%}
    </div>
    <footer>
        {%config%}
        {%scripts%}
    </footer>
</body>
</html>
'''

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=False, port=8050)

pip install dash-bootstrap-components