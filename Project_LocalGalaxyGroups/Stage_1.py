import pandas as pd

dataset = pd.read_csv('G:/Mi unidad/UdeG_Doctorado_Clases/2022_Python_introduction/pyCharm_projects/Compact_groups_of_galaxies/groups.tsv',
                      delimiter='\t')
dataset.dropna(inplace=True)
with_features = dataset.loc[(dataset['features'] == 1),'mean_mu']
wo_features = dataset.loc[(dataset['features'] == 0),'mean_mu']

print("{} {}".format(
    round(with_features.mean(), 5),
    round(wo_features.mean(), 5)
))
