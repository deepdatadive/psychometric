import pandas as pd
from psychometrics.CTT import examinee_score
from psychometrics.reliability import k_and_k, item_var_sum, total_var


#todo DOMC
#todo identify poorly performing items

def latency_analysis(data, item_id='item_id',latency='latency'):
    latencies = data.groupby(item_id)[latency].mean()
    return latencies

def option_analysis(data, distractor_correct='distractor_correct', total_score='total_score'):

    distractor_data = []
    for item in data['item_id'].unique():
        df_item = data[data['item_id'] == item]
        distractor_list = df_item['distractor_id'].unique()
        for distractor in distractor_list:
            new_data = {'item_id': item,
                        'distractor_id': distractor}
            df_distractor = df_item[df_item['distractor_id'] == distractor]
            correlation = df_distractor[distractor_correct].corr(df_distractor[total_score])
            new_data['correlation'] = correlation
            distractor_data.append(new_data)
    df_distractor_data = pd.DataFrame(distractor_data)
    return df_distractor_data

def get_p_values(data):
    '''
    returns p-values for every item in the dataframe

    :param data: a pandas dataframe where columns are items and rows are examinees.
    :return: a vector of p-values for each item in the assessment.
    '''
    p_values = pd.DataFrame(data.mean(axis=0))
    p_values.columns = ['P_Value']
    p_values['Item'] = p_values.index
    return p_values

def alpha_without_item(items):
    alpha_without_items = pd.Series(index=items.columns, name='Alpha Without Item')
    for item in items.columns:
        use_items = items.drop(item, axis=1)
        alpha_without_items.ix[item] = k_and_k(use_items) * (1 - (item_var_sum(use_items) / total_var(use_items)))
    return alpha_without_items

def discrimination_index(items):
    '''
    Calculates the point biserial and biserial for each item on the exam. Essentially these are item-total correlations where the item is not included in the total score (point-biserial) and is included int he total score (biserial).

    :param items: a pandas dataframe with columns for each item and rows for each examinee.
    :return: two dataframes. one containing the point-biserials and the other containing the biserials
    '''
    stat_without_item = pd.Series(index=items.columns, name='Point Biseral')
    for item in items.columns:
        total_deitemed = examinee_score(items) - items[item]
        stat_without_item.ix[item] = items[item].corr(total_deitemed)

    stat_with_item = pd.Series(index=items.columns, name='Biserial')
    for item in items.columns:
        total = examinee_score(items)
        stat_with_item.ix[item] = items[item].corr(total)
    return stat_without_item, stat_with_item

df = pd.read_csv('/home/cfoster/PycharmProjects/psychometric/data/distractor_analysis.csv')

returned = latency_analysis(df)
print(returned)