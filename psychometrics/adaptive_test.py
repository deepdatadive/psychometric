from __future__ import print_function, division, unicode_literals
import numpy as np
import operator
import functools
import math
from numpy.polynomial.hermite import hermgauss
from psychometrics.simulation import simulate_items, item_vectors
import random
import pandas as pd
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

#todo adaptive content balancing

'''
This module is designed to emulate an adaptive test based on a one, two or three parameter logistic model. 
'''

def _p_1pl(ability, difficulty, discrimination=1, rasch=False):
    '''
    The probability that this person gets this question correct
    alpha = discrimination of the test
    theta = ability of person
    -beta / alpha = difficulty of question
    '''
    item_count = difficulty.size
    discrimination = np.full(item_count,fill_value=discrimination)
    if rasch==True:
        xb = 1.7*discrimination*(ability-difficulty)
    else:
        xb = 1.7 * discrimination * (ability - difficulty)
    return np.exp(xb) / (1 + np.exp(xb))

def _p_2pl(discrimination, ability, difficulty):
    '''
    The probability that this person gets this question correct
    alpha = discrimination of the test
    theta = ability of person
    -beta / alpha = difficulty of question
    '''
    xb = discrimination*(ability-difficulty)
    return np.exp(xb) / (1 + np.exp(xb))

def _p_3pl(ability, discrimination, difficulty, guessing):
    '''
    The probability that this person gets this question correct
    alpha = discrimination of the test
    theta = ability of person
    -beta / alpha = difficulty of question
    '''
    xb = discrimination*(ability-difficulty)
    return guessing + (1-guessing)*(np.exp(xb) / (1 + np.exp(xb)))


def items_remaining(data, items_taken):
    ix = [i for i in data.index if i not in items_taken]
    remaining = data.loc[ix]
    return remaining


def select_next_item(items, theta, model='1PL'):
    a = np.array(items.iloc[:, 0])
    current_probabilities = _p_1pl(a, theta)
    if model == '2PL':
        b = np.array(items.iloc[:, 1])
        current_probabilities = _p_2pl(a, theta, b)

    elif model == '3PL':
        b = np.array(items.iloc[:, 1])
        c = np.array(items.iloc[:, 2])
        current_probabilities = _p_3pl(a, theta, b, c)

    items['probability'] = current_probabilities
    items['closest_prob'] = list(abs(.5 - current_probabilities))
    next_item = items['closest_prob'].idxmin()
    return items, next_item


def _f(ys, alpha, theta, betas):
    '''
    The probability of observing this person's responses (ys) given
    the discrimination of the test, the person's ability, and the
    difficulty of the questions.
    '''
    ps = _p_2pl(alpha, theta, betas)
    qs = 1 - ps
    return np.prod(np.power(ps, ys) * np.power(qs, 1 - ys))


def get_probabilities(discrimination, ability, difficulty):
    probability = math.exp(discrimination*(ability-difficulty))/(1+math.exp(discrimination*(ability-difficulty)))
    return probability


def L(ys, alpha, betas):
    '''
    How likely are we to see these responses (ys) given the
    discrimination of the test and the difficulty of the
    questions. Note, we integrate over all person abilities so it's as
    if a random person from the population took the test.
    '''
    possible_abilities = list(np.arange(-4, 4, .01))
    def f(x):
        return _f(ys=ys, alpha=alpha, theta=x, betas=betas)
    y = [f(x) for x in possible_abilities]
    max_value = y.index(max(y))
    return max_value, possible_abilities[max_value]


def item_information(alpha, beta, guessing, model='2PL'):

    possible_abilities = list(np.arange(-4, 4, .01))

    if model == '1PL':
        def f(x):
            return _p_1pl(ability=x, difficulty=beta, discrimination=1, rasch=False)
    elif model == '2PL':
        def f(x):
            return _p_2pl(discrimination=alpha, ability=x, difficulty=beta)
    else:
        def f(x):
            return _p_3pl(ability=x, discrimination=alpha, difficulty=beta, guessing=guessing)


    ps = [f(x) for x in possible_abilities]
    qs = [1-p for p in ps]

    ps_qs = np.multiply(np.array(ps),np.array(qs))
    y = alpha*alpha*np.array(ps_qs)
    info_dict = {'information': y,
                 'quad': possible_abilities}
    return info_dict

def multistage_adaptive(stage, level, items, results):
    def Average(lst):
        return sum(lst) / len(lst)

    next_stage = stage + 1
    current_stage_items = items[(items['stage'] == stage) & (items['level']==level)]
    next_stage_items = items[(items['stage'] == next_stage)]
    levels_in_next_stage = next_stage_items.level.unique().tolist()
    max_prob, theta_estimate = L(np.array(results), np.array(current_stage_items['a']), np.array(current_stage_items['b']))
    probability_next_levels = []
    for next_level in levels_in_next_stage:
        new_list = []
        next_stage_level_items = next_stage_items[next_stage_items['level'] == next_level]
        for index, row in next_stage_level_items.iterrows():
            probability = _p_2pl(row['a'], theta_estimate, row['b'])
            new_list.append(abs(.5 - probability))
        probability_next_levels.append(Average(new_list))

    next_level = probability_next_levels.index(min(probability_next_levels)) + 1

    return next_stage, next_level




# df = pd.read_csv('/home/cfoster/PycharmProjects/psychometric/data/multistage_setup.csv')
#
# next_stage, next_level = multistage_adaptive(stage=1, level=1, items=df, results=[0,1,1])
#
# item_list = [{
#     'a':.5,
#     'b':1.5,
#     'c':.25
# }, {
#     'a':1,
#     'b':0,
#     'c':.2
# }, {
#     'a':1.5,
#     'b':-1,
#     'c':.25
# }]
#
#
#
#
# max_prob, theta_estimate = L(np.array([ 1, 1, 1, 1, 0]), np.array([.5, .6, .7, .8, .9]),
#                              np.array([-3, -2, 0, 2, 3]))
#
# print(max_prob, theta_estimate)