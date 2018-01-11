import pandas as pd
import numpy as np
import math
import random
import time

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
