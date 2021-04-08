# import all modules here.
import pandas as pd
import os

os.chdir('../data')

# downloads the csv and convert it into pandas dataframe
state_details_df = pd.read_csv("state-details.csv")
vaccine_data_set_df = pd.read_csv("vaccine-data-set.csv")
daily_cases_df = pd.read_csv("daily-cases.csv")

#to remove unnamed columns
state_details_df = state_details_df.loc[:, ~state_details_df.columns.str.contains('^Unnamed')]

#In state-details.csv, TT is named as "Total", but in vaccine-data.csv, there is "india" istead of "Total"
using_index = state_details_df.iloc[38,0]="India"
#print(state_details_df)


#for merging, renamed column, state to abbreviation
daily_cases_df_new = daily_cases_df.rename(columns={"state": "abbreviation"})

#to remove unnamed columns
daily_cases_df_new = daily_cases_df_new.loc[:, ~daily_cases_df_new.columns.str.contains('^Unnamed')]
#print(daily_cases_df_new)


merge1_df = pd.merge(daily_cases_df_new, state_details_df,
                   on='abbreviation',
                   how='left')


#to remove unnamed column
merge1_df = merge1_df.loc[:, ~merge1_df.columns.str.contains('^Unnamed')]


combined_df = pd.merge(merge1_df, vaccine_data_set_df,
                   on=['State', 'Date'],
                   how='inner')


#to remove unnamed columns
combined_df = combined_df.loc[:, ~combined_df.columns.str.contains('^Unnamed')]
pd.set_option('display.max_columns', None)

combined_df.to_csv('combined_data.csv')

os.chdir('../scripts')
