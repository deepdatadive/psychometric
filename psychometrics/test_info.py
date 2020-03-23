from psychometrics.simulation import simulate_items, simulate_people, item_vectors
import random
import numpy as np

random.seed(123)
np.random.seed(123)

def test_descriptives(items):
    test_scores = items.sum(axis=1)
    test_info = {'min_score': test_scores.min(),
                'max_score': test_scores.max(),
                'score_sd': test_scores.std(),
                'score_var': test_scores.var(),
                'average_score': test_scores.mean(),
                'median_score': test_scores.median(),
                'completed_examinee_count':items.shape[0],
                'item_count': items.shape[1]}
    return test_info



# items = simulate_items()
# people = simulate_people(100, {'mean': 0, 'sd': 1})
# prob_vector, response_vector = item_vectors(items, people)
# examinee_scores = examinee_score(response_vector)
# dictstuff = test_descriptives(response_vector)
# print(dictstuff)