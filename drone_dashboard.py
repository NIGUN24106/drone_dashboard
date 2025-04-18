import streamlit as st
import time
import plotly.graph_objects as go
import pydeck as pdk
from datetime import datetime

# Page config
st.set_page_config(page_title="Drone Journey: PSG Tech to PSG iTech", layout="wide")
st.title("🚁 Drone Simulation: PSG Tech to PSG iTech")

# Coordinates
start_lat, start_lon = 11.024030, 77.002878  # PSG Tech
end_lat, end_lon = 11.065841, 77.094024      # PSG iTech

steps = 50  # Number of movement steps (simulate 50 points)

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = {
        "time": [],
        "voltage": [],
        "altitude": [],
        "temperature": [],
        "latitude": [],
        "longitude": []
    }

# Placeholder container
placeholder = st.empty()

for i in range(steps):
    # Linear interpolation of coordinates
    lat = start_lat + (end_lat - start_lat) * i / steps
    lon = start_lon + (end_lon - start_lon) * i / steps

    # Simulate telemetry
    voltage = round(13.5 - (2.0 * i / steps), 2)  # Decreases from 13.5V to 11.5V
    altitude = round(100 + (400 * i / steps), 2)  # Increases from 100m to 500m
    temperature = round(25 + (3 * i / steps), 2)  # Slight increase

    now = datetime.now().strftime("%H:%M:%S")

    # Save to session
    st.session_state.history["time"].append(now)
    st.session_state.history["voltage"].append(voltage)
    st.session_state.history["altitude"].append(altitude)
    st.session_state.history["temperature"].append(temperature)
    st.session_state.history["latitude"].append(lat)
    st.session_state.history["longitude"].append(lon)

    with placeholder.container():
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🔋 Battery Voltage", f"{voltage} V")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=voltage,
                title={'text': "Battery Level"},
                gauge={'axis': {'range': [11, 14]}}
            ))
            st.plotly_chart(fig, use_container_width=True, key=f"battery_{i}")

        with col2:
            st.metric("🛫 Altitude", f"{altitude} m")
            st.line_chart({"Altitude (m)": st.session_state.history["altitude"]}, use_container_width=True)

        with col3:
            st.metric("🌡️ Temperature", f"{temperature} °C")
            st.line_chart({"Temperature (°C)": st.session_state.history["temperature"]}, use_container_width=True)

        st.subheader("📍 Live Drone Location")
        st.metric("Latitude", lat)
        st.metric("Longitude", lon)

        # Map Layer
        route = [{"lat": la, "lon": lo} for la, lo in zip(
            st.session_state.history["latitude"], st.session_state.history["longitude"]
        )]

        map_layer = pdk.Layer(
            "PathLayer",
            data=[{"path": [[pt["lon"], pt["lat"]] for pt in route]}],
            get_color=[0, 0, 255],
            get_width=4
        )

        scatter = pdk.Layer(
            "ScatterplotLayer",
            data=[{"lat": lat, "lon": lon}],
            get_position=["lon", "lat"],
            get_color=[255, 0, 0],
            get_radius=50
        )

        deck = pdk.Deck(
            initial_view_state=pdk.ViewState(
                latitude=lat,
                longitude=lon,
                zoom=12,
                pitch=0
            ),
            layers=[map_layer, scatter],
            map_style="mapbox://styles/mapbox/satellite-streets-v11"
        )

        st.pydeck_chart(deck, use_container_width=True)

    time.sleep(0.5)
