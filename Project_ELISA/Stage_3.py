import pandas as pd
from scipy.optimize import curve_fit


def func(x, A, B, C, D):
    return D + ((A - D) / (1 + (x / C) ** B))

def logistic4x(y, A, B, C, D):
    return C * (((A - D) / (y - D)) - 1) ** (1 / B)

stage = 3

if stage == 1:
    OD_file_name = input()
    OD_file = pd.read_csv(OD_file_name)

    OD_file['AverageOD'] = (OD_file['OD1'] + OD_file['OD2']) / 2
    blank_average = OD_file.loc[OD_file['Sample'] == 'BLANK','AverageOD']

    OD_file['CorrectedOD'] = OD_file['AverageOD'] - blank_average.item()

    OD_file.to_csv('elisa_result.csv', index=False)


if stage == 2:
    ST_file_name = input()
    ST_file = pd.read_csv(ST_file_name)

    ST_file['AverageOD'] = (ST_file['OD1'] + ST_file['OD2']) / 2

    popt, pcov = curve_fit(f=func,
                           ydata=ST_file['AverageOD'],
                           xdata=ST_file['Concentration (ng/ml)'])

    answer = '{:.8f} {:.8f} {:.8f} {:.8f}'.format(popt[0], popt[1], popt[2], popt[3])
    print(answer)

if stage == 3:
    A = 0.04222050
    B = 0.73506386
    C = 7.38040039
    D = 1.05035045

    OD_file_name = input()
    OD_file = pd.read_csv(OD_file_name)

    OD_file['AverageOD'] = (OD_file['OD1'] + OD_file['OD2']) / 2
    blank_average = OD_file.loc[OD_file['Sample'] == 'BLANK','AverageOD']

    OD_file['CorrectedOD'] = OD_file['AverageOD'] - blank_average.item()

    OD_file['Concentration (ng/ml)'] = logistic4x(OD_file['CorrectedOD'], A, B, C, D)

    OD_file.to_csv('elisa_result.csv', index=False)
