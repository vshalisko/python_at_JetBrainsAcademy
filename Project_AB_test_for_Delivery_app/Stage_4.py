import math
import datetime
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats import power
import matplotlib.pyplot as plt

def roundup(x):
    return int(math.ceil(x / 100.0)) * 100
stage = 4

if stage == 1:
    ## Levene test and t-test
    data = pd.read_csv("../aa_test.csv")
    #print(data.columns.values)
    sample_1 = data['Sample 1']
    sample_2 = data['Sample 2']

    levene_res = stats.levene(sample_1, sample_2)

    if levene_res[1]>0.05:
        levene_p = ">"
        levene_reject = "no"
        levene_equal = "yes"
        ttest_equal_var = True
    else:
        levene_p = "<="
        levene_reject = "yes"
        levene_equal = "no"
        ttest_equal_var = False

    print("Levene's test")
    print("W = {0:5.3f}, p-value {1} 0.05".format(
        round(levene_res[0],3),levene_p))
    print("Reject null hypothesis: {}".format(levene_reject))
    print("Variances are equal: {}".format(levene_equal))

    ttest_res = stats.ttest_ind(sample_1, sample_2, equal_var=ttest_equal_var)

    if ttest_res[1]>0.05:
        ttest_p = ">"
        ttest_reject = "no"
        ttest_equal = "yes"
    else:
        ttest_p = "<="
        ttest_reject = "yes"
        ttest_equal = "no"

    print("\nT-test")
    print("t = {0:5.3f}, p-value {1} 0.05".format(
        round(ttest_res[0],3),ttest_p))
    print("Reject null hypothesis: {}".format(ttest_reject))
    print("Means are equal: {}".format(ttest_equal))

elif stage == 2:
    ## Power analysis to determine the required sample size
    data = pd.read_csv("../ab_test.csv")
    #print(data.columns.values)
    counts = data.groupby(['group'])['group'].count()

    power_setting = 0.8
    effect = 0.2
    significance = 0.05
    power_res = power.tt_ind_solve_power(
        effect_size = effect,
        nobs1 = None,
        alpha = significance,
        power = power_setting,
        ratio = 1,
        alternative = 'two-sided'
    )
    print("Sample size: {}\n".format(roundup(power_res)))

    print("Control group: {}".format(counts.loc['Control']))
    print("Experimental group: {}".format(counts.loc['Experimental']))

elif stage == 3:
    ## Exploratory data analysis
    data = pd.read_csv("../ab_test.csv")
    #print(data.columns.values)


    ## barplot
    data.groupby('date').group.value_counts().unstack().plot.bar()
    locs, labels = plt.xticks()
    dates = [text.get_text() for text in labels]
    dates = [datetime.datetime.strptime(predate, '%Y-%m-%d').strftime('%d') for predate in dates]
    #print(dates)
    plt.xticks(locs, dates)
    plt.legend(loc='upper center')
    plt.xlabel('June')
    plt.ylabel('Number of sessions')
    plt.show()

    ## histograms
    data_control = data.loc[data['group'] == "Control",:]
    data_experimental = data.loc[data['group'] == "Experimental", :]

    fig, axs = plt.subplots(1,2)
    axs[0].hist(data_control.order_value)
    axs[1].hist(data_experimental.order_value)
    axs[0].set_title('Control')
    axs[1].set_title('Experimental')
    fig.supxlabel('Order value')
    fig.supylabel('Frequency')
    plt.show()

    fig, axs = plt.subplots(1,2)
    axs[0].hist(data_control.session_duration)
    axs[1].hist(data_experimental.session_duration)
    axs[0].set_title('Control')
    axs[1].set_title('Experimental')
    fig.supxlabel('Session duration')
    fig.supylabel('Frequency')
    plt.show()

    ## Outliers removal
    order_value_p99 = np.percentile(data['order_value'],[99])
    session_duration_p99 = np.percentile(data['session_duration'], [99])
    data_filtered = data.loc[data['order_value'] <= order_value_p99[0],:]
    data_filtered = data_filtered.loc[data_filtered['session_duration'] <= session_duration_p99[0], :]

    print("Mean: {}".format(round(np.mean(data_filtered['order_value']), 2)))
    print("Standard deviation: {}".format(round(np.std(data_filtered['order_value']), 2)))
    print("Max: {}".format(round(np.max(data_filtered['order_value']), 2)))
    
elif stage == 4:
    ## Levene test and t-test
    data = pd.read_csv("../ab_test.csv")

    ## Outliers removal
    order_value_p99 = np.percentile(data['order_value'],[99])
    session_duration_p99 = np.percentile(data['session_duration'], [99])
    data_filtered = data.loc[data['order_value'] <= order_value_p99[0],:]
    data_filtered = data_filtered.loc[data_filtered['session_duration'] <= session_duration_p99[0], :]

    sample_1 = data_filtered.loc[data_filtered['group'] == "Control","order_value"]
    sample_2 = data_filtered.loc[data_filtered['group'] == "Experimental","order_value"]


    test_res = stats.mannwhitneyu(sample_1, sample_2)

    if test_res[1]>0.05:
        test_p = ">"
        test_reject = "no"
        test_equal = "yes"
    else:
        test_p = "<="
        test_reject = "yes"
        test_equal = "no"

    print("\nMann-Whitney U test")
    print("U1 = {0:5.3f}, p-value {1} 0.05".format(
        round(test_res[0],3),test_p))
    print("Reject null hypothesis: {}".format(test_reject))
    print("Distributions are same: {}".format(test_equal))
