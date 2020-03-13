from psychometrics.simulation import simulate_items, simulate_people, item_vectors
from psychometrics.CTT import examinee_score
from psychometrics.test_info import test_descriptives
import pandas as pd
import numpy as np

# Equating

# todo: CTT - Linear Equating
# Ctodo: TT - Equipercentile Equating
#
# todo: IRT - Fixed Ancor
# todo: IRT - Conversion Equating
#todo concurrent IRT

def mean_equating(initial_data, subsequent_data, sd_equating=False):
    test1_info = test_descriptives(initial_data)
    test2_info = test_descriptives(subsequent_data)
    score_difference = test1_info['average_score'] - test2_info['average_score']
    initial_scores = examinee_score(subsequent_data)
    subsequent_scores = examinee_score(subsequent_data) + score_difference
    print(test1_info, test2_info)

    equating_dict = {
        'initial_scores': initial_scores,
        'mean_equated_scores': subsequent_scores,
        'mean_sd_equated_scores': None
    }

    equating_df = pd.DataFrame(equating_dict)

    if sd_equating == True:
        sd_division = test1_info['score_sd']/test2_info['score_sd']
        equating_df['mean_sd_equated_scores'] = (sd_division)*equating_df['initial_scores'] + (test1_info['average_score'] - sd_division*test2_info['average_score'])
        equating_dict = equating_df.to_dict()

    return equating_dict



items1 = simulate_items()
items2= simulate_items(difficulty={'mean':1, 'sd':1})
people = simulate_people(100, {'mean': 0, 'sd': 1})
prob_vector1, response_vector1 = item_vectors(items1, people)
prob_vector2, response_vector2 = item_vectors(items2, people)
examinee_scores1 = examinee_score(response_vector1)
examinee_scores2 = examinee_score(response_vector2)
print(mean_equating(response_vector1, response_vector2, sd_equating=True))