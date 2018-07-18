log.print("starting renderer")

myText = CText("test")
myFrame = CFrame("Test", width = 1.0, height = 0.5)
myWaitStopper = CStopWaitingForGraphics()
myFrame.aChild(myText)
myFrame.aChild(myWaitStopper)

myOutput = Create(CText, {'name': 'myOutput', 'text':'Here would be selected date range!'})
myDatePicker = Create(CDatePicker, {'name' : 'myDatePicker', 'output': 'myOutput'})
myFrame.aChild(myDatePicker)
myFrame.aChild(myOutput)

log.print(myDatePicker.getSelectedRange())

myScreen = CPage('Test')
myScreen.aChild(myFrame)

return myScreen


