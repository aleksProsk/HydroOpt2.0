log.print("starting renderer")

myFrame = CFrame(hasCaption = False, width = 1.0, height = 1.0, style={'display': 'flex', 'flexDirection': 'row'})
myWaitStopper = CStopWaitingForGraphics()
myFrame.aChild(myWaitStopper)

myChart = Create(CChart, {'name': 'myChart', 'title': 'Graph', 'style': {'width': '50%', 'height': '10%'}, 'type': 'line',
                          'rows': [[]], 'headers': [''], 'rowCaptions': []})

inputFrame = CContainer(style = {'width': '50%', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'borderTopWidth': '0'})

inputTable = Create(CDataTable, {'name': 'inputTable', 'editable' : True, 'row_selectable': False, 'rows': [[['']], [['']], [['']]], 'headers': ['x', 'y', 'Method'],
                                 'style': {'width': '90%'}})
addRow = Create(CButton, {'name': 'addRow', 'text': 'Add row',
                          'style': {'height': 50, 'width': 200, 'marginTop': '1%', 'marginLeft': '1%', 'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)'},
                        })
text = Create(CText, {'name': 'text', 'text': 'Slider for spline smoothing:'})
slider = Create(CSlider, {'name': 'slider', 'min': 0, 'max': 1.3, 'step': 0.01, 'value': 0.65, 'marks': {0: '0', 0.65: '0.65', 1.3: '1.3'},
                          'style': {'width': '90%', 'marginBottom': '1%'}})

text1 = Create(CText, {'name': 'text1', 'text': 'Slider for polyfit degree:'})
slider1 = Create(CSlider, {'name': 'slider1', 'min': 1, 'max': 10, 'step': 1, 'value': 2, 'dots': True, 'marks': {1: '1', 5: '5', 10: '10'},
                          'style': {'width': '90%'}})

btn = Create(CButton, {'name': 'btn', 'text': 'MODAL TEST',
                       'style': {'height': 50, 'width': 200, 'marginTop': '5%', 'marginLeft': '1%', 'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)'},
                    })
modal = Create(CModal, {'name': 'modal'})

modalCloser = Create(CText, {'name': 'modalCloser', 'text': 'Close', 'style': {'font-size': '28px', 'color': 'black'}})
modal.aChild(modalCloser)

modalContent = Create(CContainer, {'name': 'modalContent', 'style': {'background-color': '#F2F2F2', 'margin': 'auto', 'padding': '20px', 'border': '1px solid #888', 'width': '80%'}})
modal.aChild(modalContent)

mySelectList = Create(CSelectList, {'name': 'mySelectList', 'labels': ['1', '2', '3']})

inputFrame.aChild(inputTable)
inputFrame.aChild(addRow)
inputFrame.aChild(text)
inputFrame.aChild(slider)
inputFrame.aChild(text1)
inputFrame.aChild(slider1)
inputFrame.aChild(btn)
inputFrame.aChild(modal)
inputFrame.aChild(mySelectList)

myFrame.aChild(myChart)
myFrame.aChild(inputFrame)
myScreen = CPage('Test6')
myScreen.aChild(myFrame)

return myScreen


