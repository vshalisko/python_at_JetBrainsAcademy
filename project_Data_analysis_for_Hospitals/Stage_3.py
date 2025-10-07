import pandas as pd

pd.set_option('display.max_columns', 8)

general = pd.read_csv('test/general.csv')
prenatal = pd.read_csv('test/prenatal.csv')
sports = pd.read_csv('test/sports.csv')

# print(general.head(20))
# print(prenatal.head(20))
# print(sports.head(20))
# print(general.columns)
# print(prenatal.columns)
# print(sports.columns)

# print(list(general))
renamer1 = dict(map(lambda i,j : (i,j) , list(prenatal),list(general)))
renamer2 = dict(map(lambda i,j : (i,j) , list(sports),list(general)))

prenatal.rename(columns=renamer1, inplace=True)
sports.rename(columns=renamer2, inplace=True)

prenatal[['gender']] = prenatal[['gender']].fillna('f')

# prenatal = pd.DataFrame(prenatal, columns=list(general))
# sports = pd.DataFrame(sports, columns=list(general))

# print(general.sample(n=20, random_state=30))
# print(prenatal.sample(n=20, random_state=30))
# print(sports.sample(n=20, random_state=30))

combined = pd.concat([general, prenatal, sports],
                         ignore_index=True)
combined = combined.drop(columns='Unnamed: 0')
combined[['bmi','diagnosis','blood_test','ecg','ultrasound',
          'mri','xray','children','months']] = \
    combined[['bmi','diagnosis','blood_test','ecg','ultrasound',
              'mri','xray','children','months']].fillna(0)
combined.replace({'gender':{'female':'f','male':'m','woman':'f','man':'m'}},inplace=True)
combined.dropna(inplace=True)
# print(combined)
# combined.sample(n=20, random_state=30)

print('Data shape: ' + str(combined.shape))
print(combined.sample(n=20, random_state=30))
