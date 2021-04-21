# imports
import math
import numpy as np
import pandas as pd
import plotly.express as ex
import plotly.graph_objects as go
import plotly.offline as pyo
from datetime import datetime


# load data
vacc_df = pd.read_csv("../data/country_vaccinations.csv")
daily_df = pd.read_csv("../data/coronavirus_daily_data.csv")


# Implement the above
vacc_df.country = vacc_df.country.replace().replace({
    "Czechia": "Czech Republic",
    "United States": "USA",
    "United Kingdom": "UK",
    "Isle of Man": "Isle Of Man",
    "Republic of Ireland": "Ireland",
    "Northern Cyprus": "Cyprus"
})

# drop these 3 since they are included in UK
vacc_df = vacc_df[vacc_df.country.apply(
    lambda x: x not in ['England', 'Scotland', 'Wales', 'Northern Ireland'])]

vaccines = vacc_df[['country', 'vaccines']].drop_duplicates()


# helper functions
def get_multi_line_title(title: str, subtitle: str):
    return f"{title}<br><sub>{subtitle}</sub>"


def visualize_column(data: pd.DataFrame, xcolumn: str, ycolumn: str, title: str, colors: str, ylabel="Count", n=None):
    hovertemplate = '<br><b>%{x}</b>' + \
        f'<br><b>{ylabel}: </b>'+'%{y}<br><extra></extra>'
    data = data.sort_values(ycolumn, ascending=False).dropna(subset=[ycolumn])

    if n is not None:
        data = data.iloc[:n]
    else:
        n = ""
    fig = go.Figure(go.Bar(
                    hoverinfo='skip',
                    x=data[xcolumn],
                    y=data[ycolumn],
                    hovertemplate=hovertemplate,
                    marker=dict(
                        color=data[ycolumn],
                        colorscale=colors,
                    ),
                    ),
                    )

    fig.update_layout(
        title=title,
        xaxis_title=f"Top {n} {xcolumn.title()}",
        yaxis_title=ylabel,
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode="x"
    )

    fig.show()


def calculate_growth_rate(data_list):
    growth_rate_list = []
    for i in range(1, len(data_list)):
        growth_rate_list.append(
            (data_list[i]-data_list[i-1])/data_list[i-1]*100)
    return growth_rate_list


# unique dates
dates = vacc_df.date.unique().tolist()
dates.extend(['2020-12-12', '2020-12-13'])  # add 2 dates to improve animation

# unique countries
countries = vacc_df.country.unique().tolist()

# for easy processing
short = vacc_df[['date', 'country', 'total_vaccinations']]

# values of unqiue (date, country) already in short
# i.e we want to make sure we have some data for each, even if it is 0
keys = list(zip(short.date.tolist(), short.country.tolist()))
for date in dates:
    for country in countries:
        idx = (date, country)
        if idx not in keys:
            if date == min(dates):
                # this means there's no entry for {country} on the earliest date
                short = short.append({
                    "date": date,
                    "country": country,
                    "total_vaccinations": 0
                }, ignore_index=True)
            else:
                # entry for {country} is missing on a date other than the earliest
                short = short.append({
                    "date": date,
                    "country": country,
                    "total_vaccinations": pd.NA
                }, ignore_index=True)

# fill missing values with previous day values (this is OK since it is cumulative)
short = short.sort_values(['country', 'date'])

short.total_vaccinations = short.total_vaccinations.fillna(method='ffill')

# scale the number by log to make the color transitions smoother
vaccines = short.sort_values('date')
vaccines['log_scale'] = vaccines['total_vaccinations'].apply(
    lambda x: math.log2(x+1))

fig = ex.choropleth(vaccines, locations="country",
                    locationmode='country names',
                    color="log_scale",
                    hover_name="country",
                    hover_data=['log_scale', "total_vaccinations"],
                    animation_frame="date",
                    color_continuous_scale="BuGn",
                    )

title = get_multi_line_title(
    "Vaccination Progress", "Number of Vaccines Administered Around the World")
fig.update_layout(coloraxis={"cmax": 25, "cmin": 0})
fig.update_layout(title=title, title_x=0.5, coloraxis_showscale=False)

fig.show()


# copy the datasets
vaccs = vacc_df.copy()
daily = daily_df.copy()

# standardise the dates
vaccs.date = vaccs.date.apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
daily.date = daily.date.apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))

# use only common countries and dates
countries = vaccs.dropna(subset=['daily_vaccinations'])['country'].unique()
dates = vaccs.dropna(subset=['daily_vaccinations'])['date'].unique()
country_mask = daily.country.apply(lambda x: x in countries)
date_mask = daily.date.apply(lambda x: x in dates)

# generate the visualization data
columns_to_sum = ['daily_new_cases', 'cumulative_total_cases',
                  'cumulative_total_deaths', 'active_cases']
daily_cases = daily[country_mask & date_mask].groupby('date')[
    columns_to_sum].sum()
daily_vaccs = vaccs.groupby('date')[['daily_vaccinations']].sum()

# make it a dataframe for convenience
data = pd.DataFrame(daily_cases).join(pd.DataFrame(daily_vaccs))

# bring back the vaccine data we prepared in the previous section
cumulative_vaccines = pd.DataFrame(
    vaccines.groupby('date')['total_vaccinations'].sum())
data = data.join(cumulative_vaccines).reset_index()

title = get_multi_line_title(
    "Vaccine vs Virus", "Comparing the total number of daily new cases and daily vaccinations globally")
fig = go.Figure(data=[
                go.Bar(
                    name="New Cases",
                    x=data['date'],
                    y=data['daily_new_cases'],
                    marker_color="crimson",
                ),
                go.Bar(
                    name="Vaccinated",
                    x=data['date'],
                    y=data['daily_vaccinations'],
                    marker_color="lightseagreen"
                ),

                ])

fig.update_layout(
    title=title,
    xaxis_title="Date",
    yaxis_title="Count",
    plot_bgcolor='rgba(0,0,0,0)',
    barmode='stack',
    hovermode="x"
)

fig.show()

title = get_multi_line_title(
    "The Race Against Covid", "Visualizing Rate vs Date")

fig = go.Figure(data=[
                go.Scatter(
                    mode="lines+markers",
                    name="Rate of new deaths",
                    x=data['date'],
                    y=calculate_growth_rate(
                        data['cumulative_total_deaths'].tolist()),
                    marker_color="crimson",
                ),
                go.Scatter(
                    mode="lines+markers",
                    name="Rate of new cases",
                    x=data['date'],
                    y=calculate_growth_rate(
                        data['cumulative_total_cases'].tolist()),
                    marker_color="royalblue"
                ),
                go.Scatter(
                    mode="lines+markers",
                    name="Rate of recovered cases",
                    x=data['date'],
                    y=calculate_growth_rate(
                        (data['cumulative_total_cases']-data['cumulative_total_deaths']-data['active_cases']).tolist()),
                    marker_color="green"
                ),
                ])


fig.update_layout(
    title=title,
    xaxis_title="",
    yaxis_title="Count",
    hovermode="x",
    legend_orientation='h'
)
fig.show()

country_list = []
for i in country_list:
    country = daily_df[daily_df['country'] == i]
    title = get_multi_line_title(
        "The Race Against Covid in "+i, "Visualizing Rate vs Date")

    fig = go.Figure(data=[
                    go.Scatter(
                        mode="lines+markers",
                        name="Rate of new cases",
                        x=country['date'][200:],
                        y=calculate_growth_rate(
                            country['cumulative_total_cases'].tolist())[200:],
                        marker_color="royalblue"
                    )
                    ])

    fig.update_layout(
        title=title,
        xaxis_title="",
        yaxis_title="Count",
        hovermode="x",
        legend_orientation='h'
    )
    fig.show()
