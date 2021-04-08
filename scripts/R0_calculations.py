import pandas as pd
import numpy as np
from scipy import stats as sps
from scipy.interpolate import interp1d

from IPython.display import clear_output

FILTERED_REGIONS = []

FILTERED_REGION_CODES = []



dfi = pd.read_csv("combined_data.csv")
# Data preprocessing
# Exclude states with 2 or less datapoints with 10 or less cases


new_dfi = dfi.drop(['Unnamed: 0', 'Deceased', 'Recovered', 'State', 'population', 'Total Doses Administered'], axis=1)
#print(new_dfi)

df = new_dfi.sort_values(by=['abbreviation', 'Date'])
#print(df)
states = df.set_index(['abbreviation', 'Date']).squeeze()
#print(states)

'''
def prepare_cases(cases, cutoff=25):
    new_cases = cases.diff()

    smoothed = new_cases.rolling(7,
                                 win_type='gaussian',
                                 min_periods=1,
                                 center=True).mean(std=2).round()

    idx_start = np.searchsorted(smoothed, cutoff)

    smoothed = smoothed.iloc[idx_start:]
    original = new_cases.loc[smoothed.index]

    return original, smoothed
'''
    



def get_posteriors(sr, sigma=0.15):

    # (1) Calculate Lambda
    
    #https://bmcinfectdis.biomedcentral.com/articles/10.1186/s12879-021-05950-x
    GAMMA = 1/5.8

    R_T_MAX = 12
    r_t_range = np.linspace(0, R_T_MAX, R_T_MAX*100+1)

    lam = sr[:-1].values * np.exp(GAMMA * (r_t_range[:, None] - 1))

    # (2) Calculate each day's likelihood
    likelihoods = pd.DataFrame(
        data=sps.poisson.pmf(sr[1:].values, lam),
        index=r_t_range,
        columns=sr.index[1:])

    # (3) Create the Gaussian Matrix
    process_matrix = sps.norm(loc=r_t_range,
                              scale=sigma
                              ).pdf(r_t_range[:, None])

    # (3a) Normalize all rows to sum to 1
    process_matrix /= process_matrix.sum(axis=0)

    # (4) Calculate the initial prior
    # prior0 = sps.gamma(a=4).pdf(r_t_range)
    prior0 = np.ones_like(r_t_range) / len(r_t_range)
    prior0 /= prior0.sum()

    # Create a DataFrame that will hold our posteriors for each day
    # Insert our prior as the first posterior.
    posteriors = pd.DataFrame(
        index=r_t_range,
        columns=sr.index,
        data={sr.index[0]: prior0}
    )

    # We said we'd keep track of the sum of the log of the probability
    # of the data for maximum likelihood calculation.
    log_likelihood = 0.0

    # (5) Iteratively apply Bayes' rule
    for previous_day, current_day in zip(sr.index[:-1], sr.index[1:]):
        # (5a) Calculate the new prior
        current_prior = process_matrix @ posteriors[previous_day]

        # (5b) Calculate the numerator of Bayes' Rule: P(k|R_t)P(R_t)
        numerator = likelihoods[current_day] * current_prior

        # (5c) Calcluate the denominator of Bayes' Rule P(k)
        denominator = np.sum(numerator)

        # Execute full Bayes' Rule
        posteriors[current_day] = numerator / denominator

        # Add to the running sum of log likelihoods
        log_likelihood += np.log(denominator)

    return posteriors, log_likelihood

    
    
sigmas = np.linspace(1/20, 1, 20)
#targets = ~states.index.get_level_values('abbreviation').isin(FILTERED_REGION_CODES)
#states_to_process = states.loc[targets]

results = {}
failed_states = []

for state_name, cases in states_to_process.groupby(level='state'):
    
    print(state_name)
    print(Confirmed)
    #new, smoothed = prepare_cases(cases)
    
    result = {}
    
    # Holds all posteriors with every given value of sigma
    result['posteriors'] = []
    
    # Holds the log likelihood across all k for each value of sigma
    result['log_likelihoods'] = []
    
    try:
      for sigma in sigmas:
        posteriors, log_likelihood = get_posteriors(smoothed, sigma=sigma)
        result['posteriors'].append(posteriors)
        result['log_likelihoods'].append(log_likelihood)
    
    # Store all results keyed off of state name
      results[state_name] = result
      clear_output(wait=True)
    except:
      print(f"Error for state {state_name}")
      failed_states.append(state_name)

print('Done.')
print(f"Failed for {len(failed_states)} states {failed_states}")
# Each index of this array holds the total of the log likelihoods for
# the corresponding index of the sigmas array.
total_log_likelihoods = np.zeros_like(sigmas)

# Loop through each state's results and add the log likelihoods to the running total.
for state_name, result in results.items():
    total_log_likelihoods += result['log_likelihoods']

# Select the index with the largest log likelihood total
max_likelihood_index = total_log_likelihoods.argmax()

# Select the value that has the highest log likelihood
sigma = sigmas[max_likelihood_index]


final_results = None
hdi_error_list = []

for state_name, result in results.items():
    print(state_name)
    try:
        posteriors = result['posteriors'][max_likelihood_index]
        most_likely = posteriors.idxmax().rename('ML')
        result = pd.concat([most_likely], axis=1)
        if final_results is None:
            final_results = result
        else:
            final_results = pd.concat([final_results, result])
        clear_output(wait=True)
    except:
        print(f'hdi failed for {state_name}')
        hdi_error_list.append(state_name)
        pass

print(f'HDI error list: {hdi_error_list}')
print('Done.')
#final_results.to_csv('data/rt_india_state.csv')

