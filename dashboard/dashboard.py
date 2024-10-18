import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Air Quality from Tiantan Analysis by Rahul Bhatara")
st.title('Air Quality Analysis Dashboard: Tiantan Station')

# Load data
csv_files = [file for file in os.listdir('data/') if file.endswith('.csv')]
dataframes = []
for file in csv_files:
    file_path = os.path.join('data/', file)
    d = pd.read_csv(file_path)
    dataframes.append(d)

df = pd.concat(dataframes, ignore_index=True)

# About me
st.markdown("""
### About Me
- **Name**: Mhd. Rahul Bhatara Guru
- **Email Address**: rahulbhataraguru@gmail.com
- **Dicoding ID**: [rahulbhatara](https://www.dicoding.com/users/rahulbhatara/)

### Project Overview
By analyzing ozone level data recorded at the Tiantan station, this project investigates how temperature fluctuations influence ozone concentrations in the atmosphere. Examining trends, seasonal variations, and the interplay between temperature and ozone formation, this tool aims to provide valuable insights for environmental monitoring, air quality forecasting, and public health initiatives.
""")

st.subheader("Data Preview")
st.write(df.head())

st.subheader("Missing Data Pattern")
missing_percentage = df.isnull().mean() * 100
missing_percentage = missing_percentage[missing_percentage > 0]

if not missing_percentage.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    missing_percentage.plot(kind='bar', color='salmon', ax=ax)
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}%', (p.get_x() * 1.005, p.get_height() * 1.005), fontsize=12)
    ax.set_title('Missing Data Pattern')
    ax.set_xlabel('Column')
    ax.set_ylabel('Percentage of Missing Data (%)')
    st.pyplot(fig)
else:
    st.write("No missing data!")

# Data Cleaning and Handling Missing Values
df_fixed = df.copy()
columns_numerik_to_fill = df_fixed.select_dtypes(include=['float64']).columns
for col in columns_numerik_to_fill:
    df_fixed[col].fillna(df_fixed[col].mean(), inplace=True)
columns_object = df_fixed.select_dtypes(include=['object']).columns
for col in columns_object:
    df_fixed[col].fillna(df_fixed[col].mode()[0], inplace=True)

st.subheader("Weakly Average Air Temperature Time Series")
df_fixed['date'] = pd.to_datetime(df_fixed[['year', 'month', 'day']])
df_fixed['week'] = df_fixed['date'].dt.to_period('W')
weekly_stats = df_fixed.groupby('week').agg({
    'TEMP': ['mean', 'min', 'max'],
    'O3': ['mean', 'min', 'max']
})
weekly_stats.columns = ['TEMP_mean', 'TEMP_min', 'TEMP_max', 'O3_mean', 'O3_min', 'O3_max']
weekly_stats = weekly_stats.reset_index()
weekly_stats['week'] = weekly_stats['week'].dt.to_timestamp()
fig, ax = plt.subplots(figsize=(15, 6))
ax.plot(range(len(weekly_stats)), weekly_stats.TEMP_mean, label='Average Temperature')
num_ticks = 15
step = len(weekly_stats) // num_ticks
tick_locations = np.arange(0, len(weekly_stats), step)
tick_labels = weekly_stats['week'].astype(str).iloc[tick_locations]
ax.set_xticks(tick_locations)
ax.set_xticklabels(tick_labels, rotation=45, ha='right')
ax.set_title('Weekly Average Air Temperature Time Series')
ax.set_xlabel('Weeks')
ax.set_ylabel('Temperature (°C)')
ax.legend()
plt.tight_layout()
st.pyplot(fig)

st.subheader("Average Temperature Analysis for Each Month of the Year")
df_fixed['date'] = pd.to_datetime(df_fixed[['year', 'month', 'day']])
monthly_temp = df_fixed.groupby(df_fixed['date'].dt.to_period('M'))['TEMP'].mean().reset_index()
monthly_temp['month'] = monthly_temp['date'].dt.month
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=monthly_temp, x='month', y='TEMP', ax=ax)
ax.set_title('Average Monthly Temperature Throughout the Year')
ax.set_xlabel('Month')
ax.set_ylabel('Temperature (°C)')
ax.set_xticks(range(1, 13))
st.pyplot(fig)

st.subheader("Monthly Temperature Distribution")
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=df_fixed, x=df_fixed['date'].dt.month, y='TEMP', ax=ax)
ax.set_title('Monthly Temperature Distribution')
ax.set_xlabel('Month')
ax.set_ylabel('Temperature (°C)')
st.pyplot(fig)

st.subheader("Monthly Temperature Heatmap Across Years")
df_fixed['year'] = df_fixed['date'].dt.year
df_fixed['month'] = df_fixed['date'].dt.month
temp_monthly = df_fixed.groupby(['year', 'month'])['TEMP'].mean().reset_index()
temp_pivot = temp_monthly.pivot(index='month', columns='year', values='TEMP')
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(temp_pivot, cmap='YlOrRd', annot=True, fmt='.1f', ax=ax)
ax.set_title('Monthly Temperature Heatmap Across Years')
ax.set_xlabel('Year')
ax.set_ylabel('Month')
st.pyplot(fig)

st.subheader("Correlation coefficient between Temperature (TEMP) and Ozone (O3)")
variables = ['TEMP', 'O3', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO']
correlation_matrix = df_fixed[variables].corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0, ax=ax)
ax.set_title('Correlation Coefficient Heatmap')
plt.tight_layout()
st.pyplot(fig)
correlation_temp_o3 = correlation_matrix.loc['TEMP', 'O3']
st.write(f"Correlation coefficient between Temperature (TEMP) and Ozone (O3): {correlation_temp_o3:.4f}")

st.subheader("Regression Plot: Temperature vs Ozone Level")
fig, ax = plt.subplots(figsize=(10, 6))
sns.regplot(x='TEMP', y='O3', data=df_fixed, scatter_kws={'alpha':0.5}, line_kws={'color':'red'}, ax=ax)
ax.set_title('Regression Plot: Temperature vs Ozone Level')
ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('Ozone (O3) Concentration')
plt.tight_layout()
st.pyplot(fig)

st.subheader("Conclusion")
st.markdown("""
##### Question 1: How does weather temperature change throughout the year?
###### - The analysis of the Weekly Average Air Temperature Time Series plot reveals a distinct seasonal pattern in temperature fluctuations, characterized by low temperatures at the start of the year, a gradual increase peaking around mid-year, followed by a decline towards year-end. This cyclical behavior underscores the influence of seasonal changes on temperature dynamics.
""")
st.markdown("""
##### Question 2 How is the correlation between air temperature (TEMP) and ozone (O3) quality in the atmosphere?
###### - Furthermore, the relationship between air temperature (TEMP) and ozone levels (O3) is marked by a positive correlation. As temperatures rise, ozone concentrations tend to increase correspondingly. This finding highlights the potential implications of rising temperatures on air quality, emphasizing the need for ongoing monitoring and management of ozone levels in the context of climate change.
""")