def addRow(n_clicks):
    table = screenVariables.get('inputTable')
    return table.addRow()

def updateChart(rows, smoothing, deg):
    figure = screenVariables.get('myChart').getValue()
    figure = CSafeFigure(figure=figure)
    myLst = CSafeList(list=rows)
    i = 0
    mthd = 'linear'
    while i < myLst.len():
        row = CSafeDict(myLst.get(i))
        if row.get('x') != '' and row.get('y') != '':
            figure.addPoint(row.get('x'), row.get('y'), 0)
            if row.get('Method') != '':
                mthd = row.get('Method')
        i = i + 1
    figure.setLineType(mthd, 0, smoothing, deg)
    return figure.getFigure()