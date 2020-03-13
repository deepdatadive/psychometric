import pandas as pd

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





