import pandas as pd
import math
from scipy.optimize import curve_fit


def logistic4y(x, A, B, C, D):
    return D + ((A - D) / (1 + (x / C) ** B))

def logistic4x(y, A, B, C, D):
    x = (C * (((A - D) / (y - D)) - 1) ** (1 / B))
    for i in range(len(x)):
        if isinstance(x[i], float) and math.isnan(x[i]):
            x[i] = 0
    return x

def elisa_automation(OD, ST):
    ST['AverageOD'] = (ST['OD1'] + ST['OD2']) / 2

    popt, pcor = curve_fit(f=logistic4y,
                           ydata=ST['AverageOD'],
                           xdata=ST['Concentration (ng/ml)'])

    OD['AverageOD'] = (OD['OD1'] + OD['OD2']) / 2
    blank_average = OD.loc[OD['Sample'] == 'BLANK','AverageOD']

    OD['CorrectedOD'] = OD['AverageOD'] - blank_average.item()
    OD['Concentration (ng/ml)'] = logistic4x(y=OD['CorrectedOD'],
                                             A=popt[0],
                                             B=popt[1],
                                             C=popt[2],
                                             D=popt[3])
    return OD

OD_file_name = input()
OD_file = pd.read_csv(OD_file_name)
ST_file_name = input()
ST_file = pd.read_csv(ST_file_name)

EA = elisa_automation(OD_file, ST_file)

EA.to_csv('elisa_result.csv', index=False)
