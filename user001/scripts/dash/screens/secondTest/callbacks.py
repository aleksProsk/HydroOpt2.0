#Simple case: cllback with one input and one output
def simpleExample(start_date, end_date):
	string_prefix = 'You have selected: '
	log.print('called function')
	myDatePicker = getScreenVariables().get('myDatePicker')

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
	log.print('and there')
	return str(myDatePicker.getSelectedRange())

#More complicated case, which uses state of third element
def simpleExample1(start_date, end_date, start_date1, end_date1):
	return str(start_date) + ' ' + str(end_date) + ' ' + str(start_date1) + ' ' + str(end_date1)

#Cse, when we access the other elements, not connected to input and output of callback, through dictionary
def press(n):
	a = getScreenVariables().get('myDatePicker')
	b = getScreenVariables().get('myDatePicker1')
	c = getScreenVariables().get('myOutput')
	d = getScreenVariables().get('myOutput1')
	return str(a.getSelectedRange()) + str(b.getSelectedRange()) + str(c.getText()) + str(d.getText())