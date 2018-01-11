import unittest
import pandas as pd
import numpy as np
from .IRT import Irt
from .simulation import simulate_people, simulate_items, item_vectors
from .adaptive_test import items_remaining, select_next_item, _p_2pl, L
import random
from .CTT import calculate_alpha, discrimination_index, get_p_values, examinee_score

# class TestIrt(unittest.TestCase):
#
#     def test_irt(self):
#         '''
#         Here is the expected output from this model:
#
#         . use http://www.stata-press.com/data/r15/masc1
#         (Data from De Boeck & Wilson (2004))
#
#         . irt 2pl *, intmethod(ghermite)
#
#         Fitting fixed-effects model:
#
#         Iteration 0:   log likelihood = -4275.6606
#         Iteration 1:   log likelihood = -4269.7861
#         Iteration 2:   log likelihood = -4269.7825
#         Iteration 3:   log likelihood = -4269.7825
#
#         Fitting full model:
#
#         Iteration 0:   log likelihood = -4146.9881
#         Iteration 1:   log likelihood = -4119.5698
#         Iteration 2:   log likelihood = -4118.7376
#         Iteration 3:   log likelihood = -4118.7354
#         Iteration 4:   log likelihood = -4118.7354
#
#         Two-parameter logistic model                    Number of obs     =        800
#         Log likelihood = -4118.7354
#         ------------------------------------------------------------------------------
#                      |      Coef.   Std. Err.      z    P>|z|     [95% Conf. Interval]
#         -------------+----------------------------------------------------------------
#         q1           |
#              Discrim |   1.591376   .2340873     6.80   0.000     1.132573    2.050179
#                 Diff |  -.4786277   .0755632    -6.33   0.000    -.6267289   -.3305265
#         -------------+----------------------------------------------------------------
#         q2           |
#              Discrim |   .6568686   .1161955     5.65   0.000     .4291296    .8846075
#                 Diff |  -.1524701   .1204896    -1.27   0.206    -.3886254    .0836853
#         -------------+----------------------------------------------------------------
#         q3           |
#              Discrim |    .922717   .1568708     5.88   0.000     .6152559    1.230178
#                 Diff |  -1.713807   .2427667    -7.06   0.000    -2.189621   -1.237993
#         -------------+----------------------------------------------------------------
#         q4           |
#              Discrim |   .8161676    .128136     6.37   0.000     .5650257     1.06731
#                 Diff |   .3297224   .1079496     3.05   0.002      .118145    .5412997
#         -------------+----------------------------------------------------------------
#         q5           |
#              Discrim |   .8959221   .1543132     5.81   0.000     .5934737     1.19837
#                 Diff |   1.590873   .2330593     6.83   0.000     1.134085    2.047661
#         -------------+----------------------------------------------------------------
#         q6           |
#              Discrim |   .9757092   .1465112     6.66   0.000     .6885526    1.262866
#                 Diff |   .6257779   .1121996     5.58   0.000     .4058708    .8456851
#         -------------+----------------------------------------------------------------
#         q7           |
#              Discrim |   .3575528   .1112875     3.21   0.001     .1394334    .5756722
#                 Diff |    2.82503   .8622307     3.28   0.001     1.135089    4.514971
#         -------------+----------------------------------------------------------------
#         q8           |
#              Discrim |   1.394495   .2309686     6.04   0.000     .9418049    1.847185
#                 Diff |  -1.721327   .1914727    -8.99   0.000    -2.096606   -1.346047
#         -------------+----------------------------------------------------------------
#         q9           |
#              Discrim |   .6326524   .1217531     5.20   0.000     .3940208    .8712841
#                 Diff |  -1.520289   .2815504    -5.40   0.000    -2.072117   -.9684599
#         ------------------------------------------------------------------------------
#
#         Here are the results from using ltm in R:
#
#         > library(ltm)
#         > fit <- ltm(x ~ z1, control = list(GHk = 7))
#         > summary(fit)
#
#         Call:
#         ltm(formula = x ~ z1, control = list(GHk = 7))
#
#         Model Summary:
#            log.Lik      AIC      BIC
#          -4118.735 8273.471 8357.794
#
#         Coefficients:
#                     value std.err  z.vals
#         Dffclt.q1 -0.4786  0.0756 -6.3341
#         Dffclt.q2 -0.1525  0.1205 -1.2654
#         Dffclt.q3 -1.7138  0.2428 -7.0595
#         Dffclt.q4  0.3297  0.1079  3.0544
#         Dffclt.q5  1.5909  0.2331  6.8260
#         Dffclt.q6  0.6258  0.1122  5.5774
#         Dffclt.q7  2.8250  0.8622  3.2764
#         Dffclt.q8 -1.7213  0.1915 -8.9899
#         Dffclt.q9 -1.5203  0.2816 -5.3997
#         Dscrmn.q1  1.5914  0.2341  6.7982
#         Dscrmn.q2  0.6569  0.1162  5.6531
#         Dscrmn.q3  0.9227  0.1569  5.8820
#         Dscrmn.q4  0.8162  0.1281  6.3695
#         Dscrmn.q5  0.8959  0.1543  5.8059
#         Dscrmn.q6  0.9757  0.1465  6.6596
#         Dscrmn.q7  0.3576  0.1113  3.2129
#         Dscrmn.q8  1.3945  0.2310  6.0376
#         Dscrmn.q9  0.6327  0.1218  5.1962
#
#         Integration:
#         method: Gauss-Hermite
#         quadrature points: 7
#
#         Optimization:
#         Convergence: 0
#         max(|grad|): 7.1e-05
#         quasi-Newton: BFGS
#         '''
#         data = pd.read_csv('data/masc1.csv')
#         endog = data.as_matrix()
#         model = Irt(endog).fit(method='bfgs')
#         print(model.summary())


class TestExamineeSimulation(unittest.TestCase):

    def test_examinee(self):
        np.random.seed(123)
        examinees = simulate_people(examinee_count=3, information={'mean': 0, 'sd': 1})
        self.assertEqual(examinees, [-1.0856306033005612, 0.99734544658358582, 0.28297849805199204])


class TestItemSimulation(unittest.TestCase):
    def test_item(self):
        np.random.seed(123)
        items = simulate_items(difficulty={'mean': 0, 'sd': 1}, discrimination={'mean': 1, 'sd': .05}, guessing=None, item_count=3)
        discrim_vector = items['a'].tolist()
        difficulty_vector = items['b'].tolist()
        self.assertEqual(discrim_vector, [0.9246852643040954, 0.9710699874015731, 1.0825718268548576])
        self.assertEqual(difficulty_vector, [-1.0856306033005612, 0.9973454465835858, 0.28297849805199204])


class TestResponseSimulation(unittest.TestCase):
    def test_response_vector(self):
        np.random.seed(123)
        random.seed(123)
        thetas = [0, 1]
        items = simulate_items(difficulty={'mean': 0, 'sd': 1}, discrimination={'mean': 1, 'sd': .05}, guessing=None,
                               item_count=3)
        expected = pd.DataFrame(data={0: [1, 1], 1: [1, 0], 2: [1, 1]})
        probabilities, response_vector = item_vectors(items=items, abilities=thetas)
        self.assertEqual(response_vector[0].tolist(), expected[0].tolist())

class TestAdaptiveTest(unittest.TestCase):

    def test_adaptive_test(self):
        random.seed(123)
        np.random.seed(123)
        theta_estimate = 0
        actual_theta = [0, 1]
        items = simulate_items(difficulty={'mean': 0, 'sd': 1}, discrimination={'mean': 1, 'sd': .05}, guessing=None,
                               item_count=500)

        probabilities, response_vector = item_vectors(items=items, abilities=actual_theta)

        temp = []
        for row in response_vector.iterrows():
            index, data = row
            temp.append(data.tolist())

        items['correct'] = temp[0]
        items_taken = []
        response_list = []
        items = pd.DataFrame(items)
        # simulate exam

        for i in range(0, 40):
            remaining = items_remaining(items, items_taken)
            remaining_items, next_item = select_next_item(remaining, theta_estimate)
            item = remaining_items.loc[next_item]
            a = np.array(item['a'])
            b = np.array(item['b'])
            current_probabilities = _p_2pl(a, theta_estimate, b)
            rand_num = random.uniform(0, 1)
            if current_probabilities >= rand_num:
                response_list.append(1)
            else:
                response_list.append(0)
            items_taken.append(next_item)
            new_dataframe = pd.DataFrame(list(zip(items_taken, response_list)),
                                         columns=['new_index', 'corrects']).set_index('new_index',
                                                                                      drop=True).sort_index()
            del new_dataframe.index.name
            taken_items = new_dataframe.join(items)
            max_prob, theta_estimate = L(np.array(taken_items['correct']), np.array(taken_items['a']),
                                         np.array(taken_items['b']))

        self.assertEqual(theta_estimate, -0.84000000000006736)


class TestCTTMethods(unittest.TestCase):

    def test_CTT_methods(self):

        random.seed(123)
        np.random.seed(123)

        items = simulate_items()
        people = simulate_people(100, {'mean': 0, 'sd': 1})
        prob_vector, response_vector = item_vectors(items, people)

        alphas = calculate_alpha(response_vector)
        p_values = get_p_values(response_vector)
        discrim, discrim2 = discrimination_index(response_vector)
        examinee_scores = examinee_score(response_vector)
        self.assertEqual(alphas, 0.894933894194553)
        self.assertEqual(p_values.iloc[0, 0], 0.67)
        self.assertEqual(discrim[0], 0.44019800529488035)
        self.assertEqual(examinee_scores[0], 15)