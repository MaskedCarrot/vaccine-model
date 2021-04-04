# Prediction and Analysis of State-Wise Distribution of Vaccine for Covid-19

Members: Apoorv Srivastava, Ritik Katiyar

## Project Design
<p>  </p>


#### System Entities and Components

We have defined the number of coronavirus cases in **India** as our system. Our system
will be composed of entities. These entities will be the number of active cases in the **states of
India**. The following components will control the entities of our system:

1. Active cases
2. Recovered cases
3. Deceased cases
4. daily vaccines administered.

#### Project Summary

Our project aims to create a model that will generate a suitable way of distributing the
covid19-vaccine among India’s states daily. The data generated by this model will be based
on the predictions made for the number of vaccines that will be made available in the coming
days and the number of coronavirus active, recovered and deceased cases that might be
reported in the following days.

#### Tools Technologies and data structures

To store the data that we collected, we will use pandas Data-Frame, which is
composed of NumPy arrays. We will predict data with the help of Python libraries like
sklearn. The data that will be generated from the forecast will be represented in the forms of
various graphs. These graphs will be built using libraries like matplotlib and Plotly.

## Project Implementation


The implementation of this will be a six-step process. The first step will involve the
collection of data from various data sources. Then we will clean and model the data to be
used further in the project. The final data set will be made up of two sets of data.

1. The first set will contain entity wise details of the components, i.e. state-wise details
    of active cases, recovered cases, deceased cases and the number of vaccines
    administered daily.
2. The second set will contain information about the number of vaccines administered
    throughout India.

Our next step will involve creating a polynomial regression model that will predict the
number of vaccines administered throughout India in the coming days using the second
data set mentioned above. Similarly, we will also indicate the number of covid cases recorded
in the coming days using the first data set.
Using the above data, we will generate a model that will find a suitable way of distributing
the vaccine among the states.
Our Next step will be to predict the number of corona cases throughout India if the vaccine is
distributed using the model we suggest. At this point, we have all the data that we require and
we can compare the number of covid-19 cases predicted using the current vaccine
distribution strategy and the one that our project suggests.

## References

1. Data on daily state-wise daily vaccination is collected from the GitHub pager of
    covid19India.
2. Data on daily coronavirus cases is collected from the Github page of covid19India

