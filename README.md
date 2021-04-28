# Covid-19 Vaccine Analysis

[![Test python scripts](https://github.com/MaskedCarrot/vaccine-model/actions/workflows/test_scripts.yml/badge.svg)](https://github.com/MaskedCarrot/vaccine-model/actions/workflows/test_scripts.yml)

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0f424492fa4e45c6ba5a2042c840c823)](https://www.codacy.com/gh/MaskedCarrot/vaccine-model/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=MaskedCarrot/vaccine-model&amp;utm_campaign=Badge_Grade)

Members: Apoorv Srivastava, Ritik Katiyar


## Project Design

### System Entities and Components
We have defined the vaccine analysis model as our system. Our system will be further divided into two subsystems, impact of Vaccines throughout the World and Vaccine sentiment analysis in India. These two subsystems are capable of existing individually, but together they help in weaving a concrete analysis.
 Impact of Vaccines throughout the World:
This subsystem helps us to mathematically study and analyze the impact of Covid-19 vaccines on the entire globe.
Entities: Vaccine Administered, New Cases, Deceased Cases and Recovered Cases.
Vaccine sentiment analysis in India:
 This subsystem analyzes the overall social perception of covid-19 vaccination in India, through twitter.
Entities:  Positive tweets, Negative tweets and Social Events

## Project Summary
Our project is divided into two parts, the  ‘Impact of Vaccines throughout the World’ subsystem will give the statistical analysis of Covid-19. It will analyze and quantify the effectiveness of covid vaccines. This will be done by studying the relationship between covid-19 growth rate and total vaccine administered, globally and then by taking county specific examples, to clearly prove our results. Furthermore, we will critique on India, and how even though vaccination has  increased, the growth rate has not gone down as it should have. 
The ‘Vaccine sentiment analysis in India’ will study the change in the sentiments of the tweets about the vaccine for the general public. It will create a graph which represents the date wise positive and negative sentiments of the tweets which includes the words ‘covacine’ or ‘covishelid’.

### Tools  Technologies and data structures
To store the data that we collected, we will use Pandas Data-Frame, which is composed of NumPy arrays. The data that will be generated from the forecast will be represented in the forms of various graphs. These graphs will be built using libraries like matplotlib and Plotly.  We will also use NLTK for symbolic and statistical natural language processing in the english language. We have also used tweepy to authenticate and then download the tweets.

## Project Implementation
 The first step will involve the collection of data from various data sources. Data has been collected from Covid-19 GitHub repository provided by Johns Hopkins University. Also data has been collected from twitter API with the help of a python script. Then the data is pre-processed using a python script. Finally, we will clean and model the data to be used further in this project. The final data set will be made up of 3 sets of data. 
The first set will contain coronavirus daily data, which includes date, total cases, daily new cases, activ cases, cumulative total deaths, and daily new deaths for every county.
The second set will contain country vaccinations, which includes date, and total vaccinations for every county.
The final dataset, vaccine tweets, will contain all the tweets containing the words ‘covacine’ or ‘covishelid’, in India.
Our next step will involve creating graphs using the first two datasets to project our analysis, with the help of libraries like matplotlib and Plotly. It will depict how the increase in vaccinations has reduced the growth rate of covid-19 globally and in some specific counties.

Our Final step will be to implement sentiment analysis on the 3rd dataset, which will be done by the  NLTK suite called SentimentIntensityAnalyzer. To analyse the sentiments we have used the function plot_polarity of the sentiment analyzer. To graph the results of this part of the project we have used the python libraries plotly and matplotlib. 

## References
Data on  coronavirus daily data  and  country vaccinations are collected from the GitHub pager of Johns Hopkins University.
https://github.com/CSSEGISandData/COVID-19 
