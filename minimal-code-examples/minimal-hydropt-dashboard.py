# start in linux via
# export FLASK_APP=filename.py
# flask run

# start in windows via
# set FLASK_APP=filename.py
# flask run

import inspect, os
#os.environ["FLASK_APP"] = inspect.getfile(inspect.currentframe())
os.environ["OCTAVE_EXECUTABLE"] = "C:\\Octave\\Octave-4.2.2\\bin\\octave-cli.exe"

from oct2py import octave
from flask import Flask
from dash import Dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

flask_app = Flask(__name__)
dash_app = Dash(__name__, server=flask_app)

filepath = 'C:\\Users\\SEC\\Documents\\Alperia\\HydroptModel\\vsm.mod'
octave.eval("load('" + filepath + "', '-mat')")
globalData = octave.pull('Data')

dash_app.layout = html.Div(id='page-content', children=[
	dcc.Location(id='url', refresh=False)
])

@dash_app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
	return dash_router(pathname)
	
def dash_router(url):
	children = render_cockpit(globalData)
	return children
	
def render_cockpit(data):
	children = render_OverallReturn(data)
	return children
	
def render_OverallReturn(data):
	fPnl = data.Asset.ScenarioWaterManager.Result.OverallRevenue
	sUnit = 'CHF'
	frame = render_frame('Overall PnL')
	frame.children.append(render_kpi(fPnl, sUnit))
	return frame
		
def render_frame(sCaption):
	return html.Div(className = 'frame', children = [html.H2(sCaption, className = 'frame-caption')])
	
def render_kpi(fKPI, sUnit):
	sKPI = str(fKPI) + " " + sUnit
	return html.P(sKPI, className = 'KPI')
	