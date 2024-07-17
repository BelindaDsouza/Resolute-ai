import pandas as pd
import streamlit as st

# Load the raw data
data = pd.read_excel('Downloads/rawdata.xlsx')

# Convert 'date' and 'time' columns to string
data['date'] = data['date'].astype(str)
data['time'] = data['time'].astype(str)

# Combine 'date' and 'time' columns and convert to datetime
data['datetime'] = pd.to_datetime(data['date'] + ' ' + data['time'])

# Sort the data by datetime
data = data.sort_values(by='datetime')

# Normalize 'location' and 'activity' columns to lowercase for consistent processing
data['location'] = data['location'].str.lower()
data['activity'] = data['activity'].str.lower()

# Calculate durations
data['duration'] = data['datetime'].diff().dt.total_seconds().fillna(0)
print(data.head())

# Debug: Check unique values in 'location' and 'activity' columns
print("Unique 'location' values:", data['location'].unique())
print("Unique 'activity' values:", data['activity'].unique())

# Initialize the results dictionary
results = {'date': [], 'total_inside_duration(in sec)': [], 'total_outside_duration(in sec)': [], 'picking_count': [], 'placing_count': []}

# Process data datewise
for date, group in data.groupby(data['datetime'].dt.date):
    inside_duration = group[group['position'] == 'inside']['duration'].sum()
    print(inside_duration)
    outside_duration = group[group['position'] == 'outside']['duration'].sum()
    picking_count = group[group['activity'] == 'picked'].shape[0]
    placing_count = group[group['activity'] == 'placed'].shape[0]
    
    results['date'].append(date)
    results['total_inside_duration(in sec)'].append(inside_duration)
    results['total_outside_duration(in sec)'].append(outside_duration)
    results['picking_count'].append(picking_count)
    results['placing_count'].append(placing_count)

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Streamlit app
st.title("Activity Data Analysis")

# Display the processed data
st.subheader("Processed Data")
st.write(results_df)

# Display total durations
st.subheader("Datewise Total Durations")
st.write("Total durations inside and outside on each date:")
st.write(results_df[['date', 'total_inside_duration(in sec)', 'total_outside_duration(in sec)']])

# Display activity counts
st.subheader("Datewise Activity Counts")
st.write("Number of picking and placing activities on each date:")
st.write(results_df[['date', 'picking_count', 'placing_count']])
