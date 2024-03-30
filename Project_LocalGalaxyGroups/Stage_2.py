import pandas as pd
from scipy import stats
from scipy.stats import f_oneway

## The ANOVA test has conditions that must be fulfilled so
## that the associated p -value can be valid:
## 1) The samples must be independent;
## 2) Each sample is derived from a normally distributed population;
## 3) The variances of the groups are equal (the homogeneity of variances).
## The independence of samples is guaranteed in our data,
## so we need to check only the last two conditions
## to perform the ANOVA test after.
## Conduct the Shapiro-Wilk Normality test for the IGL 
## mean surface brightness (the mean_mu column) in galaxies with LSB 
## features and without them. This step checks the second condition of the ANOVA 
## test: each sample came from a normally distributed population. 
## Is the condition satisfied?
## Perform the Fligner-Killeen Homogeneity test for 
## variances of the same two data samples. This step checks the 
## third condition: the samples came from populations with 
## equal variances. Is the condition satisfied?
## Perform the one-way ANOVA test and obtain a p-value. 
## The test's null hypothesis is that both groups (galaxies with 
## LSB features and without them) are drawn from the populations 
## with the same IGL mean surface brightness. Do LSB features 
## significantly influence the IGL mean surface brightness 
## according to the test?
## Print four floating-point numbers. Separate them with 
## one space: two p-values for the Shapiro-Wilk test 
## for galaxies with LSB features and without them, one p-value 
## obtained from the Fligner-Killeen test, and one p-value 
## of the ANOVA test.


dataset = pd.read_csv('G:/Mi unidad/UdeG_Doctorado_Clases/2022_Python_introduction/pyCharm_projects/Compact_groups_of_galaxies/groups.tsv',
                      delimiter='\t')
dataset.dropna(inplace=True)
wif = dataset.loc[(dataset['features'] == 1),'mean_mu']
wof = dataset.loc[(dataset['features'] == 0),'mean_mu']

## Stage 1
#print("{} {}".format(
#    round(wif.mean(), 5),
#    round(wof.mean(), 5)
#))

sw_wif = stats.shapiro(wif)
sw_wof = stats.shapiro(wof)
flinger_test = stats.fligner(wif, wof)
anova_test = f_oneway(wif, wof)

## Stage 2
print("{} {} {} {}".format(
    round(sw_wif.pvalue, 5),
    round(sw_wof.pvalue, 5),
    round(flinger_test.pvalue, 5),
    round(anova_test.pvalue, 5)
))
