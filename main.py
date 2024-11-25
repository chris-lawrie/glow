import streamlit as st

import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(layout="wide", page_title="glow")
st.logo("images/glow_logo.png", size="large")
st.title("glow")

col1, col2 = st.columns([1, 2])

with col1:
    region = st.selectbox(
        "Select Region:",
        options=[
            None,
            "Manhattan",
            "Brooklyn",
            "Queens",
            "Staten Island",
            "Bronx",
        ],
    )

with col2:
    st.text("Select EE technologies:")
    weather_stripping = st.checkbox("Weather Stripping")
    insulation = st.checkbox("Insulation")
    windows = st.checkbox("Windows")
    appliances = st.checkbox("Appliances")
    hvac = st.checkbox("HVAC")

# Initialize session state
if "load_results" not in st.session_state:
    st.session_state.load_results = False

if st.button("Load Results"):
    st.session_state.load_results = True

if st.session_state.load_results:
    # df = pd.read_csv(f"processed_data/{region}.csv")
    # filtered_df = df[df['State'] == region]

    filtered_df = pd.DataFrame(
        data = {
            "address": [
                "123 Main St, Manhattan, NY",
                "456 Park Ave, Brooklyn, NY",
                "789 Queens Blvd, Queens, NY",
                "101 Staten Ln, Staten Island, NY",
                "202 Bronx Rd, Bronx, NY",
                "303 Broadway, Manhattan, NY",
                "404 Bedford Ave, Brooklyn, NY",
                "505 Jamaica Ave, Queens, NY",
            ] * 2,
            "retrofit_cost": [15000, 12000, 18000, 9500, 11000, 16000, 12500, 14000] * 2,
            "bill_savings": [1200, 950, 1500, 600, 800, 1400, 1000, 1100] * 2,
            "kwh_savings": [10000, 8500, 12000, 5000, 7500, 11000, 9000, 9500] * 2,
        }
    )
    filtered_df.set_index('address', inplace=True, drop=True)

    results_col1, results_col2 = st.columns([1, 2])

    with results_col1:
        st.write("Top Candidates For", region)
        st.dataframe(filtered_df)


    with results_col2:
        m = folium.Map(
            location=[40.75502015474453, -73.9926955664234],
            zoom_start=10,
            tiles="cartodb positron",
        )
        st_folium(m, height=600, width=1000)

    st.header("Avaliable EE funding programs:")
    st.dataframe(filtered_df)
