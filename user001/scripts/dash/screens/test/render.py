log.print("starting renderer")

datePickerFrame = CFrame("Date pickers", width = 0.5, height = 0.2, style={})

myDatePicker = Create(CDatePickerRange, {'name' : 'myDatePicker'})
myOutput = Create(CText, {'name': 'myOutput', 'text':'Here should be selected date range!'})

myDatePicker1 = Create(CDatePickerSingle, {'name': 'myDatePicker1'})
singleText = Create(CText, {'name': 'singleText', 'text': 'Here should be selected date!'})

datePickerFrame.aChild(myDatePicker)
datePickerFrame.aChild(myOutput)
datePickerFrame.aChild(myDatePicker1)
datePickerFrame.aChild(singleText)


selectingItems = CFrame("Dropdown, checkbox and radio buttons", width = 0.5, height = 0.2, style={})
myDropdown = Create(CDropdown, {'name': 'myDropdown',
                                'options': [{'label': 'first', 'value': 'first',},
                                    {'label': 'second', 'value': 'second',},
                                    {'label': 'third', 'value': 'third',},
                                ],
                                'value': '',
                                'multi':False,
                                'placeholder':'Select options',
                                'style': {'marginTop': '1%'}})
dropdownText = Create(CText, {'name': 'dropdownText', 'text': 'Here should be text from dropdown!'})

myRadioItems = Create(CRadioItems, {'name': 'myRadioItems',
                                  'options': [{'label': 'first', 'value': 'first', },
                                              {'label': 'second', 'value': 'second', },
                                              {'label': 'third', 'value': 'third', },
                                              ],
                                  },
                                )
radioItemsText = Create(CText, {'name': 'radioItemsText', 'text': 'Here should be text from radio buttons!'})

myChecklist = Create(CChecklist, {'name': 'myChecklist',
                                  'options': [{'label': 'first', 'value': 'first', },
                                              {'label': 'second', 'value': 'second', },
                                              {'label': 'third', 'value': 'third', },
                                              ],
                                  },
                                )
checklistText = Create(CText, {'name': 'checklistText', 'text': 'Here should be text from checklist!'})

selectingItems.aChild(myDropdown)
selectingItems.aChild(dropdownText)
selectingItems.aChild(myRadioItems)
selectingItems.aChild(radioItemsText)
selectingItems.aChild(myChecklist)
selectingItems.aChild(checklistText)

sliders = CFrame("Sliders", width = 0.5, height = 0.2, style={})

mySlider = Create(CSlider, {'name': 'mySlider', 'min': 100, 'max': 200, 'step': 5, 'value': 150, 'vertical': False, 'dots': True, 'style': {'marginTop': '1%', 'marginLeft': '1%', 'marginRight': '1%'}})
sliderText = Create(CText, {'name': 'sliderText', 'text': 'Here should be text from slider!'})

myRangeSlider = Create(CRangeSlider, {'name': 'myRangeSlider', 'min': 0, 'max': 200, 'step': 5, 'value': [50, 150], 'vertical': False, 'dots': True, 'pushable': True, 'style': {'marginTop': '1%', 'marginLeft': '1%', 'marginRight': '1%'}})
rangeSliderText = Create(CText, {'name': 'rangeSliderText', 'text': 'Here should be text from range slider!'})

sliders.aChild(mySlider)
sliders.aChild(sliderText)
sliders.aChild(myRangeSlider)
sliders.aChild(rangeSliderText)

inputFields = CFrame("Inputs", width = 0.5, height = 0.2, style={})

myInput = Create(CInput, {'name': 'myInput', 'style': {'marginTop': '1%', 'width': '50%', 'marginLeft': '1%'}})
inputText = Create(CText, {'name': 'inputText', 'text': 'Here should be text from input!'})

myTextArea = Create(CTextArea, {'name': 'myTextArea', 'style': {'width': '50%', 'marginLeft': '1%'}})
textAreaText = Create(CText, {'name': 'textAreaText', 'text': 'Here should be text from text area!'})

inputFields.aChild(myInput)
inputFields.aChild(inputText)
inputFields.aChild(myTextArea)
inputFields.aChild(textAreaText)

buttons = CFrame("Button and tabs", width = 0.5, height = 0.2, style={})

myButton = Create(CButton, {'name': 'myButton',
                            'style': {'height': 50, 'width': 200, 'marginTop': '1%', 'marginLeft': '1%', 'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)'},
                            'text': 'Press here'})
buttonText = Create(CText, {'name': 'buttonText', 'text': 'Here should be number of button clicks!'})

myTabs = Create(CTabs, {'name': 'myTabs',
                        'tabs': [
                            {'label': 'first', 'value': 'first'},
                            {'label': 'second', 'value': 'second'},
                            {'label': 'third', 'value': 'third'}
                        ],
                        'style': {'width': '50%', 'marginLeft': '1%'}})
tabsText = Create(CText, {'name': 'tabsText', 'text': 'Here should be text from tabs!'})

buttons.aChild(myButton)
buttons.aChild(buttonText)
buttons.aChild(myTabs)
buttons.aChild(tabsText)

uploads = CFrame("Uploading", width = 0.5, height = 0.5, style = {})

myUpload = Create(CUpload, {'name': 'myUpload',
                            'style': {'height': 50, 'width': 200, 'marginTop': '1%', 'marginLeft': '1%', 'backgroundColor': 'white',
                                      'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'textAlign': 'center'}})
uploadText = Create(CText, {'name': 'uploadText', 'text': 'Here should be uploaded text!'})

myUploadTable = Create(CUpload, {'name': 'myUploadTable',
                                 'style': {'height': 50, 'width': 200, 'marginTop': '1%', 'marginLeft': '1%', 'backgroundColor': 'white',
                                           'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                           'textAlign': 'center'},
                                 'text': 'Upload table'})
myDataTable = Create(CDataTable, {'name': 'myDataTable', 'style': {'width': '95%', 'height': '80%', 'marginLeft': '1%', 'marginRight': '1%', 'marginTop': '1%'}})

uploads.aChild(myUpload)
uploads.aChild(uploadText)
uploads.aChild(myUploadTable)
uploads.aChild(myDataTable)

inputTable = CFrame("Input table", width = 0.5, height = 0.3, style = {})

myInputTable = Create(CDataTable, {'name': 'myInputTable', 'editable' : True, 'rows': [[[''], ['']], [[''], ['']]], 'headers': ['Name', 'Surname'],
                                   'style': {'width': '95%', 'height': '50%', 'marginLeft': '1%', 'marginRight': '1%', 'marginTop': '1%'}})
outputTable = Create(CText, {'name': 'outputTable', 'text': 'Table content'})

persons = Create(CText, {'name': 'persons', 'text': 'Selected persons:'})

inputTable.aChild(myInputTable)
inputTable.aChild(outputTable)
inputTable.aChild(persons)

myScreen = CPage('Test page')

myScreen.aChild(datePickerFrame)
myScreen.aChild(selectingItems)
myScreen.aChild(sliders)
myScreen.aChild(inputFields)
myScreen.aChild(buttons)
myScreen.aChild(uploads)
myScreen.aChild(inputTable)
myWaitStopper = CStopWaitingForGraphics()
myScreen.aChild(myWaitStopper)

return myScreen


