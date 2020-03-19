import pandas as pd
from psychometrics.CTT import examinee_score
import math
import numpy as np
from scipy.stats.stats import pearsonr

def k_and_k(items):
    item_count = items.shape[1]
    if item_count > 1:
        return (item_count / float(item_count - 1))
    else:
        return 0

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

def calculate_split_half(items, split='odds'):

    if split == 'odds':
        odds = items.iloc[1::2]
        evens = items.iloc[::2]
        odds_scores = examinee_score(odds)
        evens_scores = examinee_score(evens)
        reliability = pearsonr(odds_scores, evens_scores)

    elif split == "first":
        df1 = items.iloc[:, :items.shape[0]/2]
        df2 = items.iloc[:, items.shape[0]/2:]
        df1 = examinee_score(df1)
        df2 = examinee_score(df2)
        reliability = pearsonr(df1, df2)

    elif split == 'random:':
        df1 = items.sample(frac=0.5)
        df1 = df1.reset_index()
        df2 = items.drop(df1.index)
        df1.drop(['index'], axis=1)
        df1 = examinee_score(df1)
        df2 = examinee_score(df2)
        reliability = pearsonr(df1, df2)

    else:
        print("error, please select a valid split")

    return reliability

def calculate_sem(items, reliability=None):

    if reliability == None:
        reliability = calculate_alpha(items)
    total_scores = examinee_score(items)
    std = np.array(total_scores)
    return std*math.sqrt(1-reliability)

#todo Calculate SEM using IRT item stats


