import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

PROGRAM_DATA_COLS = ["Program", "Approx. Rebate Value", "Link"]
RESULTS_DF_COLS = ["address", "retrofit_cost", "bill_savings", "kwh_savings"]

MOCK_DATA = {
    "address": [
        "123 Main St, Brooklyn, NY",
        "456 Park Ave, Brooklyn, NY",
        "789 Atlantic Ave, Brooklyn, NY",
        "101 Court St, Brooklyn, NY",
        "202 Flatbush Ave, Brooklyn, NY",
        "303 Bedford Ave, Brooklyn, NY",
        "404 Fulton St, Brooklyn, NY",
        "505 Smith St, Brooklyn, NY",
        "606 Nostrand Ave, Brooklyn, NY",
        "707 Myrtle Ave, Brooklyn, NY",
        "808 Dekalb Ave, Brooklyn, NY",
        "909 Kings Hwy, Brooklyn, NY",
        "100 Grand St, Brooklyn, NY",
        "111 Berry St, Brooklyn, NY",
        "222 Jefferson Ave, Brooklyn, NY",
        "333 5th Ave, Brooklyn, NY"
    ],
    "retrofit_cost": [
        15000, 12000, 18000, 9500, 11000, 16000, 12500, 14000,
        15500, 13000, 19000, 10000, 11500, 17000, 13500, 14500
    ],
    "bill_savings": [
        1200, 950, 1500, 600, 800, 1400, 1000, 1100,
        1250, 970, 1600, 650, 850, 1450, 1050, 1120
    ],
    "kwh_savings": [
        10000, 8500, 12000, 5000, 7500, 11000, 9000, 9500,
        10200, 8700, 12500, 5500, 7700, 11300, 9200, 9700
    ],
    "latitude": [
        40.6782, 40.6805, 40.6857, 40.6929, 40.6829, 40.7035, 40.6944, 40.6868,
        40.6689, 40.6951, 40.6896, 40.6085, 40.7115, 40.7223, 40.6899, 40.7435
    ],
    "longitude": [
        -73.9442, -73.9558, -73.9767, -73.9937, -73.9754, -73.9530, -73.9871, -73.9995,
        -73.9427, -73.9608, -73.9297, -73.9576, -73.9502, -73.9575, -73.9289, -73.9615
    ],
    "yearbuilt": [
        1920, 1950, 1985, 1975, 1965, 1930, 1990, 2000,
        1910, 1940, 1970, 1960, 2005, 2015, 1890, 2020
    ],
    "numfloors": [
        3, 5, 7, 6, 4, 8, 2, 10,
        3, 5, 9, 4, 6, 15, 3, 12
    ],
    "bldgarea": [
        5000, 7000, 12000, 9000, 8500, 15000, 3000, 25000,
        4800, 7200, 13000, 8700, 9500, 20000, 4000, 22000
    ],
    "assesstot": [
        500000, 700000, 1200000, 900000, 850000, 1500000, 300000, 2500000,
        480000, 720000, 1300000, 870000, 950000, 2000000, 400000, 2200000
    ]
    }

st.set_page_config(layout="wide", page_title="glow")
st.logo("images/glow_logo.png", size="large")
st.title("glow")
st.write("portal view for contractors")
st.markdown("---")


col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.subheader("Select Region")
    region = st.selectbox(
        label="",
        options=[
            None,
            # "Manhattan",
            "Brooklyn",
            # "Queens",
            # "Staten Island",
            # "Bronx",
        ],
    )
with col2:
    st.subheader("Select EE technologies:")
    weather_stripping = st.checkbox("Weather Stripping")
    insulation = st.checkbox("Insulation")
    windows = st.checkbox("Windows")
    lighting = st.checkbox("Lighting")
with col3:
    st.subheader("")
    appliances = st.checkbox("Appliances")
    hvac = st.checkbox("HVAC")
    controls = st.checkbox("Controls")


# Initialize session state
if "load_results" not in st.session_state:
    st.session_state.load_results = False

if st.button("Load Results") and (region):
    st.session_state.load_results = True

if st.session_state.load_results:
    # df = pd.read_csv(f"data/{region}.csv")
    # filtered_df = df[df['State'] == region]

    st.header(f"Avaliable EE funding programs for {region}")
    program_data = pd.DataFrame(pd.read_csv("data/ee_program_data/nyc.csv"))
    selected_technologies = []
    if weather_stripping:
        selected_technologies.append("Weather Stripping")
    elif insulation:
        selected_technologies.append("Insulation")
    elif windows:
        selected_technologies.append("Windows")
    elif lighting:
        selected_technologies.append("Lighting")
    elif appliances:
        selected_technologies.append("Appliances")
    elif hvac:
        selected_technologies.append("HVAC")
    elif controls:
        selected_technologies.append("Controls")

    if selected_technologies:
        filtered_program_data = program_data[program_data['Eligible Technologies'].apply(lambda techs: any(item in techs for item in selected_technologies))]
        st.dataframe(filtered_program_data[PROGRAM_DATA_COLS], hide_index=True)
    else:
        st.write("No eligible funding programs found")

    results_df = pd.DataFrame(MOCK_DATA)

    results_col1, results_col2 = st.columns([1.4, 2])
    with results_col1:
        st.header(f"Top Candidates For {region}")
        st.dataframe(results_df[RESULTS_DF_COLS], hide_index=True, height=600)

    with results_col2:
        st.header("")
        m = folium.Map(
            location=[results_df['latitude'].mean(), results_df['longitude'].mean()],
            zoom_start=12,
            tiles="cartodb positron",
        )
        # Add points to the map
        for _, row in results_df.iterrows():
            tooltip = folium.Tooltip(f"""
            <b>Year Built:</b> {row['yearbuilt']} <br>
            <b>Num Floors:</b> {row['numfloors']} <br>
            <b>Building Area:</b> {row['bldgarea']} <br>
            <b>Building Value:</b> ${round(row['assesstot'] / 1_000_000, 2)}mil <br>
            <b>Address:</b> {row['address']} <br>
            """)
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=4,
                color=None,
                stroke=False,
                fill=True,
                fill_color="blue",
                fill_opacity=0.7,
                tooltip=tooltip,
            ).add_to(m)
        st_folium(m, height=600, width=1000)

    st.markdown("---")
    st.header("🚧👷🚧")
    st.subheader("please note")
    st.write("this website is in active development, and is currently using mock data")
    st.markdown("---")