# coding=utf-8
# -*- coding:cp936 -*-
import rpy2.robjects as robj
from rpy2.robjects.packages import importr

importr('forecast')

rs1 = """
air <- AirPassengers
fit <- auto.arima(air)
plot(forecast(fit, h=30))
"""
robj.r(rs1)
