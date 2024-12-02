import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

from calculations import find_top_n_candidates
from mapping_code import map_candidates

BOROUGH_MAP = {
    "Bronx":"bronx",
    "Brooklyn":"brooklyn",
    "Manhattan":"manhattan",
    "Queens":"queens",
    "Staten Island":"staten_island",
}
PROGRAM_DATA_COLS = ["Program", "Approx. Rebate Value", "Link"]
RESULTS_DF_COLS = [
    "address"
]  # , "retrofit_cost", "bill_savings", "kwh_savings"]


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
            "Bronx",
            "Brooklyn",
            "Manhattan",
            "Queens",
            "Staten Island",
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
        filtered_program_data = program_data[
            program_data["Eligible Technologies"].apply(
                lambda techs: any(
                    item in techs for item in selected_technologies
                )
            )
        ]
        st.dataframe(filtered_program_data[PROGRAM_DATA_COLS], hide_index=True)
    else:
        st.write("No eligible funding programs found")

    results_df = find_top_n_candidates(
        df=pd.read_csv(f"data/building_data/{BOROUGH_MAP[region]}.csv"), n=500
    )

    results_col1, results_col2 = st.columns([1.4, 2])
    with results_col1:
        st.header(f"Top Candidates For {region}")
        st.dataframe(results_df[RESULTS_DF_COLS], hide_index=True, height=600)

    with results_col2:
        st.header("")
        st_folium(map_candidates(results_df), height=600, width=1000)

    st.markdown("---")
    st.header("🚧👷🚧")
    st.subheader("please note")
    st.write(
        "this website is in active development, and is currently using mock data"
    )
    st.markdown("---")
