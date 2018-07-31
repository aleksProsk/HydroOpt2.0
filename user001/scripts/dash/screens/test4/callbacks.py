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

def setPointCoordinates(n_clicks, id, clickData, lat, lon):

    myTopologyMap = screenVariables.get(getNameFromId(id))
    if clickData == None:
        return myTopologyMap.getFigure()
    point = CSafePoint(clickData)
    pointData = point.getPoint()
    setIndex = pointData.get('curveNumber')
    pointIndex = pointData.get('pointIndex')
    return myTopologyMap.setNewCoordinatesForPoint(setIndex, pointIndex, lat, lon)
