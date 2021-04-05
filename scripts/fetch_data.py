# import all modules here.
import pandas as pd
import os

# constants 
VACCINATION_CSV_URL = "http://api.covid19india.org/csv/latest/cowin_vaccine_data_statewise.csv"
CASES_CSV_URL = "https://api.covid19india.org/csv/latest/state_wise_daily.csv"

# downloads the csv and convert it into pandas dataframe
vaccine_df = pd.read_csv(VACCINATION_CSV_URL)
cases_df = pd.read_csv(CASES_CSV_URL)

# change directory to data
os.chdir('../data')


# clean vaccine data
vaccine_reduced_df = vaccine_df[['Updated On', 'State', "Total Doses Administered"]].copy()

vaccine_reduced_df.rename(columns={'Updated On': 'Date'}, inplace = True, errors='raise')

vaccine_reduced_df['Date'] = pd.to_datetime(vaccine_reduced_df['Date'])

vaccine_reduced_df.to_csv(r'vaccine-data-set.csv')

# clean cases data

cases_df['Date_YMD'] = pd.to_datetime(cases_df['Date_YMD'])

del cases_df['Date']

cases_df.rename(columns={'Date_YMD': 'Date'}, inplace = True, errors='raise')

cases_df = cases_df.melt(id_vars=['Date','Status'],var_name='state' , value_name='cases')

cases_reduced_df = cases_df.pivot_table('cases', ['Date' ,'state'],'Status')

cases_reduced_df.to_csv('daily-cases.csv')

os.chdir('../scripts')
