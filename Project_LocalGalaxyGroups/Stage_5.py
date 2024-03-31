import pandas as pd
from scipy import stats
import statistics
from scipy.stats import f_oneway
import matplotlib.pyplot as plt
import itertools

from astropy.cosmology import FlatLambdaCDM
from astropy import units as u
from astropy.coordinates import SkyCoord

dataset = pd.read_csv('G:/Mi unidad/UdeG_Doctorado_Clases/2022_Python_introduction/pyCharm_projects/Compact_groups_of_galaxies/groups.tsv',
                      delimiter='\t')
dataset.dropna(inplace=True)
wif = dataset.loc[(dataset['features'] == 1),'mean_mu']
wof = dataset.loc[(dataset['features'] == 0),'mean_mu']

dataset1 = pd.read_csv('G:/Mi unidad/UdeG_Doctorado_Clases/2022_Python_introduction/pyCharm_projects/Compact_groups_of_galaxies/galaxies_morphology.tsv',
                      delimiter='\t')
dataset2 = pd.read_csv('G:/Mi unidad/UdeG_Doctorado_Clases/2022_Python_introduction/pyCharm_projects/Compact_groups_of_galaxies/isolated_galaxies.tsv',
                      delimiter='\t')
dataset3 = pd.read_csv('G:/Mi unidad/UdeG_Doctorado_Clases/2022_Python_introduction/pyCharm_projects/Compact_groups_of_galaxies/galaxies_coordinates.tsv',
                      delimiter='\t')
dataset4 = pd.read_csv('G:/Mi unidad/UdeG_Doctorado_Clases/2022_Python_introduction/pyCharm_projects/Compact_groups_of_galaxies/groups.tsv',
                      delimiter='\t')


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
#print("{} {} {} {}".format(
#    round(sw_wif.pvalue, 5),
#    round(sw_wof.pvalue, 5),
#    round(flinger_test.pvalue, 5),
#    round(anova_test.pvalue, 5)
#))

#plt.hist(dataset1.loc[:,'n'])
#plt.show()
#plt.hist(dataset2.loc[:,'n'])
#plt.show()

gm_total = dataset1.loc[:,'n'].size
gm_less2 =  dataset1.loc[(dataset1['n'] > 2),'n'].size
ig_total = dataset2.loc[:,'n'].size
ig_less2 =  dataset2.loc[(dataset2['n'] > 2),'n'].size
ks_test = stats.ks_2samp(dataset1['n'], dataset2['n'], alternative='two-sided')

## Stage 3
#print("{} {} {}".format(
#    round(gm_less2 / gm_total, 5),
#    round(ig_less2 / ig_total, 5),
#    ks_test.pvalue
#))

gm_subtotales = dataset1.groupby('Group').agg({'n':['mean'],'T':['mean']})
gm_subtotales.columns = gm_subtotales.columns.droplevel(1)
gm_subtotales = gm_subtotales.reset_index()
gm_subtotales.rename({"n": "mean_n", "T": "mean_T"},
            axis='columns', inplace=True)

#print(dataset)
#print(gm_subtotales)
dataset = dataset.merge(gm_subtotales, on='Group')
#dataset4 = dataset4.merge(gm_subtotales, on='Group', how='left')
#print(dataset4)

#y_label = r"$\mu_{IGL,r}(mag{\sim}arcsec^{-2})$"
#plt.scatter(dataset['mean_mu'], dataset['mean_n'], color='r')
#plt.xlabel(r'$\langle n \rangle$')
#plt.ylabel(y_label)
#plt.show()
#plt.scatter(dataset['mean_mu'], dataset['mean_T'], color='r')
#plt.xlabel(r'$\langle T \rangle$')
#plt.ylabel(y_label)
#plt.show()

sw_mean_mu = stats.shapiro(dataset['mean_mu'])
sw_mean_n = stats.shapiro(dataset['mean_n'])
sw_mean_T = stats.shapiro(dataset['mean_T'])
pearson_mu_n = stats.pearsonr(dataset['mean_mu'], dataset['mean_n'])
pearson_mu_T = stats.pearsonr(dataset['mean_mu'], dataset['mean_T'])

## Stage 4
#print("{} {} {} {} {}".format(
#    sw_mean_mu.pvalue,
#    sw_mean_n.pvalue,
#    sw_mean_T.pvalue,
#    pearson_mu_n.pvalue,
#    pearson_mu_T.pvalue
#))

## Stage 5

my_cosmo = FlatLambdaCDM(H0=67.74, Om0=0.3089)

dataset3.sort_values(by=['Group'], inplace=True)
#print(dataset3)

groups = dataset3['Group'].unique()
groups_table = pd.DataFrame({'Group': groups})

for group in groups:
    #print("Group: {}".format(group))
    galaxies_in_group = dataset3.loc[dataset3['Group'] == group,:]
    distances = []
    for galaxy1, galaxy2 in itertools.combinations(zip(galaxies_in_group['RA'],galaxies_in_group['DEC']),2):
        (galaxy1_RA, galaxy1_DEC) = tuple(galaxy1)
        (galaxy2_RA, galaxy2_DEC) = tuple(galaxy2)
        galaxy1_skyCoord = SkyCoord(ra=galaxy1_RA * u.degree, dec=galaxy1_DEC * u.degree, frame="fk5")
        galaxy2_skyCoord = SkyCoord(ra=galaxy2_RA * u.degree, dec=galaxy2_DEC * u.degree, frame="fk5")
        #print(galaxy1_skyCoord.separation(galaxy2_skyCoord).to(u.rad))
        separation = galaxy1_skyCoord.separation(galaxy2_skyCoord).to(u.rad).value
        z = dataset4[dataset4['Group'] == group].z.item()
        angular_diamter_distance = my_cosmo.angular_diameter_distance(z).to(u.kpc)
        r = separation * angular_diamter_distance
        distances.append(r.value)
    #mean_distances = stats.describe(distances).mean
    median_S = statistics.median(distances)
    #print("Group: {} - distance {}".format(group, median_S))
    groups_table.loc[groups_table['Group'] == group, 'separation'] = median_S

dataset4 = dataset4.merge(groups_table, on='Group')
#print(dataset4)

plt.scatter(dataset4['mean_mu'], dataset4['separation'], color='r')
plt.gca().invert_yaxis()
plt.xlabel(r'$R_ (kpc)$')
plt.ylabel(r"$\mu_{IGL,r}(mag{\sim}arcsec^{-2})$")
plt.show()

dataset4.dropna(inplace=True)
sw_mean_mu = stats.shapiro(dataset4['mean_mu'])
sw_median_S = stats.shapiro(dataset4['separation'])
pearson_mu_S = stats.pearsonr(dataset4['mean_mu'], dataset4['separation'])

print("{} {} {} {}".format(
    groups_table[groups_table['Group'] == 'HCG 2'].separation.item(),
    sw_median_S.pvalue,
    sw_mean_mu.pvalue,
    pearson_mu_S.pvalue
))
