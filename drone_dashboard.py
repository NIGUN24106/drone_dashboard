import streamlit as st
import random
import time
import plotly.graph_objects as go
import pandas as pd
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

# Simulate telemetry data
def get_telemetry_data():
    return {
        "Battery Voltage (V)": round(random.uniform(0, 12), 2),
        "Roll (°)": round(random.uniform(-180, 180), 2),
        "Pitch (°)": round(random.uniform(-90, 90), 2),
        "Yaw (°)": round(random.uniform(-180, 180), 2),
        "Temperature (°C)": round(random.uniform(-10, 50), 2),
        "Altitude (m)": round(random.uniform(0, 1000), 2),
        "Latitude": round(random.uniform(-90, 90), 6),
        "Longitude": round(random.uniform(-180, 180), 6),
        "Connection Health": random.choice(["Excellent", "Poor", "No Signal"]),
        "Time": datetime.now().strftime("%H:%M:%S")
    }

placeholder = st.empty()

# Live update loop (demo: 1000 iterations)
for _ in range(1000):
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
            st.plotly_chart(fig, use_container_width=True)

        # Altitude graph
        with col2:
            st.metric("Altitude", f"{data['Altitude (m)']} m")
            st.line_chart({
                "Altitude (m)": st.session_state.history["altitude"]
            })

        # Temperature graph
        with col3:
            st.metric("Temperature", f"{data['Temperature (°C)']} °C")
            st.line_chart({
                "Temperature (°C)": st.session_state.history["temperature"]
            })

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
        gps_df = pd.DataFrame({'lat': [data['Latitude']], 'lon': [data['Longitude']]})
        st.map(gps_df)

    time.sleep(1)
