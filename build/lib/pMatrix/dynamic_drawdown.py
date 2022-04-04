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