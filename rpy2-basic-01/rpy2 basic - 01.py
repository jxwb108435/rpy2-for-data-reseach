# coding=utf-8
# -*- coding:cp936 -*-

import rpy2.robjects as robj
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
import pandas as pd
import matplotlib.pyplot as plt

# Now that we have these objects in loaded, we can call them similar to standard Python practices
ts = robj.r('ts')
forecast = importr('forecast')

# These a key to transforming certain datatypes from Python to R.
pandas2ri.activate()

traindf = pd.read_csv('UKgas.csv', index_col=0)


def trans_date(_num):
    """ 1980.25  -> 1985-4-1 """
    import math
    _year = int(math.modf(_num)[1])
    _month = int(12 * math.modf(_num)[0] + 1)

    return str(_year) + '-' + str(_month) + '-1'


traindf.index = pd.to_datetime(traindf['time'].apply(trans_date))

rdata = ts(traindf.UKgas.values, frequency=4)
fit = forecast.auto_arima(rdata)
forecast_output = forecast.forecast(fit, h=16, level=95.0)

index = pd.date_range(start=traindf.index.max(), periods=len(forecast_output[3]) + 1, freq='QS')[1:]

forecast = pd.Series(forecast_output[3], index=index)
lowerpi = pd.Series(forecast_output[4], index=index)
upperpi = pd.Series(forecast_output[5], index=index)

fig = plt.figure(figsize=(16, 7))
ax = plt.axes()
ax.plot(traindf.index, traindf.UKgas.values, color='blue', alpha=0.5)
ax.plot(forecast.index, forecast.values, color='red')
ax.fill_between(forecast.index, lowerpi.values, upperpi.values, alpha=0.2, color='red')


# Blocking R code into a Function
rstring = """
    function(testdata){
        library(forecast)
        fitted_model<-auto.arima(testdata)
        forecasted_data<-forecast(fitted_model,h=16,level=c(95))
        outdf<-data.frame(forecasted_data$mean,forecasted_data$lower,forecasted_data$upper)
        colnames(outdf)<-c('forecast','lower_95_pi','upper_95_pi')
        outdf
    }
"""

rfunc = robj.r(rstring)
rdata2 = ts(traindf.UKgas.values, frequency=4)
r_df = rfunc(rdata2)

forecast_df = pandas2ri.ri2py(r_df)
forecast_df.index = pd.date_range(start=traindf.index.max(), periods=len(forecast_df) + 1, freq='QS')[1:]

fig2 = plt.figure(figsize=(16, 7))
ax = plt.axes()
ax.plot(traindf.index, traindf.UKgas.values, color='blue', alpha=0.5)
ax.plot(forecast_df.index, forecast_df.forecast.values, color='red')
ax.fill_between(forecast_df.index, forecast_df['lower_95_pi'], forecast_df['upper_95_pi'], alpha=0.2, color='red')
