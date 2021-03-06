import pandas as pd
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from statsmodels.stats.anova import anova_lm
from statsmodels.graphics.factorplots import interaction_plot
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

def angoff_rating(ratings):
    rater_average = ratings.mean(axis=1)
    return {'suggested_cut': rater_average.mean(), 'sem_rater_average': rater_average.sem()}

def contrasting_groups(examinees, score_column='total_score', group_column='qualification', groups=[0,1]):
    g1 = examinees[group_column] == 0
    g2 = examinees[group_column] == 1
    g1 = examinees[g1]
    g2 = examinees[g2]
    sns.distplot(g1[score_column], color="skyblue")
    sns.distplot(g2[score_column], color="red")
    return plt


def iit(ratings, raters_column='rater', item_column='item', group_column='group', rating_column='rating', minimally=False):
    iit_dict = {}
    if minimally==False:
        g1 = ratings[group_column] == 0
        g2 = ratings[group_column] == 1
        g1 = ratings[g1]
        g2 = ratings[g2]
        g1_rating = g1[rating_column].mean()
        g2_rating = g2[rating_column].mean()
        iit_dict['g1_rating'] = g1_rating
        sns.lineplot(x=item_column, y=rating_column, hue=group_column, palette='bright', data=ratings)
        plt.show()
    raters_list = ratings[raters_column].unique()

    for rater in raters_list:
        rater_df = ratings[raters_column] == rater
        rater_df = ratings[rater_df]
        rater_graph = sns.lineplot(x=item_column, y=rating_column, hue=group_column, palette='bright', data=rater_df)
        plt.show()

    formula = 'rating ~ C(group) + C(item) + C(group):C(item)'
    model = ols(formula, ratings).fit()
    aov_table = anova_lm(model, typ=2)
    return aov_table



df = pd.read_csv('/home/cfoster/Documents/iit.csv')
# contrasting_groups(df)
plt = iit(df)
print(plt)
# plt.show()