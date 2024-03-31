import pandas as pd
from scipy import stats
import statistics
import matplotlib.pyplot as plt
import itertools

from astropy.cosmology import FlatLambdaCDM
from astropy import units as u
from astropy.coordinates import SkyCoord

dataset = pd.read_csv('G:/Mi unidad/UdeG_Doctorado_Clases/2022_Python_introduction/pyCharm_projects/Compact_groups_of_galaxies/groups.tsv',
                      delimiter='\t')
dataset3 = pd.read_csv('G:/Mi unidad/UdeG_Doctorado_Clases/2022_Python_introduction/pyCharm_projects/Compact_groups_of_galaxies/galaxies_coordinates.tsv',
                      delimiter='\t')

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
        z = dataset[dataset['Group'] == group].z.item()
        angular_diamter_distance = my_cosmo.angular_diameter_distance(z).to(u.kpc)
        r = separation * angular_diamter_distance
        distances.append(r.value)
    median_S = statistics.median(distances)
    #print("Group: {} - distance {}".format(group, median_S))
    groups_table.loc[groups_table['Group'] == group, 'separation'] = median_S

dataset = dataset.merge(groups_table, on='Group')
#print(dataset4)

plt.scatter(dataset['mean_mu'], dataset['separation'], color='r')
plt.gca().invert_yaxis()
plt.xlabel(r'$R_ (kpc)$')
plt.ylabel(r"$\mu_{IGL,r}(mag{\sim}arcsec^{-2})$")
plt.show()

dataset.dropna(inplace=True)
sw_mean_mu = stats.shapiro(dataset['mean_mu'])
sw_median_S = stats.shapiro(dataset['separation'])
pearson_mu_S = stats.pearsonr(dataset['mean_mu'], dataset['separation'])

print("{} {} {} {}".format(
    groups_table[groups_table['Group'] == 'HCG 2'].separation.item(),
    sw_median_S.pvalue,
    sw_mean_mu.pvalue,
    pearson_mu_S.pvalue
))
