log.print("starting renderer")

myFrame = CFrame(hasCaption = False, width = 1.0, height = 1.0, style={'display': 'flex', 'flexDirection': 'row'})
myWaitStopper = CStopWaitingForGraphics()
myFrame.aChild(myWaitStopper)

myChart = Create(CChart, {'name': 'myChart', 'title': 'Example graph', 'style': {'width': '50%', 'height': '10%'}, 'type': 'line',
                          'rows': [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], 'headers': ['Sample graph'], 'rowCaptions': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})

exampleFrame = CContainer(style = {'width': '50%', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'borderTopWidth': '0'})

sliderFrame = CContainer(style={'width': '100%', 'border': 'none', 'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'center'})

mySlider = Create(CRangeSlider, {'name': 'mySlider', 'min': 1, 'max': 10, 'step': 1, 'value': [1, 10], 'style': {'width': '90%', 'margin': '5%'}})

sliderFrame.aChild(mySlider)

buttonFrame = CContainer(style={'border': 'none', 'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'center', 'height': '7%'})

myButton = Create(CButton, {'name': 'myButton',
                            'style': {'height': 50, 'width': 200, 'marginTop': '5%', 'marginLeft': '1%', 'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)'},
                            'text': 'Reset graph'})

buttonFrame.aChild(myButton)

exampleFrame.aChild(buttonFrame)
exampleFrame.aChild(sliderFrame)

myFrame.aChild(myChart)
myFrame.aChild(exampleFrame)
myScreen = CPage('Test3')
myScreen.aChild(myFrame)
#myScreen.aChild(sliderFrame)

return myScreen


