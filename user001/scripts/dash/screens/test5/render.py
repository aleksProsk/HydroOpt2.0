log.print("starting renderer")

myFrame = CFrame(hasCaption = False, width = 1.0, height = 1.0, style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})
myWaitStopper = CStopWaitingForGraphics()
myFrame.aChild(myWaitStopper)

myMapContainer = Create(CContainer, {'name': 'myMapcontainer', 'style': {'width': '100%', 'display': 'flex', 'flexDirection': 'row'}})

myTopologyMap = Create(CTopologyMap, {'name': 'myTopologyMap',
                                      'lat': [46.156616, 46.21667, 46.279559, 46.127516, 46.169051],
                                      'lon': [7.6174696, 7.583333, 7.5383323, 7.5675693, 7.6906223],
                                      'text': ['T', 'T', 'T', 'R', 'R', 'R'],
                                      'names': ['Turbine', 'Turbine', 'Turbine', 'Reservoir', 'Reservoir'],
                                      'customdata': ['Mottec', 'Vissoie', 'Navizence', 'Lac de Moiry', 'Turtmann dam'],
                                      'dataMode': ['markers+text', 'markers+text', 'markers+text', 'markers+text', 'markers+text'],
                                      'textposition': 'center',
                                      'hoverinfo': ['none', 'none', 'none', 'none', 'none'],
                                      'color': ['#4292f4', '#4292f4', '#4292f4', '#ef6969', '#ef6969'],
                                      'edges': [
                                          [0, 1],
                                          [1, 2],
                                          [3, 0],
                                          [4, 0],
                                      ],
                                      'style': {'width': '80%', 'height': '60vh'}})

inputContainer = Create(CContainer, {'name': 'inputContainer', 'style': {'display': 'flex', 'flexDirection': 'column', 'marginLeft': '5%'}})

title = Create(CText, {'name': 'title', 'text': 'Selected point:'})
selected = Create(CText, {'name': 'selected', 'text': 'None'})

inputLat = Create(CInput, {'name': 'inputLat', 'placeholder': 'Latitude:'})
inputLon = Create(CInput, {'name': 'inputLon', 'placeholder': 'Longitude:'})

myButton = Create(CButton, {'name': 'myButton',
                            'style': {'height': 50, 'width': 200, 'marginTop': '1%', 'marginLeft': '1%', 'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)'},
                            'text': 'Set'})

inputContainer.aChild(title)
inputContainer.aChild(selected)
inputContainer.aChild(inputLat)
inputContainer.aChild(inputLon)
inputContainer.aChild(myButton)

myMapContainer.aChild(myTopologyMap)
myMapContainer.aChild(inputContainer)

myOutput = Create(CText, {'name': 'myOutput', 'text': ''})
myOutput1 = Create(CText, {'name': 'myOutput1', 'text': 'kek'})

myMap = Create(CMap, {'name': 'myMap'})
myInterval = Create(CInterval, {'name': 'myInterval', 'interval': 2000000})
myZoom = Create(CText, {'name': 'myZoom', 'text': ''})

myFrame.aChild(myMapContainer)
myFrame.aChild(myOutput)
myFrame.aChild(myOutput1)
myFrame.aChild(myMap)
myFrame.aChild(myInterval)
myFrame.aChild(myZoom)

myScreen = CPage('Test5')
myScreen.aChild(myFrame)

return myScreen


