# coding=utf-8
# -*- coding:cp936 -*-
import rpy2.robjects as robj
from rpy2.robjects.packages import importr
importr('tseries')
importr('forecast')


# 作这个时间序列的图,通过图作一个直观判断
rs1 = """
air <- AirPassengers
ts.plot(air)
"""
robj.r(rs1)


# 查看自相关图
rs2 = """
acf(air)
"""
robj.r(rs2)


# 查看偏相关图
rs3 = """
pacf(air)
"""
robj.r(rs3)


# 初步判断 1 有趁势 2 可能有季节性 3 应该使用MA()模型来拟合
# 通过decompose 进行分解：随机、趋势、季节
rs4 = """
x<-decompose(air)
plot(x)
"""
robj.r(rs4)


rs5 = """
plot(x$seasonal)
"""
robj.r(rs5)

# 选择合适的模型拟合  趋势通过差分来消除  季节性因素，确定相应的period
rs6 = """
air.fit <- arima(air,order=c(0,1,1), seasonal=list(order=c(0,1,1), period=12))
"""
robj.r(rs6)


# 对结果进行诊断
rs7 = """
tsdiag(air.fit)
"""
robj.r(rs7)


# 向前预测12期 默认情况下24期 给出80%，95%置信度下的置信区间
rs8 = """
air.forecast <- forecast(air.fit,12)
plot.forecast(air.forecast)
"""
robj.r(rs8)
