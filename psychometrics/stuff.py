from psy import Irt, data
from psychometrics.simulation import simulate_items, simulate_people, item_vectors


score = data['lsat.dat']
#print(score.shape)
model = Irt(scores=score, link='probit')
res = model.fit()
#print(res)

items = simulate_items()
people = simulate_people(1000, {'mean': 0, 'sd': 1})
prob_vector, response_vector = item_vectors(items, people)
resp = response_vector.values
#print(resp)

model = Irt(scores=resp, link='logit', params_type='1PL')
res = model.fit()
print(res)
#print(items)

model = Irt(scores=resp, link='logit', params_type='2PL')
res = model.fit()
print(res)
