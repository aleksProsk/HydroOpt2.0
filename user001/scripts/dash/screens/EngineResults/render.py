log.print("starting renderer")

data = hydropt.getData(args.get('asset'))
result = data.Asset.ScenarioWaterManager.Result

months = dateUtils.months_from_matlab(np.min(result.DateNum), np.max(result.DateNum))
hours = dateUtils.date_range_from_matlab(np.min(result.DateNum), np.max(result.DateNum))

myKPIFrame = CFrame('Summary', width = 1)
myKPIFrame.aChild(CNumbers([
	['Optimization date', dateUtils.to_str(dateUtils.from_matlab(result.RunTime)), ''],
	['Overall revenue', result.OverallRevenue, 'CHF'],
	['Overall reserve revenue', result.OverallReserveRevenue, 'CHF'],
	['Turbine revenue', result.TurbineRevenue, 'CHF'],
	['Pump costs', result.PumpCost, 'CHF'],
	['Hedge revenue', result.HedgeRevenue, 'CHF'],
	['Hedge value', result.HedgeValue, 'CHF'],
	['Hedge value', result.HedgeValue, 'CHF'],
	]))
#log.print(str(months.year.values.reshape((1,-1)).shape))
#log.print(str(result.MonthlyEnergyPeak.shape))
#log.print(result)

myDataDumpFrame = CFrame('Raw data', width = 1)
myDataDump = CText(args)
myDataDumpFrame.aChild(myDataDump)

rows = (
	np.arange(months.values.size).reshape((-1,1)) + 1,
	months.year.values.reshape((-1,1)),
	months.month.values.reshape((-1,1)),
	result.MonthlyEnergyPeak, 
	result.MonthlyEnergyOffPeak,
	result.MonthlyEnergyPeak+result.MonthlyEnergyOffPeak
)
headers = ['#', 'Year', 'Month', 'Peak [MWh]', 'Offpeak [MWh]', 'Total [MWh]']
myMonthlyResultValueFrame = CFrame('Monthly results table', width = 0.5)
myMonthlyResultTable = CDataTable(rows, headers)
myMonthlyResultValueFrame.aChild(myMonthlyResultTable)

rows = (result.MonthlyEnergyPeak, result.MonthlyEnergyOffPeak)
rowCaptions = months.month.values
headers = ['Peak [MWh]', 'Offpeak [MWh]']
myMonthlyResultChartFrame = CFrame('Monthly results chart', width = 1)
myMonthlyResultChart = CChart(rows, headers, rowCaptions, "Monthly results", barmode='stack')
myMonthlyResultChartFrame.aChild(myMonthlyResultChart)

hpfc = result.ExpectedSpotPrice 
myPriceFrame = CFrame('Market', width = 0.5)
myPriceChart = CChart([hpfc], ['HPFC [EUR/MWh]'], hours, "HPFC [EUR/MWh]", type='line')
myPriceFrame.aChild(myPriceChart)

myScreen = CPage(args.get('asset') + ' -- Engine results')
#myScreen.aChild(myMonthlyResultValueFrame)
myScreen.aChild(myMonthlyResultChartFrame)
myScreen.aChild(myDataDumpFrame)

return myScreen