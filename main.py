import streamlit as st

import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(layout="wide")
st.logo("images/glow_logo.png", size="large")
st.title("glow")
# st.subheader("Green Living through Optimized Weatherization")

selected_state = st.selectbox("Select a State:", options=[None, 'NY', 'CA'])

data = {
    'State': ['California', 'New York', 'Texas', 'Florida', 'Illinois'],
    'City': ['Los Angeles', 'New York City', 'Houston', 'Miami', 'Chicago'],
    'Latitude': [34.0522, 40.7128, 29.7604, 25.7617, 41.8781],
    'Longitude': [-118.2437, -74.0060, -95.3698, -80.1918, -87.6298],
    'Value': [100, 200, 150, 120, 180]  # Example column
}
df = pd.DataFrame(data)

if selected_state is not None:
    filtered_df = df[df['State'] == selected_state]

    # Display the filtered DataFrame as a table
    st.write("### Data Table for", selected_state)
    st.dataframe(filtered_df)

    m = folium.Map(location=[40.75502015474453, -73.9926955664234], zoom_start=10, tiles="cartodb positron")
    st_folium(m, height=600, width=1000)
