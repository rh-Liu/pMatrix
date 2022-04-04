import pandas as pd
import numpy as np
from dynamic_drawdown import drawdown_date

def p_matrix(data, freq, start, end, exchange='CN'):

    data = data[start: end]
    ret = data.pct_change(1)

    p_mat = pd.DataFrame()
    # n: frequency per year
    if freq == 'Y':
        n = 1
    elif freq == 'M':
        n = 12
    elif freq == 'D':
        if exchange == 'CN':
            n = 250
        elif exchange == 'US':
            n = 254

    p_mat['Total Return'] = data.iloc[-1] / data.iloc[0] - 1
    # p_mat['Annualized Return1'] = p_mat['Total Return'] / data.shape[0] * n  # 年利率
    p_mat['Annualized Return'] = (p_mat['Total Return'] + 1) ** (n / data.shape[0]) - 1  # 年化利率
    p_mat['Annualized Volatility'] = ret.std(axis=0) * np.sqrt(n)
    p_mat['Shape Ratio'] = p_mat['Annualized Return'] / p_mat['Annualized Volatility']
    p_mat['Sortina Ratio'] = p_mat['Annualized Return'] / (ret[ret < -10e-12].std(axis=0) * np.sqrt(n))
    p_mat['Max Drawdown'] = (1 - data.div(data.cummax())).max()
    p_mat['Calmar Ratio'] = p_mat['Annualized Return'] / p_mat['Max Drawdown']
    p_mat['Max Drawdown Date'], p_mat['Max Drawdown Start'], p_mat['Max Drawdown Recover'] = drawdown_date(data)

    return p_mat

if __name__ == '__main__':
    pv = pd.read_csv('D:\\学习Graduate\\弘量科技\\抗通胀CPI新\\AntiCPI\\results\\backtesting\\US_AntiCPI_rh\\portfolio value.csv', parse_dates=True, index_col=0)
    p_mat = p_matrix(data=pv, freq='M', start='2021-01-01', end='2022-01-01', exchange='US')