import streamlit as st
import time
import plotly.graph_objects as go
import pandas as pd
import pydeck as pdk
from datetime import datetime

# Page config
st.set_page_config(page_title="Drone Telemetry Dashboard", layout="wide")

st.title("Drone Status Monitoring Web Interface")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = {
        "time": [],
        "voltage": [],
        "altitude": [],
        "temperature": []
    }

# Simulate telemetry data with constant values for testing
def get_telemetry_data():
    return {
        "Battery Voltage (V)": 11.5,
        "Roll (°)": 15.0,
        "Pitch (°)": 5.0,
        "Yaw (°)": 0.0,
        "Temperature (°C)": 25.0,
        "Altitude (m)": 500.0,
        "Latitude": 11.0168,
        "Longitude": 76.9558,
        "Connection Health": "Excellent",
        "Time": datetime.now().strftime("%H:%M:%S")
    }

placeholder = st.empty()

# Coimbatore Coordinates for reference
coimbatore_lat = 11.0168
coimbatore_lon = 76.9558

# Live update loop (demo: 1000 iterations)
for i in range(1000):
    data = get_telemetry_data()

    # Store for graphs
    st.session_state.history["time"].append(data["Time"])
    st.session_state.history["voltage"].append(data["Battery Voltage (V)"])
    st.session_state.history["altitude"].append(data["Altitude (m)"])
    st.session_state.history["temperature"].append(data["Temperature (°C)"])

    with placeholder.container():
        col1, col2, col3 = st.columns(3)

        # Battery gauge
        with col1:
            st.metric("Battery Voltage", f"{data['Battery Voltage (V)']} V")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=data["Battery Voltage (V)"],
                title={'text': "Battery Level"},
                gauge={'axis': {'range': [0, 12]}}
            ))
            st.plotly_chart(fig, use_container_width=True, key=f"battery_chart_{i}")

        # Altitude graph
        with col2:
            st.metric("Altitude", f"{data['Altitude (m)']} m")
            st.line_chart(
                {"Altitude (m)": st.session_state.history["altitude"]},
                use_container_width=True
            )

        # Temperature graph
        with col3:
            st.metric("Temperature", f"{data['Temperature (°C)']} °C")
            st.line_chart(
                {"Temperature (°C)": st.session_state.history["temperature"]},
                use_container_width=True
            )

        st.subheader("Other Telemetry Data")
        col4, col5, col6 = st.columns(3)
        with col4:
            st.metric("Latitude", data["Latitude"])
            st.metric("Longitude", data["Longitude"])
        with col5:
            st.metric("Roll", f"{data['Roll (°)']} °")
            st.metric("Pitch", f"{data['Pitch (°)']} °")
            st.metric("Yaw", f"{data['Yaw (°)']} °")
        with col6:
            st.metric("Connection Health", data["Connection Health"])
            st.caption(f"Last updated: {data['Time']}")

        st.subheader("Drone Position Map")

        # Pydeck map displaying Coimbatore and the drone's location
        deck = pdk.Deck(
            initial_view_state=pdk.ViewState(
                latitude=coimbatore_lat,
                longitude=coimbatore_lon,
                zoom=12,
                pitch=0
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=[{
                        'lat': data['Latitude'],
                        'lon': data['Longitude'],
                        'size': 10
                    }],
                    get_position=['lon', 'lat'],
                    get_color=[255, 0, 0],
                    get_radius=50,
                )
            ]
        )

        st.pydeck_chart(deck, use_container_width=True)

    time.sleep(1)
