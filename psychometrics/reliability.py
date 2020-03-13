import pandas as pd

#todo Parallel Forms, Different Types of Splits

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

#todo Calculate SEM

#todo Calculate SEM using IRT item stats

#todo reliability with item removed

