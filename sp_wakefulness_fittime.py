import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
from numpy import log as ln
import math

Male_list_W1 = [0.63333333, 0.70909091, 0.69393939, 0.6969697, 0.70909091, 0.70606061, 0.72121212]
Female_list_W1 = [0.83939394, 0.85757576, 0.66363636, 0.62727273, 0.67575758, 1., 0.8030303]

Male_list_W2 = [0.61818182, 0.6030303, 0.45151515, 0.70606061, 0.66060606, 0.58787879, 0.72121212]
Female_list_W2 = [0.68484848, 0.75454545, 0.6, 0.56363636, 0.66666667, 0.82727273, 0.83636364]

Male_list_RORR1 = [0.01212121, 0.02727273, 0.0030303, 0.06666667, 0.02121212, 0., 0.03636364]
Female_list_RORR1 = [0.03939394, 0.0030303, 0.00606061, 0.00606061, 0., 0.00909091, 0.01515152]

Male_list_RORR2 = [0.06969697, 0.04545455, 0.06363636, 0.14848485, 0.02121212, 0.04242424, 0.37878788]
Female_list_RORR2 = [0.08787879, 0.0030303, 0.01818182, 0.21818182, 0.01818182, 0.11515152, 0.09090909]

Male_list_RORR3 = [0.16666667, 0.02727273, 0.05454545, 0.16060606, 0.17272727, 0.2, 0.1969697]
Female_list_RORR3 = [0.1030303, 0.16363636, 0., 0.0969697, 0.22424242, 0.11515152, 0.27575758]

Male_list_RORR4 = [0.11818182, 0.1030303, 0.10606061, 0.15454545, 0.23636364, 0.14242424, 0.15757576]
Female_list_RORR4 = [0.26060606, 0.38484848, 0.1030303, 0.12424242, 0.11818182, 0.14848485, 0.4030303]

Male_list_RORR5 = [0.40909091, 0.09090909, 0.16060606, 0.24545455, 0.44545455, 0.61818182, 0.]
Female_list_RORR5 = [0.3030303, 0.47878788, 0.31515152, 0.42121212, 0.25454545, 0.24848485, 0.51818182]
# x_data = Male_list_W1 + Female_list_W1 + Male_list_W2 + Female_list_W2 + Male_list_RORR1 + \
#          Female_list_RORR1 + Male_list_RORR2 + Female_list_RORR2 + Male_list_RORR3 + Female_list_RORR3 \
#          + Male_list_RORR4 + Female_list_RORR4 + Male_list_RORR5 + Female_list_RORR5
# y_data = [1] * 14 + [2] * 14 + [3] * 14 + [4] * 14 + [5] * 14 + [6] * 14 + [7] * 14

y_data = Male_list_RORR1 + \
         Female_list_RORR1 + Male_list_RORR2 + Female_list_RORR2 + Male_list_RORR3 + Female_list_RORR3 \
         + Male_list_RORR4 + Female_list_RORR4 + Male_list_RORR5 + Female_list_RORR5
x_data = [3] * 14 + [4] * 14 + [5] * 14 + [6] * 14 + [7] * 14

# Recast xdata and ydata into numpy arrays so we can use their handy features
xdata = np.asarray(x_data)
ydata = np.asarray(y_data)


# plt.plot(ydata, xdata, 'o')
# df=pd.dataframe(data,columns=[‘Name’,’Age’])

# Define the Gaussian function
def Gauss(x, A, B):
    y = A * np.exp(-1 * B * x ** 2)  # y = 0.03997673527789254 * np.exp(0.04275123842656964 * x ** 2)
    return y


parameters, covariance = curve_fit(Gauss, xdata, ydata)

fit_A = parameters[0]
fit_B = parameters[1]
print(fit_A)
print(fit_B)

fit_y = Gauss(xdata, fit_A, fit_B)
plt.plot(xdata, ydata, 'o', label='data')
plt.plot(xdata, fit_y, '-', label='fit')
plt.legend()

SE = np.sqrt(np.diag(covariance))
SE_A = SE[0]
SE_B = SE[1]


# print(F'The value of A is {fit_A:.5f} with standard error of {SE_A:.5f}.')
# print(F'The value of B is {fit_B:.5f} with standard error of {SE_B:.5f}.')


def delay_time(value):
    A = value / fit_A
    B = ln(A)
    C = -B / fit_B
    x = np.sqrt(C) * 5

    return x


# from sympy.solvers import solve
# from sympy import Symbol
#
# x = Symbol('x')
# print(solve(0.7006493507142857= 0.03997673527789254 * np.exp(0.04275123842656964 * x ** 2), x))
mean = np.mean(Male_list_W1 + Female_list_W1 + Male_list_W2 + Female_list_W2)
var1 = np.var(Male_list_W1 + Female_list_W1 + Male_list_W2 + Female_list_W2)
x1 = mean + 4 * var1
x2 = mean - 4 * var1

# x = np.sqrt(ln(A) / (-0.04275123842656964))

y1 = delay_time(x1)
y2 = delay_time(x2)
print('拟合曲线预测时间范围为：', [y2, y1])
