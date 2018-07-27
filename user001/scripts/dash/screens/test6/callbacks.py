def addRow(n_clicks):
    table = screenVariables.get('inputTable')
    return table.addRow()

def updateChart(rows, value):
    figure = screenVariables.get('myChart').getValue()
    figure = CSafeFigure(figure=figure)
    myLst = CSafeList(list=rows)
    i = 0
    while i < myLst.len():
        row = CSafeDict(myLst.get(i))
        if row.get('x') != '' and row.get('y') != '':
            figure.addPoint(row.get('x'), row.get('y'), 0)
            if row.get('Method') != '':
                log.print('here')
                figure.setLineType(row.get('Method'), 0, value)
        i = i + 1
    return figure.getFigure()