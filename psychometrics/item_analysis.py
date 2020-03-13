import pandas as pd
from psychometrics.CTT import examinee_score
from psychometrics.reliability import k_and_k, item_var_sum, total_var
#todo DOMC
#todo Distractor Analysis
#todo Latency analysis
#todo identify poorly performing items

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

def alpha_without_item(items):
    alpha_without_items = pd.Series(index=items.columns, name='Alpha Without Item')
    for item in items.columns:
        use_items = items.drop(item, axis=1)
        alpha_without_items.ix[item] = k_and_k(use_items) * (1 - (item_var_sum(use_items) / total_var(use_items)))
    return alpha_without_items

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