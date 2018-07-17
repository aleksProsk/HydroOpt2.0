# start in linux via
# export FLASK_APP=filename.py
# flask run

# start in windows via
# set FLASK_APP=filename.py
# flask run
# oder
# flask run --host=0.0.0.0 --port=4000


print("imports...")
import inspect, os
from shutil import copyfile
#os.environ["FLASK_APP"] = inspect.getfile(inspect.currentframe())
os.environ["OCTAVE_EXECUTABLE"] = "C:\\Octave\\Octave-4.4.0\\bin\\octave-cli.exe"
import copy
from oct2py import octave
from flask import Flask
from flask import send_from_directory
from dash import Dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
import random

from pandas import DataFrame, DatetimeIndex
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime

import plotly.graph_objs as go

from RestrictedPython import compile_restricted_function, safe_builtins, limited_builtins, utility_builtins

from pathlib import Path # für inline-io
from functools import lru_cache # für memoization

import infix
import funcy

@infix.div_infix
def m(f,x): return list(map(f,x))

@infix.div_infix
def M(f,g): return lambda x: f /m/ g(x)

@infix.div_infix
def c(*f): return funcy.compose(*f)

# Beispiel: (math.sin /c/ math.cos /c/ math.tan) /m/ [1,2,3]

@infix.div_infix
def a(f,x): return f(x)

def split(s): return lambda x: x.split(s)

def transpose(v): return list(map(list, zip(*v)))

def flatten(lis):
	"""Given a list, possibly nested to any level, return it flattened."""
	new_lis = []
	for item in lis:
		if type(item) == type([]):
			new_lis.extend(flatten(item))
		else:
			new_lis.append(item)
	return new_lis
	
print("classdefs...")

def get_current_uid():
	return 0	#todo
	
	
@lru_cache(maxsize=32) #todo: bei dateiänderungen nicht memoisieren, ggf änderungsdatum mitschicken als argument
def load_hydropt_data(filepath):
	print("load_hydopt_data")
	octave.eval("load('" + filepath + "', '-mat')") #todo: separate octave instanz für jeden user
	data = octave.pull('Data')
	return data
	
class CUser(object):
	def __init__(self, uid=None):
		if uid is None:
			self.__uid = get_current_uid()
		else:
			self.__uid = uid
	def getRights(self):return 0
	def getUID(self): return self.__uid

class CRestricted(object):
	__id = 0
	def getID(self): return str(self.__localID) #str(CRestricted.__id)
	def getNumberOfInstances(): return str(CRestricted.__id)
	getNumberOfInstances = staticmethod(getNumberOfInstances)
	def __init__(self, user): 
		self.__user = user
		CRestricted.__id += 1
		self.__localID = CRestricted.__id
	def getUser(self): return self.__user

class CHydropt(CRestricted):
	def __init__(self, user): 
		super().__init__(user)
		self.__assetNames = {
			'Alperia-VSM': 'Valle Selva Meloni',
			'Alpiq-FMHL': 'Hongrin-Léman',
			'TAH-TM': 'Testmodell'}
	def getData(self, filepath): 
		#todo: dynamsieren
		pathLookup = {
			'Alperia-VSM': 'models\\vsm.mod',
			'Alpiq-FMHL': 'models\\FMHLplus.mod',
			'TAH-TM': 'models\\Testmodell.mod'}
		return load_hydropt_data(pathLookup[filepath])
	def getAssetName(self, asset): return self.__assetNames[asset]
		
class CSafeNP(CRestricted):
	def __init__(self, user=CUser()): super().__init__(user)
	def min(self, v): return np.min(v)
	def max(self, v): return np.max(v)
	def hstack(self, v): return np.hstack(v)
	def vstack(self, v): return np.vstack(v)
	def arange(self, stop, start=0, step=1, dtype=None): return np.arange(start=start, stop=stop, step=step, dtype=dtype)
	def size(self, v) : return v.size

class CSafeDict(CRestricted):
	def __init__(self, dict, user=CUser()): 
		super().__init__(user)
		self.__d = dict
	def get(self, s): return self.__d[s]
	
class CSafeDateUtils(CRestricted):
	def __init__(self, user=CUser()): super().__init__(user)
	def to_datetime(self,v): return pd.to_datetime(v)
	def to_str(self, d) : return d.strftime("%Y-%m-%d %H:%M")
	def from_matlab(self,v): return date.fromordinal(int(v)) + timedelta(days=v%1) - timedelta(days = 366) #date.fromordinal(int(v-366))
	def date_range(self, start, end, freq='D', tz=None) : return pd.date_range(start=start, end=end, freq=freq, tz=tz)
	def date_range_from_matlab(self, start, end, freq='H', tz=None) : return self.date_range(start=self.from_matlab(start), end=self.from_matlab(end), freq=freq, tz=tz)
	def months_from_matlab(self, start, end) : return self.date_range_from_matlab(start=start, end=end, freq='MS')
	#df['python_datetime'] = df['matlab_datenum'].apply(lambda x: self.from_matlab(x))
	
class CSafeDF(CRestricted):
	def __init__(self, user=CUser()): super().__init__(user)
	def define(self, matrix, columns): self.__df = DataFrame(matrix, columns=columns)
	def to_dict(self, param): return self.__df.to_dict(param)
	def columns(self): return self.__df.columns

class CSafeLog(CRestricted):
	def __init__(self, user): super().__init__(user)
	def print(self,s): print(s)
	
class CGUIComponent(CRestricted):
	def __init__(self): 
		super().__init__(CUser())
		self.__children = []
	def getChildren(self): return self.__children
	def appendChild(self, c): self.__children.append(c)
	
class CDashComponent(CGUIComponent):
	def setDashRendering(self, r): self.__dashRendering = r
	def getDashRendering(self): return self.__dashRendering
	def appendChild(self,c): 
		super().appendChild(c)
		self.__dashRendering.children.append(c.getDashRendering())
	def aChild(self,c): self.appendChild(c)
	
class CFrame(CDashComponent): #todo: eindeutiger id-parameter 
	def __init__(self, sCaption, type = 'frame', isDynamic = True, width = 0.25, height = 0, smallScreenFactor = 2, tinyScreenFactor = 4, captionType = html.H2): 
		super().__init__()
		self._captionType = captionType
		self._caption = sCaption
		self._width = width
		self._height = height
		self._smallScreenFactor = smallScreenFactor
		self._tinyScreenFactor = tinyScreenFactor
		self._type = type
		if isDynamic: self._type = type + ' grid-item varsize' + '-' + str(round(width*100)) + '-' + str(round(height*100)) + '-' + str(round(smallScreenFactor)) + '-' + str(round(tinyScreenFactor))
		self.setCaption(sCaption)
	def getCaption(self): return self._caption
	def setCaption(self, sCaption): super().setDashRendering(html.Div(className = self._type, children = [self._captionType(sCaption, className = 'frame-caption')]))

class CNavigationPane(CDashComponent): 
	def __init__(self, nestedLinkList): 
		super().__init__()
		self.setNavigationTree(nestedLinkList)
	def getNavigationTree(self): return self.__nestedLinkList
	def setNavigationTree(self, nestedLinkList): 
		self.__nestedLinkList = nestedLinkList
		#nestedLinkList = [['Screens', [['Result overview', 'url'], ['Engine results', 'url']]], ['Assets', [['VSM', 'url'], ['NdD', 'url']]]]
		linkRendering =  flatten((lambda x: [html.P(str(x[0])+': ', className = 'no-break'), (lambda y: html.A(html.Button(y[0], className=y[2]), href=y[1])) /m/ x[1]]) /m/ nestedLinkList)
		super().setDashRendering(html.Div(className = 'navigation-pane', children = linkRendering))
	
class CPage(CFrame): #todo: eindeutiger id-parameter 
	def __init__(self, sCaption): 
		super().__init__(sCaption, type = 'content', isDynamic = False, captionType = html.H1)
		
		
class CText(CDashComponent):
	def __init__(self, text): 
		super().__init__()
		self.setText(text)
	def getText(self): return self.__text
	def setText(self, text): 
		self.__text = text
		super().setDashRendering(html.P(str(text), className = 'text', id=str(super().getID())))  
		
class CStopWaitingForGraphics(CDashComponent):
	def __init__(self): 
		super().__init__()
		super().setDashRendering(html.P("", className = 'CStopWaitingForGraphics'))	

class CNumber(CText):
	def __init__(self, value, unit):
		super().__init__(str(value) + " " + unit)
		self.__value = value
		self.__unit = unit
		self.setValue(value, unit)
	def getValue(self): return self.__value
	def setValue(self, value, unit=None): 
		if unit is None: unit=self.__unit
		super().setText(str(value) + " " + unit)
		self.__value = value
		self.__unit = unit
		
class CNumbers(CText):
	def __init__(self, keys_values_units, separator = '│'):
		self.__keys_values_units = keys_values_units
		self.__separator = separator
		super().__init__(self._getText())
	def _getText(self): return (' ' + self.__separator + ' ').join((lambda x: x[0] + ': ' + str(x[1]) + ' ' + x[2]) /m/ self.__keys_values_units)
	
class CDataTable(CDashComponent):
	def __init__(self, rows, headers): 
		super().__init__()
		self.__np = CSafeNP(super().getUser())
		self.__df = CSafeDF(super().getUser())
		self.setTable(rows, headers)
	def getRows(self): return self.__rows
	def getHeaders(self): return self.__headers
	def __setValues(self, rows): self.__values = self.__np.hstack(rows)
	def setTable(self, rows, headers):
		self.__setValues(rows)
		self.__df.define(self.__values, columns=headers)
		self.__dt = dt.DataTable(
			rows=self.__df.to_dict('records'),
			#optional - sets the order of columns
			#columns=sorted(self.__df.columns()),
			row_selectable=True,
			filterable=True,
			sortable=True,
			selected_row_indices=[]#,
			#id='datatable-gapminder' todo
		)
		self.__rows = rows
		self.__headers = headers
		super().setDashRendering(self.__dt)
		
BASIC_GRAPH_LAYOUT = dict(
	autosize=True,
	height=500,
	#font=dict(color='#CCCCCC'),
	#titlefont=dict(color='#CCCCCC', size='14'),
	margin=dict(l=35, r=35, b=35, t=45),
	hovermode="closest",
	plot_bgcolor="#F9FAFA",
	paper_bgcolor="#F2F2F2",
	legend=dict(font=dict(size=10), orientation='h'),
	title='Satellite Overview'#,
	#mapbox=dict(
	#	accesstoken=mapbox_access_token,
	#	style="dark",
	#	center=dict(
	#		lon=-78.05,
	#		lat=42.54
	#	),
	#	zoom=7,
	#)
)

class CChart(CDashComponent):
	def __init__(self, rows, headers, rowCaptions, title, type='bar', barmode='group'): 
		super().__init__()
		self.setChart(rows, headers, rowCaptions, title, type, barmode)
	def getRows(self): return self.__rows
	def getHeaders(self): return self.__headers
	def getRowCaptions(self): return self._rowCaptions
	def _setParams(self, rows, headers, rowCaptions, title, type='bar', barmode='group'):
		self.__rows = rows
		self.__headers = headers
		self._isTimeSeries = isinstance(rowCaptions, DatetimeIndex)
		self._rowCaptions = rowCaptions if self._isTimeSeries else rowCaptions.flatten()
		self.__title = title
		self.__type = type
		self.__barmode = barmode
	def _setDataMap(self): self._dataMap = lambda x: {'x': self._rowCaptions, 'y': x[0], 'name': x[1], 'type': self.__type}
	def _setDataVec(self): self._dataVec = (lambda x: [x[0].flatten(), x[1]]) /m/ transpose([self.__rows, self.__headers])  #list(map(lambda x: [x[0].flatten(), x[1]], transpose([self.__rows, self.__headers])))
	def _setData(self):	self._data = self._dataMap /m/ self._dataVec #list(map(self._dataMap, self._dataVec))
	def _setLayout(self):
		self.__layout = copy.deepcopy(BASIC_GRAPH_LAYOUT)
		self.__layout['title'] = self.__title
		self.__layout['barmode'] = self.__barmode
		if self._isTimeSeries: 
			self.__layout['xaxis'] = dict(rangeselector=dict(
				buttons=list([
					dict(count=1, label='1d', step='day', stepmode='backward'),
					dict(count=7, label='1w', step='day', stepmode='backward'),
					dict(count=1, label='1m', step='month', stepmode='backward'),
					dict(count=6, label='6m', step='month', stepmode='backward'),
					dict(count=12, label='1y', step='month', stepmode='backward'),
					dict(step='all')])),
				rangeslider=dict(), type='date')
	def _setFigure(self): self.__figure = {'data': self._data, 'layout': self.__layout}
	def _getFigure(self): return self.__figure
	def setChart(self, rows, headers, rowCaptions, title, type='bar', barmode='group'):
		self._setParams(rows, headers, rowCaptions, title, type, barmode)
		self._setDataMap()
		self._setDataVec()
		self._setData()
		self._setLayout()
		self._setFigure()
		chart = dcc.Graph(id=super().getID(), figure=self._getFigure())
		super().setDashRendering(chart)
		
def update_output_A(start_date, end_date):
	print("callb")
	string_prefix = 'You have selected: '
	if start_date is not None:
		start_date = datetime.strptime(start_date, '%Y-%m-%d')
		start_date_string = start_date.strftime('%B %d, %Y')
		string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
	if end_date is not None:
		end_date = datetime.strptime(end_date, '%Y-%m-%d')
		end_date_string = end_date.strftime('%B %d, %Y')
		string_prefix = string_prefix + 'End Date: ' + end_date_string
	if len(string_prefix) == len('You have selected: '):
		return 'Select a date to see it displayed here'
	else:
		return string_prefix
		
class CDatePicker(CDashComponent):
	#Initialising function
	def __init__(self, callb=update_output_A, output=None, outputParam='children', minDate=(1995, 8, 5), maxDate=(2017, 9, 19), startDate=(2017, 8, 5), endDate=(2017, 8, 25), retrieveOldValue=False): 
		super().__init__()
		self.setDatePicker(callb, output, outputParam, minDate, maxDate, startDate, endDate)
	#Updating function. It is called every time user changes the time range to store current information about date range
	def internal_update(self):
		def changeData(start_date, end_date):
			if start_date is not None:
				self.__start_date = start_date
			if end_date is not None:
				self.__end_date = end_date
			print('lol')
		return changeData
	#Wrapper to get the layout of object
	def getRendering(self): return self.__rendering
	#These are the functions to get decorators for callbacks
	def __getCallbDecorator(self): 
		outp = None
		if self.__output is None:
			outp = 'none-' + str(super().getID())
		else:
			outp = self.__output.getID()
		print(self.__output.getID())
		print(self.__outputParam)
		print(super().getID())
		return (
			Output(str(outp), self.__outputParam),
			[Input('my-date-picker-range-' + str(super().getID()), 'start_date'),
			 Input('my-date-picker-range-' + str(super().getID()), 'end_date')])
	def __getFakeCallbDecorator(self):
		return (
		Output('fake-container-' + str(super().getID()), 'children'),
		[Input('my-date-picker-range-' + str(super().getID()), 'start_date'),
		 Input('my-date-picker-range-' + str(super().getID()), 'end_date')])
	#Wrapper for a callback function
	def getCallback(self): return self.__cb
	#Creating callbacks for object
	def __registerCallb(self):
		print('register callbacks in datepicker')
		dash_app.callback(*self.__getFakeCallbDecorator())(self.internal_update())
		#dash_app.callback(*self.__getCallbDecorator())(self.getCallback())
	#Function to receive the date range
	def getSelectedRange(self):
		return [self.__start_date, self.__end_date]
	def setDatePicker(self, callb, output, outputParam, minDate, maxDate, startDate, endDate):
		self.__cb = callb
		self.__start_date = datetime(*startDate).date()
		self.__end_date = datetime(*endDate).date()
		self.__output = output
		self.__outputParam = outputParam
		super().setDashRendering(html.Div([dcc.DatePickerRange(
			id='my-date-picker-range-' + str(super().getID()),
			min_date_allowed=datetime(*minDate),
			max_date_allowed=datetime(*maxDate),
			initial_visible_month=datetime(*startDate),
			end_date=datetime(*endDate).date(),
			start_date=datetime(*startDate).date()),
			html.Div(id='fake-container-' + str(super().getID()), style={'display':'none'})]))
		self.__registerCallb()
		


@lru_cache(maxsize=32)
def crf_mem(body, name): return compile_restricted_function(p = '', body = body, name = name, filename = '<inline code>')
		
def load_script(scriptpath, additional_globals, safe_locals, name):
	myscript = Path(scriptpath).read_text()
	cr = crf_mem(myscript, name)#compile_restricted_function(p = '', body = myscript, name = name, filename = '<inline code>')
	safe_globals = safe_builtins
	safe_globals.update(additional_globals)
	exec(cr.code, safe_globals, safe_locals)
	return safe_locals[name]

class HDict(dict): 
	def __hash__(self): return hash(str(self))#hash(frozenset(self.items()))  #hashable dictionary
	


#@lru_cache(maxsize=32) todo führt dazu, dass seite nicht neu geladen wird
def load_script_uid(scriptpath, name, uid, args):
	user = CUser(uid)
	globals = {
		'hydropt' : CHydropt(user), 
		'html' : html, 
		'dt' : dt, 
		'np' : CSafeNP(user), 
		'df' : CSafeDF(user), 
		'log' : CSafeLog(user), 
		'CFrame' : CFrame, 
		'CNumber' : CNumber,
		'CDataTable' : CDataTable,
		'CChart' : CChart,
		'dateUtils' : CSafeDateUtils(),
		'CPage': CPage,
		'CText': CText,
		'CStopWaitingForGraphics': CStopWaitingForGraphics,
		'CNumbers': CNumbers,
		'datePicker': datePicker,
		'args':CSafeDict(args, user=user)}
	return load_script(scriptpath, globals, {}, name)
	
def getSubdirs(path):
	return next(os.walk(path))[1]

class CInits(object):
	__numOfInstances = 0
	def __init__(self, user, args):
		#Kompilieren der Hauptfunktion
		print("init")
		scriptpath = 'user001\\scripts\\dash\\screens\\' + args['screen'] + '\\render.py'
		self.hydropt = CHydropt(user)
		self.__user = user
		self.__args = args
		self.render_pointer = load_script_uid(scriptpath, 'render', user.getUID(), HDict(args))
		CInits.__numOfInstances += 1
	def getArgs(self): return self.__args
	def getNumOfInstances():
		return CInits.__numOfInstances
	getNumOfInstances = staticmethod(getNumOfInstances)

dt0 = dt.DataTable(
	rows=[{0: 0}],
	row_selectable=False,
	filterable=False,
	sortable=False,
	selected_row_indices=[],
	id=str(hash('dt0'))
)



print("start servers...")
flask_app = Flask(__name__)
dash_app = Dash(__name__, server=flask_app, url_base_pathname='/d/')

print("start dash...")

dash_app.layout = html.Div(id='page-content', children=[dcc.Location(id='url', refresh=False), dt0])

dash_app.css.config.serve_locally = False
dash_app.scripts.config.serve_locally = False
dash_app.config.supress_callback_exceptions = True

#copy css and js files to static folder
STATIC_FOLDER = os.path.join(os.getcwd(), 'static') #'/cygdrive/c/Users/Aleksandr Proskurin/Documents/work/MyDashFiles/static/' #todo temporäres verzeichnis ("with tempfile.TemporaryDirectory() as dirpath:")
STATIC_URL = '/static/'
CSS_PATHS = [
	'CSS/stylesheet-oil-and-gas.css',
	'CSS/jquery-ui-1.12.1/jquery-ui.css',
	'mynodefiles/myapp3/node_modules/jquery.mmenu/dist/css/jquery.mmenu.all.css',
	'mynodefiles/myapp3/node_modules/flickity/dist/flickity.css',
	'Beispiel-HTMLs/stylesheets/demo.css']
JS_PATHS = [
	'mynodefiles/jquery-zeug/node_modules/jquery/dist/jquery.js',
	'CSS/jquery-ui-1.12.1/jquery-ui.js',
	'mynodefiles/myapp3/node_modules/jquery.mmenu/dist/js/jquery.mmenu.min.js',
	'mynodefiles/myapp3/node_modules/jquery.mmenu/dist/js/jquery.mmenu.all.min.js',
	'mynodefiles/myapp3/node_modules/flickity/dist/flickity.pkgd.min.js',
	'mynodefiles/isotope-zeug/node_modules/isotope-layout/dist/isotope.pkgd.min.js',
	'initialize-isotope.js']

(lambda x: copyfile(x, os.path.join(STATIC_FOLDER, os.path.basename(x)))) /m/ (CSS_PATHS + JS_PATHS)
(lambda x: dash_app.css.append_css			({"external_url": STATIC_URL + x})) /m/ (os.path.basename /m/ CSS_PATHS)
(lambda x: dash_app.scripts.append_script	({"external_url": STATIC_URL + x})) /m/ (os.path.basename /m/ JS_PATHS)

datePicker = CDatePicker()

@flask_app.route('/')
def hello_world():
	return 'Index page'

#@dash_app.server.route('/static/<path:path>')
@flask_app.route(STATIC_URL + '<path>')
def static_file(path): return send_from_directory(STATIC_FOLDER, path)
	
@flask_app.route('/user/<username>')
def show_user_profile(username):
	# show the user profile for that user
	return 'User %s' % username

class CUrlProcessor(CRestricted):
#bsp. path: http://localhost:5000/d/DisplayScreen@screen=ResultOverview&theme=grey/CalcFourier@data=data
	def __init__(self, sUrl, sBasePath, sFuncSplitter='/', sHeadSplitter='@', sArgsSplitter='&', sKeyValueSplitter='=', user=CUser()):
		super().__init__(user)
		
		self.hasFunctionCalls = False
		self.callStringList = []
		self.numberOfFunctionCalls = 0
		self.nestedCallList = []
		self.argList = []
		self.funcList = []
		self.results = None
		self.dashResult = None
		
		baseSplit = sUrl.split(sBasePath)
		self.hasFunctionCalls = len(baseSplit) > 1
		if self.hasFunctionCalls:
			callString = ''.join(baseSplit[1:])
			self.callStringList = callString.split(sFuncSplitter)
			self.numberOfFunctionCalls = len(self.callStringList)
			if self.numberOfFunctionCalls > 0:
				self.nestedCallList = (lambda x: [flatten(x[0]), dict(x[1])]) /m/ (split(sKeyValueSplitter) /M/ split(sArgsSplitter) /M/ split(sHeadSplitter) /M/ split(sFuncSplitter))(callString)
				self.funcList = transpose(self.nestedCallList)[0]
				self.argList = transpose(self.nestedCallList)[1]
				#callString='f&g?a=x&b=y/h?c=z/d?u=ux' -> [[['f', 'g'], {'a': 'x', 'b': 'y'}], [['h'], {'c': 'z'}], [['d'], {'u': 'ux'}]]
				
				#callString = 'f&g?a=x&b=y/h?c=z/d?x'
				#self.nestedCallList = list(map(lambda x: list(map(lambda y: list(map(lambda z: z.split('='), y.split('&'))), x.split('?'))), callString.split('/')))
				# -> [[[['f'], ['g']], [['a', 'x'], ['b', 'y']]], [[['h']], [['c', 'z']]], [[['d']], [['x']]]]
		
		self.sDashFunction = 'DisplayScreen'
		self.hasDashFunction = [self.sDashFunction] in self.funcList
		self.idxDashFunction = self.funcList.index([self.sDashFunction]) if self.hasDashFunction else None
		self.fDash = dash_router /c/ (lambda x: CInits(user, x))
		
		self.funcLookup = {}
		self.funcLookup[self.sDashFunction] = self.fDash
		
	def run(self): 
		if self.hasFunctionCalls: 
			print((lambda x: x[0]) /m/ self.nestedCallList)
			def buildFuncComposition(fstrings): return funcy.compose(*(lambda fstring: self.funcLookup[fstring]) /m/ fstrings)
			self.result = (lambda x: buildFuncComposition(x[0])(x[1])) /m/ self.nestedCallList #bildet (fi1@*fi2@*...)(xi1, xi2, ...) für alle i = 1, ..., numberOfFunctionCalls
			self.dashResult = self.result[self.idxDashFunction]
				
@dash_app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
	print("display_page ")
	uid = 1
	user = CUser(uid)
	if pathname is None: return None
	urlProcessor = CUrlProcessor(pathname, dash_app.url_base_pathname, user = user)
	#inits = CInits(user, 'C:\\Users\\Aleksandr Proskurin\Documents\\work\\MyDashFiles\\user001\\scripts\\dash\\screens\\'+pathname.split("/")[-1])
	#return dash_router(inits, pathname)
	urlProcessor.run()
	return urlProcessor.dashResult

def dash_router(inits, url=''):
	children = []
	if inits.render_pointer is not None:
		screenComponents = inits.render_pointer(*[], **{})
		menu = [
			['Screens', [
				['Result overview', '/d/DisplayScreen@screen=ResultOverview&asset='+inits.getArgs()['asset'], 'menu-item-active' if inits.getArgs()['screen'] == 'ResultOverview' else 'menu-item'], 
				['Engine results', '/d/DisplayScreen@screen=EngineResults&asset='+inits.getArgs()['asset'], 'menu-item-active' if inits.getArgs()['screen'] == 'EngineResults' else 'menu-item']]], 
			['Assets', [
				['Valle Selva Meloni', '/d/DisplayScreen@asset=Alperia-VSM&screen='+inits.getArgs()['screen'], 'menu-item-active' if inits.getArgs()['asset'] == 'Alperia-VSM' else 'menu-item'], 
				['Hongrin-Léman', '/d/DisplayScreen@asset=Alpiq-FMHL&screen='+inits.getArgs()['screen'], 'menu-item-active' if inits.getArgs()['asset'] == 'Alpiq-FMHL' else 'menu-item'],
				['Testmodell',  '/d/DisplayScreen@asset=TAH-TM&screen='+inits.getArgs()['screen'], 'menu-item-active' if inits.getArgs()['asset'] == 'TAH-TM' else 'menu-item']]]]
		navPane = CNavigationPane(menu)
		if screenComponents is not None:
			children = [navPane.getDashRendering(), screenComponents.getDashRendering()]
		else:
			print("error rendering screen " + url)
	else:
		print("render-pointer is none")
	return children
#http://localhost:5000/d/DisplayScreen@screen=ResultOverview&asset=Alperia-VSM
#http://localhost:5000/d/DisplayScreen@screen=test
	
'''
dash_app.callback( 
	Output('12', 'children'),
	[Input('my-date-picker-range-' + str("13"), 'start_date'),
	Input('my-date-picker-range-' + str("13"), 'end_date')])(update_output_A)
	
	
dash_app.callback( 
	Output('StaticOutputDivId', 'children'),
	[Input('StaticInputDivId', 'll')])(dashOutputRouter)
	
def dashOutputRouter(x):
	x => (f, args)
	f(args) => y => divifiedy
	return divifiedy
'''

'''
@dash_app.callback(Output('fake-container-' + str(13), 'children'),
		[Input('my-date-picker-range-' + str(13), 'start_date'),
		 Input('my-date-picker-range-' + str(13), 'end_date')])
def tmp(a, b):
	print('lol')
'''