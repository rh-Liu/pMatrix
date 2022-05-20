import pandas as pd
import numpy as np

def d_drawdown(data):
    drawdown = 1 - data.div(data.cummax())
    return drawdown

def drawdown_date(data):

    '''
    Dynamic drawdown, and some dates calculation.
    :param data: pv series
    :return:
        md_date_list: max drawdown date.
        md_start_list: the highest point before max drawdown.
        md_recover_list: the date recovered from the max drawdown.
    '''

    drawdown = 1 - data.div(data.cummax())

    md_date_list = []
    md_start_list = []
    md_recover_list = []
    for col in drawdown:
        md_date = drawdown[col].idxmax(axis=0)
        temp = drawdown[col][:md_date]
        md_start = temp[temp==temp.min()].index[-1]
        md_recover = drawdown[col][md_date:].idxmin(axis=0)
        md_date_list.append(md_date.date())
        md_start_list.append(md_start.date())
        md_recover_list.append(md_recover.date())
    return md_date_list, md_start_list, md_recover_list

def p_matrix(data, freq, start, end, exchange='CN'):

    '''
    performance matrix of the data.
    :param data: pv.
    :param freq: trading frequency.
    :param exchange: determine the num of trading days per year.
    :return: performance matrix.
    '''

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
            n = 252
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

def value_cal(ret_df, init_cash=1):

    '''
    Transform the return to the net value.
    :param init_cash: net value at time 0.
    :param ret_df: return series.
    :return: net value.
    '''

    ret_mat = np.array(ret_df)
    value_mat = np.ones([ret_df.shape[0], ret_df.shape[1]]) * init_cash
    for i in range(1, value_mat.shape[0]):
        value_mat[i] = value_mat[i - 1] * (ret_mat[i - 1] + 1)
    value_df = pd.DataFrame(value_mat, index=ret_df.index, columns=ret_df.columns)
    return value_df