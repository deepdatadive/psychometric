from psychometrics.simulation import simulate_items, simulate_people, item_vectors
import random
import numpy as np
from psychometrics.CTT import examinee_score
import pandas as pd

def test_descriptives(items):
    test_scores = items.sum(axis=1)
    hist_data = test_scores.value_counts()
    test_info = {'min_score': test_scores.min(),
                'max_score': test_scores.max(),
                'score_sd': test_scores.std(),
                'score_var': test_scores.var(),
                'average_score': test_scores.mean(),
                'median_score': test_scores.median(),
                'score_hist_data': hist_data.to_json(),
                'completed_examinee_count':items.shape[0],
                'item_count': items.shape[1]}
    return test_info

def total_test_times(data, time_column='time', long_column=['examine_id']):
    test_info = data.groupby(long_column)[time_column].agg('sum')
    return test_info


# items = simulate_items()
# people = simulate_people(100, {'mean': 0, 'sd': 1})
# prob_vector, response_vector = item_vectors(items, people)
# examinee_scores = examinee_score(response_vector)
#
# val = examinee_scores.value_counts()
# dictstuff = test_descriptives(response_vector)
# print(dictstuff)