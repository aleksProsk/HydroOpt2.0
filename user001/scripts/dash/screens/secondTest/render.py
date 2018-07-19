log.print("starting renderer")

myText = CText("test")
myFrame = CFrame("Test", width = 1.0, height = 1.0)
myWaitStopper = CStopWaitingForGraphics()
myFrame.aChild(myText)
myFrame.aChild(myWaitStopper)

myOutput = Create(CText, {'name': 'myOutput', 'text':'Here would be selected date range!'})
myDatePicker = Create(CDatePickerRange, {'name' : 'myDatePicker'})


myOutput1 = Create(CText, {'name': 'myOutput1', 'text':'Something new'})
myDatePicker1 = Create(CDatePickerRange, {'name' : 'myDatePicker1'})

textToPress = Create(CText, {'name': 'textToPress', 'text': 'PRESS HERE PLEASE'})

myDropdown = Create(CDropdown, {'name': 'myDropdown',
                                'options': [{'label': 'first', 'value': 'first',},
                                    {'label': 'second', 'value': 'second',},
                                    {'label': 'third', 'value': 'third',},
                                ],
                                'value': '',
                                'multi':True,
                                'placeholder':'Select options on this screen',})
dropdownText = Create(CText, {'name': 'dropdownText', 'text': 'Here should be text from dropdown'})

mySlider = Create(CSlider, {'name': 'mySlider', 'min': 100, 'max': 200, 'step': 5, 'value': 150})
sliderText = Create(CText, {'name': 'sliderText', 'text': 'Here should be text from slider'})

myRangeSlider = Create(CRangeSlider, {'name': 'myRangeSlider', 'min': 0, 'max': 200, 'step': 5, 'value': [50, 150], 'allowCross': True})
rangeSliderText = Create(CText, {'name': 'rangeSliderText', 'text': 'Here should be text from slider'})

myInput = Create(CInput, {'name': 'myInput', 'type': 'number', 'min': -5, 'max': 10, 'width': 100})
inputText = Create(CText, {'name': 'inputText', 'text': 'Here should be text from input'})

myTextArea = Create(CTextArea, {'name': 'myTextArea', 'width': 500, 'title': 'Text area 2', 'draggable': True})
textAreaText = Create(CText, {'name': 'textAreaText', 'text': 'Here should be text from text area'})

myChecklist = Create(CChecklist, {'name': 'myChecklist',
                                  'options': [{'label': 'first', 'value': 'first', },
                                              {'label': 'second', 'value': 'second', },
                                              {'label': 'third', 'value': 'third', },
                                              ],
                                'labelStyle': {'display': 'inline-block'},
                                  })
checklistText = Create(CText, {'name': 'checklistText', 'text': 'Here should be text from checklist'})

myRadioItems = Create(CRadioItems, {'name': 'myRadioItems',
                                  'options': [{'label': 'first', 'value': 'first', },
                                              {'label': 'second', 'value': 'second', },
                                              {'label': 'third', 'value': 'third', },
                                              ],
                                    'labelStyle': {'display': 'inline-block'},
                                  },)
radioItemsText = Create(CText, {'name': 'radioItemsText', 'text': 'Here should be text from checklist'})

myButton = Create(CButton, {'name': 'myButton', 'height': 50, 'width': 200, 'text': 'Press here', 'style': {'backgroundColor': 'white'}})
buttonText = Create(CText, {'name': 'buttonText', 'text': 'Here should be number of button clicks'})

myDatePicker2 = Create(CDatePickerSingle, {'name': 'myDatePicker2'})
singleText = Create(CText, {'name': 'singleText', 'text': 'Here should be number of button clicks'})

myUpload = Create(CUpload, {'name': 'myUpload', 'style': {'backgroundColor': 'white'}})
uploadText = Create(CText, {'name': 'uploadText', 'text': 'Here should be uploaded text'})

myFrame.aChild(myDatePicker)
myFrame.aChild(myOutput)
myFrame.aChild(myDatePicker1)
myFrame.aChild(myOutput1)
myFrame.aChild(textToPress)
myFrame.aChild(myDropdown)
myFrame.aChild(dropdownText)
myFrame.aChild(mySlider)
myFrame.aChild(sliderText)
myFrame.aChild(myRangeSlider)
myFrame.aChild(rangeSliderText)
myFrame.aChild(myInput)
myFrame.aChild(inputText)
myFrame.aChild(myTextArea)
myFrame.aChild(textAreaText)
myFrame.aChild(myChecklist)
myFrame.aChild(checklistText)
myFrame.aChild(myRadioItems)
myFrame.aChild(radioItemsText)
myFrame.aChild(myButton)
myFrame.aChild(buttonText)
myFrame.aChild(myDatePicker2)
myFrame.aChild(singleText)
myFrame.aChild(myUpload)
myFrame.aChild(uploadText)


log.print(myDatePicker.getSelectedRange())

myScreen = CPage('Test')
myScreen.aChild(myFrame)

return myScreen


