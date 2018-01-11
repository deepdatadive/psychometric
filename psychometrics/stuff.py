import statsmodels.api as sm
import pandas as pd
from .CTT import examinee_score
from scipy import stats
stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)
chisqrprob = lambda chisq, df: stats.chi2.sf(chisq, df)

df = pd.read_csv('/home/cfoster/Documents/projects/psychometrics/data/ref_focus.csv')

def likelihood_ratio(llmin, llmax):
    return(-2*(llmax-llmin))

items = ["i1","i2","i3","i4","i5","i6","i7","i8","i9","i10","i11","i12","i13",
         "i14","i15","i16","i17","i18","i19","i20","i21","i22","i23","i24","i25","i26","i27","i28","i29","i30"]

df['total_score'] = examinee_score(df[items])
df['total_group_int'] = df['total_score'] * df['group']

vars_for_log_diff = ['total_score', 'group', 'total_group_int']

y = df['i1']
X = df[vars_for_log_diff]
logit_model = sm.Logit(y, X)
result = logit_model.fit()
print(result.summary())

LR = likelihood_ratio(-1335.5, -1381.3)


p = chisqrprob(LR, 1) # L2 has 1 DoF more than L1

print('p: %.30f' % p)

