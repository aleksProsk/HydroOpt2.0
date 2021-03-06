#Anmerkung:
#Dieser Code funlt nicht so, wie er sollte -- weil Cookies nicht erzeugt werden (können?).
#In "try_to_login" sollte ein Cookie durch Flask erzeugt werden. Geht nicht.
#In dash_app.layout gibt's ein Script, das Cookies erstellt. Geht nicht.
#Dash sieht als Workaround die Verwendung von JSON-Datensätzen vor, die im HTML-Layout herumhängen.
#D.h., man speichert den Session-Status irgendwie darin.
#Alternativ könnte Dash in einem IFRame erzeugt werden (Master = Flask) und der Master schreibt Cookies, Dsah liest nur. Kommunikation via JSON ewtc.

# start in linux via
# export FLASK_APP=filename.py
# flask run

# start in windows via
# set FLASK_APP=filename.py
# flask run

from flask import Flask, request, make_response, render_template, redirect
from dash import Dash
from dash.dependencies import Input, Output, Event, State
import dash_html_components as html
import dash_core_components as dcc
import http.cookies

flask_app = Flask(__name__)
dash_app = Dash(__name__, server=flask_app)

colors = {
    'background': '#AB1111',
    'text': '#7FDBFF'
}

dash_app.layout = html.Div(id='universe', style={'backgroundColor': colors['background']}, children=[
	dcc.Location(id='url', refresh=False),
	html.Script("""
		function setCookie(name,value,days) {
			var expires = "";
			if (days) {
				var date = new Date();
				date.setTime(date.getTime() + (days*24*60*60*1000));
				expires = "; expires=" + date.toUTCString();
			}
			document.cookie = name + "=" + (value || "")  + expires + "; path=/";
		}""",
		type="text/JavaScript"),
	html.Div(id='main-page', style={'backgroundColor': colors['background']}, children=[
		html.Div(id='page-header', style={'backgroundColor': '#1B1111'}, children=[
			html.P(children=["Username: ", dcc.Input(type='text', id='username', placeholder='username')]),
			html.P(children=["Password: ", dcc.Input(type='password', id='password', placeholder='password')]),
			html.Button(id='submit-button', n_clicks=0, children='Login')
		]),
		html.Div(id='page-content', style={'backgroundColor': colors['background']}, children=[
			dcc.Location(id='url2', refresh=False)			
		])
	])
])


@dash_app.callback(
	Output('main-page', 'children'), 
	[Input('url', 'pathname'), Input('submit-button', 'n_clicks')],
	[State('username', 'value'), State('password', 'value')])
def display_page(pathname, n_clicks, username, password):
	isLoginAttempt = (n_clicks > 0)
	usernameFromCookie = request.cookies.get('username')
	isLoggedIn = usernameFromCookie is not None
	if not isLoggedIn and isLoginAttempt:
		try_to_login(username, password)
	return dash_router(pathname)
	
def try_to_login(username, password):
	print('trying to login with the following credentials:')
	print(username)
	print(password)
	resp = make_response(redirect('/'))
	resp.set_cookie('username', username)
	
def dash_router(pathname):
	username = request.cookies.get('username')
	print(username)
	isLoggedIn = username is not None
	pageContent = [
		html.H1(
			children='Dash routing',
			style={
				'textAlign': 'center',
				'color': colors['text']
			}
		),
		html.H2(children=pathname),
		html.H1(children='Username'),
		html.H2(children=username)			
	]
	
	children=[
		html.Div(id='page-header', style={'backgroundColor': '#1B1111'}, children=[
			html.P(children=["Username: ", dcc.Input(type='text', id='username', placeholder='username')]),
			html.P(children=["Password: ", dcc.Input(type='password', id='password', placeholder='password')]),
			html.Button(id='submit-button', children='Login')
		]),
		html.Div(id='page-content', style={'backgroundColor': colors['background']}, children=pageContent)
	]
	
	return children	