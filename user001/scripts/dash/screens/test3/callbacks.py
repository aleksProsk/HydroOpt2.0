def updateGraph(value):
    figure = screenVariables.get('myChart').getValue()
    newFigure = CSafeFigure(figure=figure)
    newFigure.restrict(value)
    return newFigure.getFigure()

def resetSlider(n_clicks):
    time.sleep(10)
    slider = screenVariables.get('mySlider')
    return slider.getMinMaxRange()
