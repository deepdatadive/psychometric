.. psychometrics documentation master file, created by
   sphinx-quickstart on Thu Jan 11 15:36:34 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

psychometrics
=========================================

Psychometrics is a python package designed to help users implement both Classical Test Theory and Item Response Theory models and applications within a python framework.

Motivation
----------

There were very few python packages built in python and I felt it was important to have some packages built as psychometricians begin utilizing python more frequently.

Installation
------------

This package can be installed via pip::

    pip install git+https://github.com/deepdatadive/psychometric.git


CTT example
----------------

Lets examine how we could analyze a test using classical test theory. First lets generate some data using the simulation module::


    from psychometric.simulation import simulate_items, simulate_people, response_vector
    items = simulate_items()
    people = simulate_people(100, {'mean': 0, 'sd': 1})
    prob_vector, response_vector = item_vectors(items, people)

We now have a pandas dataframe name response_vector that contains correct (1) and incorrect(0) responses for 100 people and 50 items. We can apply specific CTT functions directly to this dataframe.::

    from psychometrics.CTT import calculate_alpha, discrimination_index, get_p_values, examinee_score
    # Calculate coefficient alpha
    alphas = calculate_alpha(response_vector)
    # Calculate p-values for each item
    p_values = get_p_values(response_vector)
    # Calculate biserial and point biseral values for each item
    discrim, discrim2 = discrimination_index(response_vector)
    # Calculate raw scores for each examinee
    examinee_scores = examinee_score(response_vector)

API
===

.. automodule:: psychometrics.CTT
    :members:

.. automodule:: psychometrics.simulation
    :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
