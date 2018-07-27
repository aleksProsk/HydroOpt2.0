import dash_html_components as html

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CButton(CDashComponent):
	def __init__(self, text = 'Button', style = {},
				 name = None, screenName = None):
		super().__init__(name, screenName)
		self.setButton(text, style)
	def getValue(self):
		return self.__value
	def update(self, value):
		self.__value = value
	def setButton(self, text, style):
		self.__text = text
		self.__value = 0
		self.setDashRendering(html.Button(
			text,
			id=str(super().getID()),
			name=str(super().getID()),
			style=style,
		))