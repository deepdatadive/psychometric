# Changed
# from psychometrics.simulation import simulate_items, simulate_people, item_vectors, get_probabilities
# import random
# import numpy as np
# import pandas as pd
#
# np.random.seed(123)
# random.seed(123)
#
# item_count = 50
# person_count = 100
# fixed_test_length = 40
#
# people = simulate_people(person_count, information={'mean': 0, 'sd': 1})
#
# # Simulate a bunch of items
# items = simulate_items(difficulty={'mean': 0, 'sd': 1}, discrimination={'mean': 1, 'sd': .05}, guessing=None,
#                        item_count=item_count)
#
# items_frame = pd.DataFrame(items)
# probabilities, response_vector = item_vectors(items=items, abilities=people)
#
#
#
# def item_vectors_dif(items, abilities, focal, item_list, group_difference):
#     '''
#
#     :param items: a dictionary (usually from the simulate items function) which contains keys 'a', 'b', and 'c' which are vectors containing the parameters of items.
#     :param abilities: a list of examinee abilities
#     :return: two dataframes: one containing the probabilities of getting each item correct for each examinee and another containing the correct (1) and incorrect (0) response vectors for each examinee
#     '''
#     items = pd.DataFrame(items)
#     list_of_probabilities = []
#     list_of_correct = []
#     count = 0
#     for ability in abilities:
#         person_probabilities = []
#         person_correct = []
#         focal_group = []
#         for index, row in items.iterrows():
#             if count in focal and index in item_list:
#                 focal_group.append(1)
#                 prob = get_probabilities(discrimination=row['a'], difficulty=row['b'], ability=ability + group_difference)
#                 rand_num = random.uniform(0, 1)
#                 if prob >= rand_num:
#                     correct = 1
#                 else:
#                     correct = 0
#             else:
#                 focal_group.append(0)
#                 prob = get_probabilities(discrimination=row['a'], difficulty=row['b'], ability=ability)
#                 rand_num = random.uniform(0, 1)
#                 if prob >= rand_num:
#                     correct = 1
#                 else:
#                     correct = 0
#             person_probabilities.append(prob)
#             person_correct.append(correct)
#         list_of_probabilities.append(person_probabilities)
#         list_of_correct.append(person_correct)
#         count = count + 1
#     df_probabilities = pd.DataFrame(list_of_probabilities)
#     df_correct = pd.DataFrame(list_of_correct)
#     return df_probabilities, df_correct
#
# def cheating_spreading_plague():
#     return True
#
# def differential_item_functioning():
#     return True
#
#
# def cheating_pre_knowledge(percent_cheaters=.2, percent_items_comprimised=.5, people_list=[], people=people, item_list=[], items=items, cheating_effect_size=1):
#
#     # Select Cheaters
#     if len(people_list) == 0:
#         cheater_count = int(len(people)*percent_cheaters)
#         cheater_sample = random.sample(range(len(people)), cheater_count)
#
#     else:
#         cheater_sample = people_list
#     items_frame = pd.DataFrame(items)
#     #Get comprimised items
#     if len(item_list) == 0:
#         comprimised_items = items_frame.sample(frac=percent_items_comprimised)
#         comprimised_items_list = comprimised_items.index.tolist()
#     else:
#         comprimised_items_list = item_list
#     prob_cheat, response_cheat = item_vectors_dif(items=items, abilities=people, focal=cheater_sample, item_list=comprimised_items_list, group_difference=cheating_effect_size)
#     print(comprimised_items_list)
#     return prob_cheat, response_cheat, comprimised_items_list
#
# cheating_pre_knowledge(people=people)
