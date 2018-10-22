import pandas as pd
import numpy as np
import math
import random
import time

'''
This section is designed to simulate examinees for use in other modules or for any other experimental purpose. 
It is possible to simulate IRT parameters for items, ability parameters for examinees or response strings (correct/incorrect) 
for each simulated item for each examinee.
'''


def simulate_items(difficulty={'mean': 0, 'sd': 1}, discrimination={'mean': 1, 'sd': 0}, guessing=None, item_count=50):
    '''
    Simulates item parameters for the one, two and three parameter models. For the one parameter model keep the the
    discrimination sd equal to 0.
    :param difficulty: a dictionary with keys mean and sd
    :param discrimination: a dictionary with keys mean and sd
    :param guessing: a dictionary with keys mean and sd
    :param item_count: an integer for how many items you wish to simulate
    :return: A dictionary with keys 'a', 'b' and 'c' each containing a vector of length equal to item count with the corresponding parameters
    '''

    b = np.random.normal(difficulty['mean'], difficulty['sd'], item_count)

    if discrimination['sd'] != 0:
        a = np.random.normal(discrimination['mean'], discrimination['sd'], item_count)
    else:
        a = np.array([discrimination['mean']] * item_count)
        a = np.array(a)

    if guessing is not None:
        c = np.random.normal(guessing['mean'], guessing['sd'], item_count)
    else:
        c = None

    item_dict = {
        'a': a,
        'b': b,
        'c': c
    }
    return item_dict


def get_probabilities(discrimination, ability, difficulty):
    '''
    Estimates the probability of a correct response for the 2 parameter model for an item of a given difficult and discrimination for an examinee with ability theta
    :param discrimination: discrimination parameter for item
    :param ability: examinee estimated theta
    :param difficulty: a difficutly parameter for an item
    :return: the probability an examinee with a given ability will get the question correct.
    '''
    probability = math.exp(discrimination*(ability-difficulty))/(1+math.exp(discrimination*(ability-difficulty)))
    return probability


def simulate_people(examinee_count, information):
    '''
    Simulates theta parameters for examinees sampled from a normal distribution.
    :param examinee_count: how many examinees you wish to simulate
    :param information: dictionary with keys 'mean' and 'sd' representing the mean and standard deveviation.
    :return: a list of examinee abilities
    '''
    examinee_abilities = list(np.random.normal(information['mean'], information['sd'], examinee_count))
    return examinee_abilities


def item_vectors(items, abilities):
    '''

    :param items: a dictionary (usually from the simulate items function) which contains keys 'a', 'b', and 'c' which are vectors containing the parameters of items.
    :param abilities: a list of examinee abilities
    :return: two dataframes: one containing the probabilities of getting each item correct for each examinee and another containing the correct (1) and incorrect (0) response vectors for each examinee
    '''
    items = pd.DataFrame(items)
    list_of_probabilities = []
    list_of_correct = []
    for ability in abilities:
        person_probabilities = []
        person_correct = []
        for index, row in items.iterrows():
            prob = get_probabilities(discrimination=row['a'], difficulty=row['b'], ability=ability)
            rand_num = random.uniform(0, 1)
            if prob >= rand_num:
                correct = 1
            else:
                correct = 0
            person_probabilities.append(prob)
            person_correct.append(correct)
        list_of_probabilities.append(person_probabilities)
        list_of_correct.append(person_correct)
    df_probabilities = pd.DataFrame(list_of_probabilities)
    df_correct = pd.DataFrame(list_of_correct)
    return df_probabilities, df_correct

def item_vectors_dif(items, abilities, focal, item_list, group_difference):
    '''

    :param items: a dictionary (usually from the simulate items function) which contains keys 'a', 'b', and 'c' which are vectors containing the parameters of items.
    :param abilities: a list of examinee abilities
    :return: two dataframes: one containing the probabilities of getting each item correct for each examinee and another containing the correct (1) and incorrect (0) response vectors for each examinee
    '''
    items = pd.DataFrame(items)
    list_of_probabilities = []
    list_of_correct = []
    count = 0
    for ability in abilities:
        person_probabilities = []
        person_correct = []
        focal_group = []
        for index, row in items.iterrows():
            if count in focal and index in item_list:
                focal_group.append(1)
                prob = get_probabilities(discrimination=row['a'], difficulty=row['b'], ability=ability + group_difference)
                rand_num = random.uniform(0, 1)
                if prob >= rand_num:
                    correct = 1
                else:
                    correct = 0
            else:
                focal_group.append(0)
                prob = get_probabilities(discrimination=row['a'], difficulty=row['b'], ability=ability)
                rand_num = random.uniform(0, 1)
                if prob >= rand_num:
                    correct = 1
                else:
                    correct = 0
            person_probabilities.append(prob)
            person_correct.append(correct)
        list_of_probabilities.append(person_probabilities)
        list_of_correct.append(person_correct)
        count = count + 1
    df_probabilities = pd.DataFrame(list_of_probabilities)
    df_correct = pd.DataFrame(list_of_correct)
    return df_probabilities, df_correct

def cheating_spreading_plague():
    return True


def cheating_pre_knowledge(percent_cheaters=.2, percent_items_comprimised=.5, people_list=[], people=people, item_list=[], items=items, cheating_effect_size=1):

    # Select Cheaters
    if len(people_list) == 0:
        cheater_count = int(len(people)*percent_cheaters)
        cheater_sample = random.sample(range(len(people)), cheater_count)

    else:
        cheater_sample = people_list
    items_frame = pd.DataFrame(items)
    #Get comprimised items
    if len(item_list) == 0:
        comprimised_items = items_frame.sample(frac=percent_items_comprimised)
        comprimised_items_list = comprimised_items.index.tolist()
    else:
        comprimised_items_list = item_list
    prob_cheat, response_cheat = item_vectors_dif(items=items, abilities=people, focal=cheater_sample, item_list=comprimised_items_list, group_difference=cheating_effect_size)
    print(comprimised_items_list)
    return prob_cheat, response_cheat, comprimised_items_list