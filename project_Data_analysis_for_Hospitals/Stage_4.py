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

#print('Data shape: ' + str(combined.shape))
#print(combined.sample(n=20, random_state=30))

result_1 = combined.hospital.value_counts().idxmax()
print('The answer to the 1st question is ' + result_1)

general_diagnosis = combined[combined['hospital'] == 'general'].diagnosis.value_counts()
result_2 = str(round(general_diagnosis.loc[['stomach']].item() / general_diagnosis.sum(), 3))
print('The answer to the 2nd question is ' + result_2)

sports_diagnosis = combined[combined['hospital'] == 'sports'].diagnosis.value_counts()
result_3 = str(round(sports_diagnosis.loc[['dislocation']].item() / sports_diagnosis.sum(), 3))
print('The answer to the 3rd question is ' + result_3)

age_by_hospital = combined.groupby('hospital').agg({'age':'median'})
result_4 = str(int(age_by_hospital.loc['general','age'] - age_by_hospital.loc['sports','age']))
print('The answer to the 4th question is ' + result_4)

blood_by_hosp = combined.groupby('hospital').agg({'blood_test': 'value_counts'})
blood_by_hosp.rename(columns={'blood_test': 'blood_test_col'}, inplace=True)
#print(blood_by_hosp)
blood_by_hosp.reset_index(inplace=True)
#print(blood_by_hosp)
blood_by_hosp = blood_by_hosp[(blood_by_hosp["blood_test"] == 't')]
preresult_5 = blood_by_hosp.sort_values(by=['blood_test_col'], ascending=False)
result_5_1 = preresult_5.iloc[0,0]
result_5_2 = preresult_5.iloc[0,2]
print('The answer to the 5th question is ' + result_5_1 + ',', result_5_2,'blood tests')
