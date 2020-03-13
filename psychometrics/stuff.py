from psy import Irt, data

score = data['lsat.dat']
model = Irt(scores=score, link='probit')
res = model.fit()
print(res)
