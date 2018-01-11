import pandas as pd
import numpy as np
import os
import statsmodels
import random
from psychometrics.simulation import simulate_items, simulate_people, item_vectors

'''
This secion is built to implement many commonly used item analysis tools in Classical Test Theory. Included is a method to optain 
coefficient alpha, p-values for all items, discrimination (point biserials and biserals) values for all items and get examinee raw scores.
'''



def examinee_score(items):
    '''
    Returns examinee scores for an exam

    :param items: a pandas dataframe containing the correct (1) and incorrect (0) response patterns for each examinee on every item.
    :return: a vector containing raw scores for the exam.
    '''
    return items.sum(axis=1)

def get_p_values(data):
    '''
    returns p-values for every item in the dataframe

    :param data: a pandas dataframe where columns are items and rows are examinees.
    :return: a vector of p-values for each item in the assessment.
    '''
    p_values = pd.DataFrame(data.mean(axis=0))
    p_values.columns = ['P_Value']
    p_values['Item'] = p_values.index
    return p_values

def k_and_k(items):
    item_count = items.shape[1]
    if item_count > 1:
        return (item_count / float(item_count - 1))
    else:
        return 0


def alpha_without_item(items):
    alpha_without_items = pd.Series(index=items.columns, name='Alpha Without Item')
    for item in items.columns:
        use_items = items.drop(item, axis=1)
        alpha_without_items.ix[item] = k_and_k(use_items) * (1 - (item_var_sum(use_items) / total_var(use_items)))
    return alpha_without_items


def total_var(items):
    return float(items.sum(axis=1).var(ddof=1))


def item_var_sum(items):
    return float(items.var(axis=0, ddof=1).sum())


def calculate_alpha(items):
    '''
    Calculates coefficient alpha for the given exam.

    :param items: a pandas dataframe with columns for each item and rows for each examinee.
    :return: coefficient alpha
    '''
    return k_and_k(items) * (1 - (item_var_sum(items) / total_var(items)))


def discrimination_index(items):
    '''
    Calculates the point biserial and biserial for each item on the exam. Essentially these are item-total correlations where the item is not included in the total score (point-biserial) and is included int he total score (biserial).

    :param items: a pandas dataframe with columns for each item and rows for each examinee.
    :return: two dataframes. one containing the point-biserials and the other containing the biserials
    '''
    stat_without_item = pd.Series(index=items.columns, name='Point Biseral')
    for item in items.columns:
        total_deitemed = examinee_score(items) - items[item]
        stat_without_item.ix[item] = items[item].corr(total_deitemed)

    stat_with_item = pd.Series(index=items.columns, name='Biserial')
    for item in items.columns:
        total = examinee_score(items)
        stat_with_item.ix[item] = items[item].corr(total)
    return stat_without_item, stat_with_item


