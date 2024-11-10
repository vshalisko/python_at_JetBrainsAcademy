import pandas as pd
from scipy import stats

## Implementation of Levene test and T-test for two samples

data = pd.read_csv("../aa_test.csv")
#print(data.columns.values)
sample_1 = data['Sample 1']
sample_2 = data['Sample 2']
sample_3 = [2,4,20,2,40]

#levene_res = stats.levene(sample_1, sample_2, sample_3)
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
