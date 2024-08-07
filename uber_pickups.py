# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 16:49:51 2024

@author: HP 820 G3
"""

import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
data_url = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(data_url, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data..')
data = load_data(1000)
data_load_state.text('Done!!!')

if st.checkbox('Show row data'):
    st.subheader('Raw data')
    st.write(data)
st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)
hour_to_fil = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_fil]
st.subheader(f'Map of all pickups at {hour_to_fil}:00')
st.map(filtered_data)