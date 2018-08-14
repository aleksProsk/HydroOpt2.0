def addRow(n_clicks):
    table = screenVariables.get('inputTable')
    return table.addRow()

def updateChart(rows, smoothing, deg):
    figure = screenVariables.get('myChart').getValue()
    figure = CSafeFigure(figure=figure)
    myLst = CSafeList(lst=rows)
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

def loadModal(n_clicks, n_clicks1, oldStyle):
    log.print('here')
    style = CSafeDict(oldStyle)
    if n_clicks1 is None or n_clicks > n_clicks1:
        style.set('display', 'block')
    else:
        style.set('display', 'none')
    return style.getDict()

Clicks = CSafeList()
def selectListInteraction(*clicks):
    global Clicks
    clicks = CSafeList(lst=clicks)
    selectList = screenVariables.get('mySelectList')
    i = 0
    while Clicks.len() < clicks.len():
        Clicks.append(0)
    while i < clicks.len():
        z = clicks.get(i)
        if z is None:
            clicks.set(i, 0)
        i = i + 1
    selected = 'none'
    i = 0
    while i < clicks.len():
        if clicks.get(i) != Clicks.get(i):
            if i == 0:
                selected = 'all'
            else:
                selected = i
        i = i + 1
    selectedList = CSafeList(lst=selectList.getSelected())
    log.print('was: ')
    log.print(selectList.getSelected())
    i = 0
    while i < clicks.len():
        if selected == i:
            selectedList.set(i, selectedList.get(i) ^ 1)
        elif selected == 'all':
            selectedList.set(i, 1)
        i = i + 1
    log.print('now: ')
    log.print(selectedList.getList())
    return selectList.select(selectedList.getList())
