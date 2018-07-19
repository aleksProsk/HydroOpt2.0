#Simple case: cllback with one input and one output
def simpleExample(start_date, end_date):
	string_prefix = 'You have selected: '
	log.print('called function in test 1')
	#myDatePicker = getScreenVariables().get('myDatePicker')
	myDatePicker = screenVariables.get('myDatePicker')
	'''
	if start_date is not None:
		start_date = datetime.strptime(start_date, '%Y-%m-%d')
		start_date_string = start_date.strftime('%B %d, %Y')
		string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
	if end_date is not Non
		end_date = datetime.strptime(ee:nd_date, '%Y-%m-%d')
		end_date_string = end_date.strftime('%B %d, %Y')
		string_prefix = string_prefix + 'End Date: ' + end_date_string
	if len(string_prefix) == len('You have selected: '):
		return 'Select a date to see it displayed here'
	else:
		return string_prefix + ' and ' + '''
	#return str(start_date) + ' ' + str(end_date)
	return str(myDatePicker.getSelectedRange())

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
	return str(a.getSelectedRange()) + ' ' + str(b.getSelectedRange()) + ' ' + str(c.getText()) + ' ' + str(d.getText()) + ' ' + str(e.getValue()) + ' ' + str(f.getValue()) + ' ' + \
		   str(g.getValue()) + ' ' + str(h.getValue()) + ' ' + str(i.getValue()) + ' ' + str(j.getValue()) + ' ' + str(k.getValue()) + str(l.getValue()) + ' ' + str(m.getValue()) + \
		   ' ' + str(n.getValue())

def displayValue(value):
	return value

#TODO:Add feature of multiple files upload!
def readFile(list_of_contents, filename):
	if list_of_contents is None:
		return 'Nothing!'
	log.print(type(list_of_contents))
	content_type = split(',', list_of_contents, 0)
	content_string = split(',', list_of_contents, 1)
	decoded = decodeFile(content_string)
	return 'File: ' + filename + "\n" + str(decoded)
