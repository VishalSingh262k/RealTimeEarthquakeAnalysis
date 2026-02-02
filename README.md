# Real-Time Earthquake Analytics Dashboard

A real-time data visualization dashboard built with [Streamlit](https://streamlit.io/) that fetches and displays earthquake data from the USGS (United States Geological Survey) API. The application provides geospatial analytics, statistical summaries, and interactive charts to explore seismic activity.

The app is deployed on Streamlit Community Cloud on this link: https://realtimeearthquakeanalysis.streamlit.app/

## Features

- **Real-Time Data**: Fetches the latest earthquake data based on user-defined criteria.
- **Interactive Map**: Visualizes earthquake locations with magnitude-scaled markers using Folium.
- **Statistical Insights**: Displays summary metrics like total events, maximum magnitude, and average depth.
- **Data Visualization**:
  - **Magnitude Distribution**: Histogram showing the frequency of different earthquake magnitudes.
  - **Temporal Analysis**: Line chart tracking earthquake magnitude over time.
- **Data Filtering**: Sidebar controls to filter by minimum magnitude and number of recent events.
- **Raw Data View**: Explore the underlying dataset in a tabular format.

## Tech Stack

- **Python**: Core programming language.
- **Streamlit**: Web framework for building the dashboard.
- **Pandas**: Data manipulation and analysis.
- **Requests**: HTTP library for API calls.
- **Folium & Streamlit-Folium**: Interactive map visualizations.
- **Plotly Express**: Interactive charting library.

## Installation

1.  **Clone the repository** (if required):
    ```bash
    git clone git@github.com:VishalSingh262k/RealTimeEarthquakeAnalysis.git
    cd RealTimeEarthquakeAnalysis
    ```

2.  **Install dependencies**:
    Ensure you have Python installed. It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    # Or install manually:
    pip install streamlit pandas requests folium streamlit-folium plotly
    ```

## Usage

1.  **Run the application**:
    Navigate to the project directory in your terminal and run:
    ```bash
    streamlit run earthquakeApp.py
    ```

2.  **Explore the Dashboard**:
    - Use the sidebar to adjust the **Minimum Magnitude Threshold** and **Number of Recent Events**.
    - Interact with the map and charts to analyze the data.

## API Source

This application uses the [USGS Earthquake Hazards Program API](https://earthquake.usgs.gov/fdsnws/event/1/).
