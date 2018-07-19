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

from RestrictedPython import compile_restricted_function, safe_builtins, limited_builtins, utility_builtins, compile_restricted

from pathlib import Path # für inline-io
from functools import lru_cache # für memoization

from parser import parse
from compile_callbacks import compile_callbacks
from readObjects import readObjects
import infix
import funcy
import base64
import io

def safeSplit(separator, string, num):
    return string.split(separator)[num]

dictionaryOfAllScreenVariables = {}

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

def getScreenNames(uid):
	path = "user" + uid + "/scripts/dash/screens/"
	screenNames = []
	for root, dirs, files in os.walk(path, topdown=False):
		for name in dirs:
			screenNames.append(os.path.join(name))
	return screenNames

def getNameFromId(id):
	name, type, screen = id.split('-')
	return name

def getTypeFromId(id):
	name, type, screen = id.split('-')
	return type

def generateId(name, type, screen):
	print(name, type, screen)
	return name + '-' + type + '-' + screen

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
	def __init__(self, user, name = None, screenName = None):
		self.__user = user
		CRestricted.__id += 1
		if name is None and screenName is None:
			self.__localID = CRestricted.__id
		else:
			self.__localID = generateId(name, self.__class__.__name__, screenName)
			cur_uid = str(self.getUser().getUID())
			if cur_uid not in dictionaryOfAllScreenVariables:
				dictionaryOfAllScreenVariables[cur_uid] = {}
			if screenName not in dictionaryOfAllScreenVariables[cur_uid]:
				dictionaryOfAllScreenVariables[cur_uid][screenName] = CSafeDict({})
			dictionaryOfAllScreenVariables[cur_uid][screenName].set(name, self)
			print('Added ', name, ' to dict with uid = ', cur_uid, ' screen = ', screenName)
		print('name: ', name)
		print('screenName: ', screenName)
		print('classname: ', self.__class__.__name__)
		print('id: ', self.__localID)
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
	def getDict(self): return self.__d
	def set(self, key, value): self.__d[key] = value

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
	def __init__(self, name, screenName):
		super().__init__(CUser(), name, screenName)
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
	def __init__(self, sCaption, type = 'frame', isDynamic = True, width = 0.25, height = 0, smallScreenFactor = 2,
                 tinyScreenFactor = 4, captionType = html.H2, name = None, screenName = None):
		super().__init__(name, screenName)
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
	def __init__(self, nestedLinkList, name = None, screenName = None):
		super().__init__(name, screenName)
		self.setNavigationTree(nestedLinkList)
	def getNavigationTree(self): return self.__nestedLinkList
	def setNavigationTree(self, nestedLinkList):
		self.__nestedLinkList = nestedLinkList
		#nestedLinkList = [['Screens', [['Result overview', 'url'], ['Engine results', 'url']]], ['Assets', [['VSM', 'url'], ['NdD', 'url']]]]
		linkRendering =  flatten((lambda x: [html.P(str(x[0])+': ', className = 'no-break'), (lambda y: html.A(html.Button(y[0], className=y[2]), href=y[1])) /m/ x[1]]) /m/ nestedLinkList)
		super().setDashRendering(html.Div(className = 'navigation-pane', children = linkRendering))
	
class CPage(CFrame): #todo: eindeutiger id-parameter 
	def __init__(self, sCaption, name = None, screenName = None):
		super().__init__(sCaption, type = 'content', isDynamic = False, captionType = html.H1, name = name, screenName = screenName)
		
		
class CText(CDashComponent):
	def __init__(self, text, name = None, screenName = None):
		super().__init__(name, screenName)
		self.update(text)
	def getText(self): return self.__text
	def update(self, text):
		self.__text = text
		super().setDashRendering(html.P(str(text), className = 'text', id=str(super().getID())))
		
class CStopWaitingForGraphics(CDashComponent):
	def __init__(self, name = None, screenName = None):
		super().__init__(name, screenName)
		super().setDashRendering(html.P("", className = 'CStopWaitingForGraphics'))	

class CNumber(CText):
	def __init__(self, value, unit, name = None, screenName = None):
		super().__init__(str(value) + " " + unit, name = name, screenName = screenName)
		self.__value = value
		self.__unit = unit
		self.update(value, unit)
	def getValue(self): return self.__value
	def update(self, value, unit=None):
		if unit is None: unit=self.__unit
		super().update(str(value) + " " + unit)
		self.__value = value
		self.__unit = unit
		
class CNumbers(CText):
	def __init__(self, keys_values_units, separator = '│', name = None, screenName = None):
		self.__keys_values_units = keys_values_units
		self.__separator = separator
		super().__init__(self._getText(), name = name, screenName = screenName)
	def _getText(self): return (' ' + self.__separator + ' ').join((lambda x: x[0] + ': ' + str(x[1]) + ' ' + x[2]) /m/ self.__keys_values_units)
	
class CDataTable(CDashComponent):
	def __init__(self, rows, headers, name = None, screenName = None):
		super().__init__(name, screenName)
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
	def __init__(self, rows, headers, rowCaptions, title, type='bar', barmode='group',
                 name = None, screenName = None):
		super().__init__(name, screenName)
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

class CDatePickerRange(CDashComponent):
	#Initialising function
	def __init__(self, minDate = (1995, 8, 5), maxDate = (2017, 9, 19), startDate = (2017, 8, 5), endDate = (2017, 8, 25),
				 name = None, screenName = None):
		super().__init__(name, screenName)
		self.setDatePickerRange(minDate, maxDate, startDate, endDate)
	def update(self, start_date = None, end_date = None):
		if start_date is not None:
			self.__start_date = start_date
		if end_date is not None:
			self.__end_date = end_date
	def getSelectedRange(self):
		return [self.__start_date, self.__end_date]
	def setDatePickerRange(self, minDate, maxDate, startDate, endDate):
		self.__start_date = datetime(*startDate).date()
		self.__end_date = datetime(*endDate).date()
		super().setDashRendering(dcc.DatePickerRange(
			id=str(super().getID()),
			min_date_allowed=datetime(*minDate),
			max_date_allowed=datetime(*maxDate),
			initial_visible_month=datetime(*startDate),
			end_date=datetime(*endDate).date(),
			start_date=datetime(*startDate).date())
		)

class CDatePickerSingle(CDashComponent):
	def __init__(self, minDate=(1995, 8, 5), maxDate = (2017, 9, 19), date = (2017, 8, 5),
				 name = None, screenName = None):
		super().__init__(name, screenName)
		self.setDatePickerSingle(minDate, maxDate, date)
	def getValue(self):
		return self.__date
	def update(self, date = None):
		if date is not None:
			self.__date = date
	def setDatePickerSingle(self, minDate, maxDate, date):
		self.__minDate = datetime(*minDate).date()
		self.__maxDate = datetime(*maxDate).date()
		self.__date = datetime(*date).date()
		super().setDashRendering(dcc.DatePickerSingle(
			id=str(super().getID()),
			min_date_allowed=datetime(*minDate),
			max_date_allowed=datetime(*maxDate),
			initial_visible_month=datetime(*date),
			date=datetime(*date).date())
		)

class CDropdown(CDashComponent):
	def __init__(self, options = [], placeholder = 'Select', value = '', multi = False,
				 name = None, screenName = None, height = 'auto', width = 'auto'):
		super().__init__(name, screenName)
		self.setDropdown(options, placeholder, value, multi, height, width)
	def getValue(self):
		return self.__value
	def update(self, value):
		self.__value = value
	def setDropdown(self, options, placeholder, value, multi, height, width):
		self.__options = options
		self.__placeholder = placeholder
		self.__value = value
		self.__multi = multi
		self.__height = height
		self.__width = width
		st = {'height': height, 'width': width}
		super().setDashRendering(html.Div([dcc.Dropdown(
			id=str(super().getID()),
			options=options,
			placeholder=placeholder,
			multi=multi,
			value=value,
		)], style=st))

class CSlider(CDashComponent):
	def __init__(self, dots = False, marks = {}, min = 0, max = 100, step = 1, value = None, vertical = False,
				 name = None, screenName = None, height = 'auto', width = 'auto'):
		if value is None:
			value = max
		super().__init__(name, screenName)
		self.setSlider(dots, marks, min, max, step, value, vertical, height, width)
	def getValue(self):
		return self.__value
	def update(self, value):
		self.__value = value
	def setSlider(self, dots, marks, min, max, step, value, vertical, height, width):
		self.__dots = dots
		self.__marks = marks
		self.__min = min
		self.__max = max
		self.__step = step
		self.__value = value
		self.__vertical = vertical
		self.__height = height
		self.__width = width
		st = {'height': height, 'width': width}
		super().setDashRendering(html.Div([dcc.Slider(
			id=str(super().getID()),
			dots=dots,
			marks=marks,
			min=min,
			max=max,
			step=step,
			value=value,
			vertical=vertical,
		)], style=st))

class CRangeSlider(CDashComponent):
	def __init__(self, allowCross = False, dots = False, marks = {}, min = 0, max = 100, step = 1, value = None, pushable = False, vertical = False,
				 name = None, screenName = None, height = 'auto', width = 'auto'):
		if value is None:
			value = max
		super().__init__(name, screenName)
		self.setRangeSlider(allowCross, dots, marks, min, max, step, value, pushable, vertical, height, width)
	def getValue(self):
		return self.__value
	def update(self, value):
		self.__value = value
	def setRangeSlider(self, allowCross, dots, marks, min, max, step, value, pushable, vertical, height, width):
		self.__allowCross = allowCross
		self.__dots = dots
		self.__marks = marks
		self.__min = min
		self.__max = max
		self.__step = step
		self.__value = value
		self.__pushable = pushable
		self.__vertical = vertical
		self.__height = height
		self.__width = width
		st = {'height': height, 'width': width}
		super().setDashRendering(html.Div([dcc.RangeSlider(
			id=str(super().getID()),
			allowCross=allowCross,
			dots=dots,
			marks=marks,
			min=min,
			max=max,
			step=step,
			value=value,
			pushable=pushable,
			vertical=vertical,
		)], style=st))

class CInput(CDashComponent):
	def __init__(self, list = [], min = None, max = None, maxlength = -1, placeholder = 'Input field',
				 readonly = False, style = {}, type = 'text', value = None, height = 'auto', width = 'auto',
				 name = None, screenName = None):
		super().__init__(name, screenName)
		self.setInput(list, min, max, maxlength, placeholder, readonly, style, type, value, height, width)
	def getValue(self):
		return self.__value
	def update(self, value):
		self.__value = value
	def setInput(self, list, min, max, maxlength, placeholder, readonly, style, type, value, height, width):
		self.__list = list
		self.__min = min
		self.__max = max
		self.__maxlength = maxlength
		self.__placeholder = placeholder
		self.__readonly = readonly
		self.__type = type
		self.__value = value
		self.__height = height
		self.__width = width
		style['height'] = height
		style['width'] = width
		self.__style = style
		super().setDashRendering(dcc.Input(
			id=str(super().getID()),
			name=str(super().getID()),
			list=list,
			min=min,
			max=max,
			maxlength=maxlength,
			placeholder=placeholder,
			readonly=readonly,
			style=style,
			type=type,
			value=value,
		))

class CTextArea(CDashComponent):
	def __init__(self, cols = 20, contentEditable = True, disabled = False, draggable = False, maxLength = -1, minLength = -1,
				 placeholder = 'Enter text', readonly = False, rows = 20, style = {}, title = '', value = None,
				 name = None, screenName = None, height = 'auto', width = 'auto'):
		super().__init__(name, screenName)
		self.setTextArea(cols, contentEditable, disabled, draggable, maxLength, minLength, placeholder, readonly, rows, style, title, value, height, width)
	def update(self, value):
		self.__value = value
	def getValue(self):
		return self.__value
	def setTextArea(self, cols, contentEditable, disabled, draggable, maxLength, minLength, placeholder, readonly, rows, style,title, value, height, width):
		self.__cols = cols
		self.__contentEditable = contentEditable
		self.__disabled = disabled
		self.__draggable = draggable
		self.__maxLength = maxLength
		self.__minLength = minLength
		self.__placeholder = placeholder
		self.__readonly = readonly
		self.__rows = rows
		self.__title = title
		self.__value = value
		self.__height = height
		self.__width = width
		style['height'] = height
		style['width'] = width
		self.__style = style
		super().setDashRendering(dcc.Textarea(
			id=str(super().getID()),
			name=str(super().getID()),
			cols=cols,
			contentEditable=contentEditable,
			disabled=disabled,
			draggable=draggable,
			maxLength=maxLength,
			minLength=minLength,
			placeholder=placeholder,
			readOnly=readonly,
			rows=rows,
			title=title,
			value=value,
			style=style,
		))

class CChecklist(CDashComponent):
	def __init__(self, inputStyle = {}, labelStyle = {}, options = [], style = {}, value = [], height = 'auto', width = 'auto',
				 name = None, screenName = None):
		super().__init__(name, screenName)
		self.setChecklist(inputStyle, labelStyle, options, style, value, height, width)
	def getValue(self):
		return self.__value
	def update(self, value):
		self.__value = value
	def setChecklist(self, inputStyle, labelStyle, options, style, value, height, width):
		self.__inputStyle = inputStyle
		self.__labelStyle = labelStyle
		self.__options = options
		self.__value = value
		self.__height = height
		self.__width = width
		style['height'] = height
		style['width'] = width
		self.__style = style
		super().setDashRendering(dcc.Checklist(
			id=str(super().getID()),
			inputStyle=inputStyle,
			labelStyle=labelStyle,
			options=options,
			style=style,
			values=value,
		))

class CRadioItems(CDashComponent):
	def __init__(self, inputStyle = {}, labelStyle = {}, options = [], style = {}, value = [], height = 'auto', width = 'auto',
				 name = None, screenName = None):
		super().__init__(name, screenName)
		self.setRadioItems(inputStyle, labelStyle, options, style, value, height, width)
	def getValue(self):
		return self.__value
	def update(self, value):
		self.__value = value
	def setRadioItems(self, inputStyle, labelStyle, options, style, value, height, width):
		self.__inputStyle = inputStyle
		self.__labelStyle = labelStyle
		self.__options = options
		self.__value = value
		self.__height = height
		self.__width = width
		style['height'] = height
		style['width'] = width
		self.__style = style
		super().setDashRendering(dcc.RadioItems(
			id=str(super().getID()),
			inputStyle=inputStyle,
			labelStyle=labelStyle,
			options=options,
			style=style,
			value=value,
		))

class CButton(CDashComponent):
	def __init__(self, text = 'Button', style = {}, height = 'auto', width = 'auto',
				 name = None, screenName = None):
		super().__init__(name, screenName)
		self.setButton(text, style, height, width)
	def getValue(self):
		return self.__value
	def update(self, value):
		self.__value = value
	def setButton(self, text, style, height, width):
		self.__text = text
		style['height'] = height
		style['width'] = width
		self.__style = style
		self.__height = height
		self.__width = width
		self.__value = 0
		self.setDashRendering(html.Button(
			text,
			id=str(super().getID()),
			name=str(super().getID()),
			style=style,
		))

#TODO: Add feature of multiple file upload!!!
class CUpload(CDashComponent):
	def __init__(self, text = 'Drag and Drop or Select a File', max_size = -1, multiple = False, style = {}, height = 'auto', width = 'auto',
				 name = None, screenName = None):
		super().__init__(name, screenName)
		self.setUpload(text, max_size, multiple, style, height, width)
	def getValue(self):
		return [self.__filename, self.__contents]
	def update(self, contents = None, filename = None):
		if contents is not None:
			self.__contents = contents
		if filename is not None:
			self.__filename = filename
	def setUpload(self, text, max_size, multiple, style, height, width):
		self.__max_size = max_size
		self.__multiple = multiple
		style['height'] = height
		style['width'] = width
		self.__style = style
		self.__filename = None
		self.__contents = None
		super().setDashRendering(dcc.Upload(
			[text],
			id=str(super().getID()),
			max_size=max_size,
			multiple=multiple,
			style=style,
		))

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

def CreateObjectWithScreeName(o, scName, **args):
	print(args['args'][0])
	print(scName)
	return o(**args['args'][0], screenName=scName)

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
		'CDatePickerRange': CDatePickerRange,
		'CDatePickerSingle': CDatePickerSingle,
		'CDropdown': CDropdown,
		'CSlider': CSlider,
		'CRangeSlider': CRangeSlider,
		'CInput': CInput,
		'CTextArea': CTextArea,
		'CChecklist': CChecklist,
		'CRadioItems': CRadioItems,
		'CButton': CButton,
		'CUpload': CUpload,
		'Create': lambda o, *a: CreateObjectWithScreeName(o=o, scName=args['screen'], args=a),
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
#http://localhost:5000/d/DisplayScreen@screen=test&asset=Alperia-VSM
#http://localhost:5000/d/DisplayScreen@screen=secondTest&asset=Alperia-VSM

def createUpdateCallback(uid, screen):
	objects = readObjects(uid, screen)
	inputLst = []
	stateLst = []
	for obj in objects:
		id = generateId(obj['object'], obj['type'], screen)
		num = 1
		if obj['type'] == 'CDatePickerRange':
			num = 2
			inputLst.append(Input(id, 'start_date'))
			inputLst.append(Input(id, 'end_date'))
		elif obj['type'] ==  'CDatePickerSingle':
			inputLst.append(Input(id, 'date'))
		elif obj['type'] == 'CText':
			inputLst.append(Input(id, 'children'))
		elif obj['type'] == 'CDropdown':
			inputLst.append(Input(id, 'value'))
		elif obj['type'] == 'CSlider':
			inputLst.append(Input(id, 'value'))
		elif obj['type'] == 'CRangeSlider':
			inputLst.append(Input(id, 'value'))
		elif obj['type'] == 'CInput':
			inputLst.append(Input(id,'value'))
		elif obj['type'] == 'CTextArea':
			inputLst.append(Input(id, 'value'))
		elif obj['type'] == 'CChecklist':
			inputLst.append(Input(id, 'values'))
		elif obj['type'] == 'CRadioItems':
			inputLst.append(Input(id, 'value'))
		elif obj['type'] == 'CButton':
			inputLst.append(Input(id, 'n_clicks'))
		elif obj['type'] == 'CUpload':
			num = 2
			inputLst.append(Input(id, 'contents'))
			inputLst.append(Input(id, 'filename'))
		for i in range(num):
			stateLst.append(State(id, 'id'))
	if len(objects) > 0:
		outputId = generateId(objects[0]['object'], objects[0]['type'], screen)
		@dash_app.callback(
			Output(outputId, 'id'),
			inputLst,
			stateLst,
		)
		def update(*args):
			for i in range(len(args) // 2):
				if args[i] is None:
					continue
				id = args[i + len(args) // 2]
				type = getTypeFromId(id)
				name = getNameFromId(id)
				#### TODO:User Id 0 is hardcoded!!!
				object = dictionaryOfAllScreenVariables["0"][screen].get(name)
				if type == 'CDatePickerRange':
					if i + len(args) // 2 + 1 < len(args) and args[i + len(args) // 2 + 1] == args[i + len(args) // 2]:
						object.update(start_date = args[i])
					else:
						object.update(end_date = args[i])
				elif type == 'CDatePickerSingle':
					object.update(args[i])
				elif type == 'CText':
					object.update(args[i])
				elif type == 'CDropdown':
					object.update(args[i])
				elif type == 'CSlider':
					object.update(args[i])
				elif type == 'CRangeSlider':
					object.update(args[i])
				elif type == 'CInput':
					object.update(args[i])
				elif type == 'CTextArea':
					object.update(args[i])
				elif type == 'CChecklist':
					object.update(args[i])
				elif type == 'CRadioItems':
					object.update(args[i])
				elif type == 'CButton':
					object.update(args[i])
				elif type == 'CUpload':
					if i + len(args) // 2 + 1 < len(args) and args[i + len(args) // 2 + 1] == args[i + len(args) // 2]:
						object.update(contents = args[i])
					else:
						object.update(filename = args[i])
			print(outputId)
			return outputId

# find out all the screen names
screenNames = getScreenNames("001")

#Create callbacks for live updates of objects
for screen in screenNames:
	createUpdateCallback("001", screen)

'''
def getScreenVariables(user, screen):
	def getScreenVariablesForUser():
		print(screen)
		if user in dictionaryOfAllScreenVariables and screen in dictionaryOfAllScreenVariables[user]:
			return dictionaryOfAllScreenVariables[user][screen]
		else:
			return {}
	return getScreenVariablesForUser


#Extract all the callbacks
callbackFunctions = {}
for screen in screenNames:
	callbackFunctions[screen] = compile_callbacks("001", screen, getScreenVariables("0", screen), CSafeLog(None))
'''
callbackFunctions = {}
for screen in screenNames:
	path = "user" + "001" + "/scripts/dash/screens/"
	f = open(path + screen + "/callbacks.py", "r")
	source_code = f.read()
	locals = {}
	byte_code = compile_restricted(
		source = source_code,
		filename = '<inline>',
		mode = 'exec'
	)
	#TODO: User Id 0 is hardcoded
	uid = "0"
	if uid not in dictionaryOfAllScreenVariables:
		dictionaryOfAllScreenVariables[uid] = {}
	if screen not in dictionaryOfAllScreenVariables[uid]:
		dictionaryOfAllScreenVariables[uid][screen] = CSafeDict({})
	additional_globals = {
		'date': date, 'timedelta': timedelta, 'datetime': datetime, 'screenVariables': dictionaryOfAllScreenVariables["0"][screen], 'log': CSafeLog(None), 'screen': screen,
		'decodeFile': base64.b64decode, 'split': safeSplit, 'pd': pd, 'io': io
	}
	safe_globals = safe_builtins
	safe_globals.update(additional_globals)
	exec(byte_code, dict(safe_globals), locals)
	callbackFunctions[screen] = locals

#Extract all the interactions
interactionsDict = parse("001")

for interaction in interactionsDict:
	inputLst = []
	for input in interaction['input']:
		inputId = generateId(input['object'], input['type'], interaction['screen'])
		if input['type'] == 'CDatePickerRange':
			inputLst.append(Input(inputId, 'start_date'))
			inputLst.append(Input(inputId, 'end_date'))
		elif input['type'] == 'CDatePickerSingle':
			inputLst.append(Input(inputId, 'date'))
		elif input['type'] == 'CText':
			inputLst.append(Input(inputId, 'n_clicks'))
		elif input['type'] == 'CDropdown':
			inputLst.append(Input(inputId, 'value'))
		elif input['type'] == 'CSlider':
			inputLst.append(Input(inputId, 'value'))
		elif input['type'] == 'CRangeSlider':
			inputLst.append(Input(inputId, 'value'))
		elif input['type'] == 'CInput':
			inputLst.append(Input(inputId, 'value'))
		elif input['type'] == 'CTextArea':
			inputLst.append(Input(inputId, 'value'))
		elif input['type'] == 'CChecklist':
			inputLst.append(Input(inputId, 'values'))
		elif input['type'] == 'CRadioItems':
			inputLst.append(Input(inputId, 'value'))
		elif input['type'] == 'CButton':
			inputLst.append(Input(inputId, 'n_clicks'))
		elif input['type'] == 'CUpload':
			inputLst.append(Input(inputId, 'contents'))
			inputLst.append(Input(inputId, 'filename'))
	stateLst = []
	if 'state' in interaction:
		for state in interaction['state']:
			stateId = generateId(state['object'], state['type'], interaction['screen'])
			if state['type'] == 'CDatePickerRange':
				stateLst.append(State(stateId, 'start_date'))
				stateLst.append(State(stateId, 'end_date'))
			elif state['type'] == 'CDatePickerSingle':
				stateLst.append(State(stateId, 'date'))
			elif state['type'] == 'CText':
				stateLst.append(State(stateId, 'children'))
			elif state['type'] == 'CDropdown':
				stateLst.append(State(stateId, 'value'))
			elif state['type'] == 'CSlider':
				stateLst.append(State(stateId, 'value'))
			elif state['type'] == 'CRangeSlider':
				stateLst.append(State(stateId, 'value'))
			elif state['type'] == 'CInput':
				stateLst.append(State(steteId, 'value'))
			elif state['type'] == 'CTextArea':
				stateLst.append(State(stateId, 'value'))
			elif state['type'] == 'CChecklist':
				stateLst.append(State(stateId, 'values'))
			elif state['type'] == 'CRadioItems':
				stateLst.append(State(stateId, 'value'))
			elif state['type'] == 'CButton':
				stateLst.append(State(stateId, 'n_clicks'))
			elif state['type'] == 'CUpload':
				stateLst.append(State(stateId, 'contents'))
				stateLst.append(State(stateId, 'filename'))
	outputId = generateId(interaction['output']['object'], interaction['output']['type'], interaction['screen'])
	dash_app.callback(
		Output(outputId, interaction['output']['param']),
		inputLst,
		stateLst,
	)(callbackFunctions[interaction['screen']][interaction['callback']])