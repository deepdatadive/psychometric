from __future__ import print_function, division, unicode_literals
import numpy as np
import operator
import functools
import math
from numpy.polynomial.hermite import hermgauss
from psychometrics.simulation import simulate_items, item_vectors
import random
import pandas as pd

#todo multistage
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

def _p_3pl(discrimination, ability, difficulty, guessing):
    '''
    The probability that this person gets this question correct
    alpha = discrimination of the test
    theta = ability of person
    -beta / alpha = difficulty of question
    '''
    xb = discrimination*(ability-difficulty)
    return guessing + (1-guessing)*(np.exp(xb) / (1 + np.exp(xb)))


# def _f(ys, alpha, theta, betas):
#     '''
#     The probability of observing this person's responses (ys) given
#     the discrimination of the test, the person's ability, and the
#     difficulty of the questions.
#     '''
#     ps = _p_2pl(alpha, theta, betas)
#     qs = 1 - ps
#     return np.prod(np.power(ps, ys) * np.power(qs, 1 - ys))
#
#
# def get_probabilities(discrimination, ability, difficulty):
#     probability = math.exp(discrimination*(ability-difficulty))/(1+math.exp(discrimination*(ability-difficulty)))
#     return probability
#
#
# def L(ys, alpha, betas):
#     '''
#     How likely are we to see these responses (ys) given the
#     discrimination of the test and the difficulty of the
#     questions. Note, we integrate over all person abilities so it's as
#     if a random person from the population took the test.
#     '''
#     def f(x):
#         return _f(ys=ys, alpha=alpha, theta=x, betas=betas)
#     y = [f(x) for x in possible_abilities]
#     max_value = y.index(max(y))
#     return max_value, possible_abilities[max_value]

# possible_abilities = list(np.arange(-4, 4, .01))


def items_remaining(data, items_taken):
    ix = [i for i in data.index if i not in items_taken]
    remaining = data.loc[ix]
    return remaining


def select_next_item(items, theta, model='1PL'):
    a = np.array(items.ix[:, 0])
    current_probabilities = _p_1pl(a, theta)
    if model == '2PL':
        b = np.array(items.ix[:, 1])
        current_probabilities = _p_2pl(a, theta, b)

    elif model == '3PL':
        b = np.array(items.ix[:, 1])
        c = np.array(items.ix[:, 2])
        current_probabilities = _p_3pl(a, theta, b, c)

    items['probability'] = current_probabilities
    items['closest_prob'] = list(abs(.5 - current_probabilities))
    next_item = items['closest_prob'].idxmin()
    return items, next_item

# initialize

