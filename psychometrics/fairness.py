import pandas as pd
from scipy.stats import chi2_contingency
import pandas as pd
import pylab as pl
import numpy as np
import statsmodels.api as sm

#todo DIF approaches - IRT

def mantel_hanzel_dif(items, response_column='response', refrence_column='group'):
    item_list = items['item'].unique().tolist()
    dict_list = []
    for item in item_list:
        df_item = items[items['item']==item]
        crosstab = pd.crosstab(df_item[response_column], df_item[refrence_column])
        chi2, p, dof, ex = chi2_contingency(crosstab)

        crosstab_dict = {
            'item':item,
            'chi2':chi2,
            'p_value':p,
            'dof': dof
        }
        dict_list.append(crosstab_dict)

    chi2_df = pd.DataFrame(dict_list)
    return chi2_df

def logistic_regression_dif(items, response_column='response', refrence_column='group'):
    items_list = items['item'].unique().tolist()
    dict_list = []
    for item in items_list:
        df_item = items[items['item']==item]
        logit = sm.Logit(df_item[response_column], df_item[refrence_column])
        result = logit.fit()

        stats_dict = {
            'item':item,
            'coef':result.params[0],
            'p_value':result.pvalues[0],
            'prquared': result.prsquared
        }
        dict_list.append(stats_dict)

    logit_df = pd.DataFrame(dict_list)
    return logit_df

df = pd.read_csv('/home/cfoster/Documents/dif_CTT.csv')
result = logistic_regression_dif(df)
print(result)