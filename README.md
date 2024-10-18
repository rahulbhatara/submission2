# Air Quality Analysis Project: Tiantan Station

## Live Dashboard
https://rahulbhatara.streamlit.app/

## Project Overview
This project analyzes ozone level data recorded at the Tiantan station to investigate how temperature fluctuations influence ozone concentrations in the atmosphere. By examining trends, seasonal variations, and the interplay between temperature and ozone formation, this tool aims to provide valuable insights for environmental monitoring, air quality forecasting, and public health initiatives.

## Libraries Used
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- NumPy

## How to Run the Dashboard

To run the Air Quality Analysis Dashboard, follow these steps:

### Setup Environment

1. **Install Required Packages**:
   - The following packages are necessary for running the analysis and the dashboard:
     ```
     pip install pandas numpy matplotlib seaborn streamlit
     ```

     or you can do
     ```
     pip install -r requirements.txt
     ```

### Run the Streamlit App

1. **Navigate to the Project Directory** where `dashboard.py` is located.

2. **Run the Streamlit App**:
    ```
    streamlit run dashboard.py
    ```

## Dashboard Features

The dashboard includes the following visualizations and analyses:

1. Data Preview
2. Missing Data Pattern Analysis
3. Weekly Average Air Temperature Time Series
4. Average Temperature Analysis for Each Month of the Year
5. Monthly Temperature Distribution
6. Monthly Temperature Heatmap Across Years
7. Correlation Coefficient Heatmap (including TEMP, O3, PM2.5, PM10, SO2, NO2, CO)
8. Regression Plot: Temperature vs Ozone Level

## Conclusions

The dashboard provides insights into two main questions:

1. How does weather temperature change throughout the year?
2. How is the correlation between air temperature (TEMP) and ozone (O3) quality in the atmosphere?

The analysis reveals seasonal patterns in temperature fluctuations and a positive correlation between temperature and ozone levels.

## About Me
- **Name**: Mhd. Rahul Bhatara Guru
- **Email Address**: rahulbhataraguru@gmail.com
- **Dicoding ID**: [rahulbhatara](https://www.dicoding.com/users/rahulbhatara)