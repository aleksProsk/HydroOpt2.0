log.print("starting renderer")

myText = CText("test")
myFrame = CFrame("Test", width = 1.0, height = 0.5)
myWaitStopper = CStopWaitingForGraphics()
myFrame.aChild(myText)
myFrame.aChild(myWaitStopper)

myOutput = Create(CText, {'name': 'myOutput', 'text':'Here would be selected date range!'})
myDatePicker = Create(CDatePicker, {'name' : 'myDatePicker'})


myOutput1 = Create(CText, {'name': 'myOutput1', 'text':'Something new'})
myDatePicker1 = Create(CDatePicker, {'name' : 'myDatePicker1'})

textToPress = Create(CText, {'name': 'textToPress', 'text': 'PRESS HERE PLEASE'})

myFrame.aChild(myDatePicker)
myFrame.aChild(myOutput)
myFrame.aChild(myDatePicker1)
myFrame.aChild(myOutput1)
myFrame.aChild(textToPress)

log.print(myDatePicker.getSelectedRange())

myScreen = CPage('Test')
myScreen.aChild(myFrame)

return myScreen


