def getClickData(clickData):
    point = CSafePoint(clickData)
    pointData = point.getPoint()
    log.print(pointData.get('lat'))
    log.print(pointData.get('lon'))
    log.print(pointData.get('customdata'))
    log.print(pointData.get('pointIndex'))
    log.print(pointData.get('pointNumber'))
    log.print(pointData.get('curveNumber'))
    return str(pointData.getDict())

def clickState(n_clicks, clickData):
    click = screenVariables.get('myTopologyMap').getValue()
    return str(click) + ' ' + str(clickData)

def getZoom(n_intervals, figure):
    figure = CSafeFigure(figure=figure)
    return figure.getZoom()

def getClickedInfo(clickData):
    point = CSafePoint(clickData)
    pointData = point.getPoint()
    return 'Lat: ' + str(pointData.get('lat')) + ', ' + 'Lon: ' + str(pointData.get('lon')) + ', ' + 'Data: ' + pointData.get('customdata')

clicks = 0
def setPointCoordinates(n_clicks, clickData, id, lat, lon):
    myTopologyMap = screenVariables.get(getNameFromId(id))
    global clicks
    if n_clicks is None:
        n_clicks = 0
    log.print("HEEEEEEEEEEEEEEERE")
    log.print(clicks)
    log.print(n_clicks)
    if clickData is None:
        clicks = n_clicks
        return myTopologyMap.getFigure()
    point = CSafePoint(clickData)
    pointData = point.getPoint()
    setIndex = pointData.get('curveNumber')
    pointIndex = pointData.get('pointIndex')
    if n_clicks != clicks: #no click on figure, click on button
        clicks = n_clicks
        if lat is None or lon is None:
            return myTopologyMap.getFigure()
        return myTopologyMap.setNewCoordinatesForPoint(setIndex, pointIndex, lat, lon)
    else: #click on figure
        return myTopologyMap.highlight(setIndex, pointIndex)