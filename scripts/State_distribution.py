import pandas as pd
import numpy as np
import os

os.chdir('../data')


FILTERED_REGION_CODES = []



final_results = pd.read_csv("R0_calculations.csv")
state_details = pd.read_csv("state-details2.csv")
recov_df = pd.read_csv("daily-cases.csv")
dec_df = pd.read_csv("daily-cases.csv")
vac_df = pd.read_csv("vaccine-data-set.csv")


new = state_details.drop(["state_name"], axis=1)
#print(new.columns)
merge1_df = pd.merge(final_results, state_details,
                   on='state',
                   how='left')

#print(merge1_df)


new_recov_df = recov_df.drop(['Confirmed', 'Deceased'], axis=1)
new_recov_df2 = new_recov_df.rename(columns={"Date": "date"})
new_recov_df3 = new_recov_df2.sort_values(by=['state', 'date'])
#print(new_recov_df3)
new_recov_df3['total Recovered'] = new_recov_df3.groupby('state').cumsum()
#print(new_recov_df3)
final_recov = new_recov_df3.drop(['Recovered'], axis=1)
final_recov.reset_index(drop=True, inplace=True)


#print(dec_df.columns)
new_dec_df = dec_df.drop(['Confirmed', 'Recovered'], axis=1)
new_dec_df2 = new_dec_df.rename(columns={"Date": "date"})
new_dec_df3 = new_dec_df2.sort_values(by=['state', 'date'])
#print(new_dec_df3)
new_dec_df3['total Deceased'] = new_dec_df3.groupby('state').cumsum()
#print(new_dec_df3)
final_dec = new_dec_df3.drop(['Deceased'], axis=1)
final_dec.reset_index(drop=True, inplace=True)


#print(vac_df.columns)
new_vac_df = vac_df.rename(columns={"Date": "date"})
new_vac_df2 = new_vac_df.rename(columns={'State' : 'state_name'}) 
final_vac = new_vac_df2.drop(['Unnamed: 0'], axis=1)
final_vac.reset_index(drop=True, inplace=True)



merge2_df = pd.merge(merge1_df, final_recov,
                   on=['state', 'date'],
                   how='left')

#print(merge2_df)

merge3_df = pd.merge(merge2_df, final_dec,
                   on=['state', 'date'],
                   how='left')

#print(merge3_df)

merge4_df = pd.merge(merge3_df, final_vac,
                   on=['state_name', 'date'],
                   how='left')

removeNan = merge4_df.fillna(method='ffill')
final_df_orignal = removeNan.fillna(2000)


final_df_orignal['Susceptible'] = final_df_orignal['population'] - final_df_orignal['total Recovered'] - final_df_orignal['total Deceased'] - final_df_orignal['Total Doses Administered']
final_df_orignal['R0*Susceptible'] = final_df_orignal['ML'] * final_df_orignal['Susceptible']
final_df_orignal.to_csv('Final_data.csv')


state_distribution = final_df_orignal.drop(['ML', 'state_name', 'population', 'total Recovered', 'total Deceased', 'Total Doses Administered', 'Susceptible' ], axis=1)
#print(state_distribution.columns)
state_distribution2 = state_distribution.sort_values(by=['date', 'state'])
#print(state_distribution3)
grouped_df = state_distribution2.groupby(['date', 'state']).agg({'R0*Susceptible': 'sum'})
percents_df = grouped_df.groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))

percents_df.to_csv('State_wise_distribution.csv')

os.chdir('../scripts')