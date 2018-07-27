#Simple case: cllback with one input and one output
def simpleExample(start_date, end_date):
	myDatePicker = screenVariables.get('myDatePicker')
	return str(start_date) + ' ' + str(end_date)
	#return str(myDatePicker.getSelectedRange())

#More complicated case, which uses state of third element
def simpleExample1(start_date, end_date, start_date1, end_date1):
	return str(start_date) + ' ' + str(end_date) + ' ' + str(start_date1) + ' ' + str(end_date1)

#Cse, when we access the other elements, not connected to input and output of callback, through dictionary
def press(n):
	# a = getScreenVariables().get('myDatePicker')
	# b = getScreenVariables().get('myDatePicker1')
	# c = getScreenVariables().get('myOutput')
	# d = getScreenVariables().get('myOutput1')
	a = screenVariables.get('myDatePicker')
	b = screenVariables.get('myDatePicker1')
	c = screenVariables.get('myOutput')
	d = screenVariables.get('myOutput1')
	e = screenVariables.get('myDropdown')
	f = screenVariables.get('mySlider')
	g = screenVariables.get('myRangeSlider')
	h = screenVariables.get('myInput')
	i = screenVariables.get('myTextArea')
	j = screenVariables.get('myChecklist')
	k = screenVariables.get('myRadioItems')
	l = screenVariables.get('myButton')
	m = screenVariables.get('myDatePicker2')
	n = screenVariables.get('myUpload')
	o = screenVariables.get('myTabs')
	p = screenVariables.get('myDataTable')
	for i in range(10):
		log.print(i)
	return str(a.getSelectedRange()) + ' ' + str(b.getSelectedRange()) + ' ' + str(c.getText()) + ' ' + str(d.getText()) + ' ' + str(e.getValue()) + ' ' + str(f.getValue()) + ' ' + \
		   str(g.getValue()) + ' ' + str(h.getValue()) + ' ' + str(i.getValue()) + ' ' + str(j.getValue()) + ' ' + str(k.getValue()) + str(l.getValue()) + ' ' + str(m.getValue()) + \
		   ' ' + str(n.getValue()) + ' ' + str(o.getValue()) + ' '  + str(p.getValue()) + ' ' + str(p.getData().to_dict('records'))

#TODO:Add feature of multiple files upload!
def readFile(list_of_contents, filename):
	if list_of_contents is None:
		return 'Nothing!'
	content_type = split(',', list_of_contents, 0)
	content_string = split(',', list_of_contents, 1)
	decoded = decodeFile(content_string)
	return 'File: ' + filename + "\n" + str(decoded)

def loadDataTable(list_of_contents, filename):
	if list_of_contents is None:
		return []
	content_type = split(',', list_of_contents, 0)
	content_string = split(',', list_of_contents, 1)
	decoded = decodeFile(content_string)
	try:
		df = pd.read_csv(io.StringIO(decoded.decode('ISO-8859-1')))
		return df.to_dict('records')
	except Exception as e:
		return [{'Error': 'file is not .csv'}]

def updateTableContent(rows):
	return str(rows)

def getPersons(selected_row_indices):
	log.print(selected_row_indices)
	dataTable = screenVariables.get('myInputTable')
	log.print(dataTable.getRows())
	return 'You selected: ' + '\n' + str(dataTable.getRowsByIndices(selected_row_indices))


