# Importing required libraries

import requests
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.express as px

# setting page configuration
st.set_page_config(
    page_title="Real-Time Earthquake Analytics Dashboard",
    layout="wide"
)

# Defining function for fetching real-time earthquake data

def fetch_earthquake_data(min_magnitude, limit):
    # defining API endpoint
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    # defining query parameters
    params = {
        "format": "geojson",
        "orderby": "time",
        "minmagnitude": min_magnitude,
        "limit": limit
    }

    try:
        # sending request with parameters
        response = requests.get(url, params=params, timeout=10)

        # validating HTTP status
        response.raise_for_status()

        # validating non-empty response
        if not response.text.strip():
            raise ValueError("Empty response received from API")

        # converting response to JSON
        data = response.json()

        # validating expected JSON structure
        if "features" not in data:
            raise ValueError("Unexpected API response structure")

        return data

    except requests.exceptions.Timeout:
        st.error("Request timed out while contacting the earthquake API.")
        return {"features": []}

    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP error occurred: {e}")
        return {"features": []}

    except requests.exceptions.JSONDecodeError:
        st.error("Failed to decode API response as JSON.")
        return {"features": []}

    except Exception as e:
        st.error(f"Unexpected error occurred: {e}")
        return {"features": []}



# Defining function for processing raw JSON data

def process_earthquake_data(data):
    # handling empty or invalid API response
    if not data or "features" not in data or len(data["features"]) == 0:
        return pd.DataFrame(
            columns=[
                "place",
                "magnitude",
                "time",
                "longitude",
                "latitude",
                "depth_km",
                "tsunami_flag",
                "felt_reports"
            ]
        )

    records = []

    for feature in data["features"]:
        properties = feature.get("properties", {})
        geometry = feature.get("geometry", {})
        coordinates = geometry.get("coordinates", [None, None, None])

        records.append({
            "place": properties.get("place"),
            "magnitude": properties.get("mag"),
            "time": pd.to_datetime(properties.get("time"), unit="ms", errors="coerce"),
            "longitude": coordinates[0],
            "latitude": coordinates[1],
            "depth_km": coordinates[2],
            "tsunami_flag": properties.get("tsunami"),
            "felt_reports": properties.get("felt")
        })

    return pd.DataFrame(records)



# Defining dashboard title

st.title("Real-Time Earthquake Geospatial Analytics")


# Defining sidebar controls

st.sidebar.header("Data Controls")

min_magnitude = st.sidebar.slider(
    "Minimum Magnitude Threshold",
    min_value=0.0,
    max_value=8.0,
    value=2.5,
    step=0.1
)

event_limit = st.sidebar.selectbox(
    "Number of Recent Events",
    options=[50, 100, 250, 500],
    index=1
)


# Fetching and processing data

raw_data = fetch_earthquake_data(min_magnitude, event_limit)
df = process_earthquake_data(raw_data)

# Sorting data chronologically
df = df.sort_values("time", ascending=False)


# Defining descriptive statistics

st.subheader("Descriptive Statistics")

if not df.empty:
    st.dataframe(df[["magnitude", "depth_km"]].describe())
else:
    st.warning("No earthquake data available for the selected filters.")


# Defining summary metrics

st.subheader("Summary Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Earthquake Events", len(df))

with col2:
    st.metric(
        "Maximum Magnitude",
        round(df["magnitude"].max(), 2) if not df.empty else "N/A"
    )

with col3:
    st.metric(
        "Average Depth (km)",
        round(df["depth_km"].mean(), 2) if not df.empty else "N/A"
    )


# Defining spatial distribution map

st.subheader("Spatial Distribution of Earthquakes")

map_object = folium.Map(location=[0, 0], zoom_start=2, tiles="CartoDB positron")

for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=(row["magnitude"] or 0) * 2,
        popup=f"""
        Location: {row['place']}
        Magnitude: {row['magnitude']}
        Depth (km): {row['depth_km']}
        """,
        color="black",
        fill=True,
        fill_opacity=0.5
    ).add_to(map_object)

st_folium(map_object, width=1200, height=500)


# Defining magnitude distribution

st.subheader("Magnitude Distribution")

if not df.empty:
    fig_mag = px.histogram(
        df,
        x="magnitude",
        nbins=25,
        title="Frequency Distribution of Earthquake Magnitudes"
    )
    st.plotly_chart(fig_mag, use_container_width=True)


# Defining temporal analysis

st.subheader("Temporal Earthquake Activity")

if not df.empty:
    df_sorted = df.sort_values("time")
    fig_time = px.line(
        df_sorted,
        x="time",
        y="magnitude",
        title="Earthquake Magnitude Over Time"
    )
    st.plotly_chart(fig_time, use_container_width=True)


# Defining raw data table

st.subheader("Raw Earthquake Data")

st.dataframe(df)
