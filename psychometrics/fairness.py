import pandas as pd
from scipy.stats import chi2_contingency

#todo DIF approaches - , logistic regression, IRT



def mantel_hanzel_dif(items, response_column='response', refrence_column='group'):
    items = items['item'].unique().tolist()
    dict_list = []
    for item in items:
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

