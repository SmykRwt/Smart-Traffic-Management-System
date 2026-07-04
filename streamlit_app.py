import streamlit as st
import tempfile
import os
from pathlib import Path
import pandas as pd
import time

from app.detection.image_processor import ImageProcessor
from app.detection.video_processor import VideoProcessor
from app.database.repository import AnalyticsRepository

st.set_page_config(
    page_title="Smart Traffic Management System",
    page_icon="🚦",
    layout="wide"
)

# Custom premium CSS injection
st.markdown("""
<style>
    /* Main app styles */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Outfit', 'Inter', sans-serif !important;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    .main-title {
        font-size: 2.8rem !important;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.1rem;
        padding-top: 0px;
    }
    
    .subtitle {
        color: #a0aec0;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }

    /* Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s, border-color 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(79, 172, 254, 0.4);
    }
    
    .metric-val {
        font-size: 2.0rem;
        font-weight: 800;
        margin-top: 0.3rem;
        color: #4facfe;
    }
    
    .metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #a0aec0;
    }
    
    /* Alert cards styling */
    .alert-container {
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
        border-left: 5px solid;
    }
</style>
""", unsafe_allow_html=True)

# Title Header
st.markdown('<h1 class="main-title">🚦 Smart Traffic Management System</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Next-Generation AI Traffic Monitoring & Emergency Vehicle Prioritization</p>', unsafe_allow_html=True)

st.divider()

# Instantiate Database Repository
repository = AnalyticsRepository()

# Sidebar / Config
st.sidebar.markdown("## ⚙️ Control Center")
st.sidebar.markdown("Configure thresholds and run inference")

uploaded_file = st.sidebar.file_uploader(
    "Upload Traffic Video or Image",
    type=["jpg", "jpeg", "png", "bmp", "mp4", "avi", "mov", "mkv"],
)

st.sidebar.markdown("### Settings")
confidence = st.sidebar.slider(
    "Confidence Threshold",
    0.10, 1.00, 0.30, 0.05,
)
st.sidebar.info("YOLO models will ignore detections with confidence below this threshold.")

run = st.sidebar.button(
    "🚀 Launch Vision Agent",
    use_container_width=True,
)

# Set up main display layout
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("🎥 Live Feed Analytics")
    output_placeholder = st.empty()
    
    # Placeholders for real-time charts below feed
    st.markdown("### 📊 Distribution & Trends")
    chart_tabs = st.tabs(["Vehicle Distribution", "Traffic Volume (Database)"])
    with chart_tabs[0]:
        vehicle_dist_placeholder = st.empty()
    with chart_tabs[1]:
        history_chart_placeholder = st.empty()

with col_right:
    st.subheader("📡 Real-time Telemetry")
    
    # Real-time Metrics Panels
    # Grid of metrics
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        card_current = st.empty()
        card_density = st.empty()
    with m_col2:
        card_unique = st.empty()
        card_congestion = st.empty()
        
    card_current.markdown('<div class="metric-card"><div class="metric-label">Current Count</div><div class="metric-val">0</div></div>', unsafe_allow_html=True)
    card_density.markdown('<div class="metric-card" style="margin-top: 15px;"><div class="metric-label">Density</div><div class="metric-val" style="color: #00ff00;">N/A</div></div>', unsafe_allow_html=True)
    card_unique.markdown('<div class="metric-card"><div class="metric-label">Unique Count</div><div class="metric-val">0</div></div>', unsafe_allow_html=True)
    card_congestion.markdown('<div class="metric-card" style="margin-top: 15px;"><div class="metric-label">Congestion</div><div class="metric-val" style="color: #00ff00;">N/A</div></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Dynamic values placeholders
    telemetry_placeholder = st.empty()
    
    st.markdown("### 🚨 System Events & Alerts")
    events_placeholder = st.empty()

# Baseline Dashboard Rendering (before run is pressed)
with chart_tabs[0]:
    vehicle_dist_placeholder.info("Upload media and launch the agent to analyze vehicle distribution.")
with chart_tabs[1]:
    # Populate historical trends from database
    history = repository.get_history(limit=50)
    if history:
        hist_data = {
            "Time": [h.timestamp for h in history],
            "Current Vehicles": [h.current_vehicle_count for h in history],
            "Unique Vehicles": [h.unique_vehicle_count for h in history]
        }
        df_hist = pd.DataFrame(hist_data)
        history_chart_placeholder.line_chart(df_hist.set_index("Time"))
    else:
        history_chart_placeholder.info("PostgreSQL database is currently empty.")

output_placeholder.info("Please upload a file in the sidebar and click 'Launch Vision Agent' to begin.")
events_placeholder.markdown('<div style="color:gray; font-style:italic;">System offline. Waiting for Vision Agent...</div>', unsafe_allow_html=True)

# Run Pipeline
if run:
    if uploaded_file is None:
        st.sidebar.error("Error: Please upload a file first.")
        st.stop()
        
    suffix = Path(uploaded_file.name).suffix
    
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp.write(uploaded_file.read())
    temp.close()
    file_path = temp.name
    
    is_image = suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp"]
    
    progress_bar = st.sidebar.progress(0)
    
    with st.spinner("Processing in progress..."):
        if is_image:
            processor = ImageProcessor()
            output_image, summary = processor.process_image(file_path)
            
            output_placeholder.image(output_image, channels="BGR", use_container_width=True)
            
            analytics = summary["analytics"]
            events = summary["events"] # strings
            
            # Format Density & Congestion colors
            density_color = "#00ff00" if analytics.traffic_density == "LOW" else ("#ffaa00" if analytics.traffic_density == "MEDIUM" else "#ff4b4b")
            congestion_color = "#00ff00" if analytics.congestion_level in ["FREE FLOW", "MODERATE"] else ("#ffaa00" if analytics.congestion_level == "HEAVY" else "#ff4b4b")
            
            # Update metrics cards
            card_current.markdown(f'<div class="metric-card"><div class="metric-label">Current Count</div><div class="metric-val">{analytics.current_vehicle_count}</div></div>', unsafe_allow_html=True)
            card_density.markdown(f'<div class="metric-card" style="margin-top: 15px;"><div class="metric-label">Density</div><div class="metric-val" style="color: {density_color};">{analytics.traffic_density}</div></div>', unsafe_allow_html=True)
            card_unique.markdown(f'<div class="metric-card"><div class="metric-label">Unique Count</div><div class="metric-val">{analytics.unique_vehicle_count}</div></div>', unsafe_allow_html=True)
            card_congestion.markdown(f'<div class="metric-card" style="margin-top: 15px;"><div class="metric-label">Congestion</div><div class="metric-val" style="color: {congestion_color};">{analytics.congestion_level}</div></div>', unsafe_allow_html=True)

            # Update metrics table
            telemetry_placeholder.markdown(f"""
            <div style="background: rgba(255,255,255,0.02); padding: 15px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.05);">
                <table style="width:100%; font-size:1.1rem; border-collapse: collapse;">
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);"><td style="padding:8px 0; color:#a0aec0;">FPS</td><td style="text-align:right; font-weight:bold; color:#4facfe;">{analytics.fps}</td></tr>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);"><td style="padding:8px 0; color:#a0aec0;">Current Vehicles</td><td style="text-align:right; font-weight:bold; color:#ffaa00;">{analytics.current_vehicle_count}</td></tr>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);"><td style="padding:8px 0; color:#a0aec0;">Unique Vehicles</td><td style="text-align:right; font-weight:bold; color:#ffaa00;">{analytics.unique_vehicle_count}</td></tr>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);"><td style="padding:8px 0; color:#a0aec0;">Traffic Density</td><td style="text-align:right; font-weight:bold; color:{density_color};">{analytics.traffic_density}</td></tr>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);"><td style="padding:8px 0; color:#a0aec0;">Congestion Level</td><td style="text-align:right; font-weight:bold; color:{congestion_color};">{analytics.congestion_level}</td></tr>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);"><td style="padding:8px 0; color:#a0aec0;">Stopped Vehicle IDs</td><td style="text-align:right; font-weight:bold; color:#ff4b4b;">{len(analytics.stopped_vehicle_ids)}</td></tr>
                    <tr><td style="padding:8px 0; color:#a0aec0;">Emergency Vehicles</td><td style="text-align:right; font-weight:bold; color:#ff4b4b;">{len(analytics.emergency_vehicles)}</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
            
            # Update bar chart
            if analytics.vehicle_count:
                df = pd.DataFrame(list(analytics.vehicle_count.items()), columns=["Vehicle Class", "Count"])
                vehicle_dist_placeholder.bar_chart(df.set_index("Vehicle Class"))
            else:
                vehicle_dist_placeholder.write("No vehicles detected.")
                
            # Update events
            events_html = ""
            for event_str in events:
                severity = "INFO"
                if "Heavy" in event_str or "Stopped" in event_str:
                    severity = "MEDIUM"
                if "Emergency" in event_str or "Jam" in event_str:
                    severity = "HIGH"
                
                if severity == "HIGH":
                    events_html += f'<div style="background-color:rgba(255,0,0,0.1); border-left: 5px solid red; padding:10px; margin-bottom:10px; border-radius:4px; color:#ff4b4b;"><strong>🚨 {event_str}</strong></div>'
                elif severity == "MEDIUM":
                    events_html += f'<div style="background-color:rgba(255,165,0,0.1); border-left: 5px solid orange; padding:10px; margin-bottom:10px; border-radius:4px; color:#ffaa00;"><strong>⚠️ {event_str}</strong></div>'
                else:
                    events_html += f'<div style="background-color:rgba(0,255,0,0.1); border-left: 5px solid green; padding:10px; margin-bottom:10px; border-radius:4px; color:#00ff00;"><strong>ℹ️ {event_str}</strong></div>'
            if not events_html:
                events_html = '<div style="color:gray; font-style:italic;">No active events. Road is normal.</div>'
            events_placeholder.markdown(events_html, unsafe_allow_html=True)
            
            # Historical trends update
            history = repository.get_history(limit=50)
            if history:
                hist_data = {
                    "Time": [h.timestamp for h in history],
                    "Current Vehicles": [h.current_vehicle_count for h in history],
                    "Unique Vehicles": [h.unique_vehicle_count for h in history]
                }
                df_hist = pd.DataFrame(hist_data)
                history_chart_placeholder.line_chart(df_hist.set_index("Time"))
                
            progress_bar.progress(100)
            st.sidebar.success("Image processed successfully!")
            
        else:
            # Video Processing with Live Streaming Feed
            processor = VideoProcessor()
            frame_index = 0
            
            # Start streaming
            for frame, analytics, events, detections, output_path in processor.process_video_stream(file_path):
                # Update frame
                output_placeholder.image(frame, channels="BGR", use_container_width=True)
                
                # Format Density & Congestion colors
                density_color = "#00ff00" if analytics.traffic_density == "LOW" else ("#ffaa00" if analytics.traffic_density == "MEDIUM" else "#ff4b4b")
                congestion_color = "#00ff00" if analytics.congestion_level in ["FREE FLOW", "MODERATE"] else ("#ffaa00" if analytics.congestion_level == "HEAVY" else "#ff4b4b")
                
                # Update metrics cards
                card_current.markdown(f'<div class="metric-card"><div class="metric-label">Current Count</div><div class="metric-val">{analytics.current_vehicle_count}</div></div>', unsafe_allow_html=True)
                card_density.markdown(f'<div class="metric-card" style="margin-top: 15px;"><div class="metric-label">Density</div><div class="metric-val" style="color: {density_color};">{analytics.traffic_density}</div></div>', unsafe_allow_html=True)
                card_unique.markdown(f'<div class="metric-card"><div class="metric-label">Unique Count</div><div class="metric-val">{analytics.unique_vehicle_count}</div></div>', unsafe_allow_html=True)
                card_congestion.markdown(f'<div class="metric-card" style="margin-top: 15px;"><div class="metric-label">Congestion</div><div class="metric-val" style="color: {congestion_color};">{analytics.congestion_level}</div></div>', unsafe_allow_html=True)

                # Render metrics table dynamically
                telemetry_placeholder.markdown(f"""
                <div style="background: rgba(255,255,255,0.02); padding: 15px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.05);">
                    <table style="width:100%; font-size:1.1rem; border-collapse: collapse;">
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);"><td style="padding:8px 0; color:#a0aec0;">FPS</td><td style="text-align:right; font-weight:bold; color:#4facfe;">{analytics.fps}</td></tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);"><td style="padding:8px 0; color:#a0aec0;">Current Vehicles</td><td style="text-align:right; font-weight:bold; color:#ffaa00;">{analytics.current_vehicle_count}</td></tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);"><td style="padding:8px 0; color:#a0aec0;">Unique Vehicles</td><td style="text-align:right; font-weight:bold; color:#ffaa00;">{analytics.unique_vehicle_count}</td></tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);"><td style="padding:8px 0; color:#a0aec0;">Traffic Density</td><td style="text-align:right; font-weight:bold; color:{density_color};">{analytics.traffic_density}</td></tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);"><td style="padding:8px 0; color:#a0aec0;">Congestion Level</td><td style="text-align:right; font-weight:bold; color:{congestion_color};">{analytics.congestion_level}</td></tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);"><td style="padding:8px 0; color:#a0aec0;">Stopped Vehicles</td><td style="text-align:right; font-weight:bold; color:#ff4b4b;">{len(analytics.stopped_vehicle_ids)}</td></tr>
                        <tr><td style="padding:8px 0; color:#a0aec0;">Emergency Vehicles</td><td style="text-align:right; font-weight:bold; color:#ff4b4b;">{len(analytics.emergency_vehicles)}</td></tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
                
                # Update bar chart
                if analytics.vehicle_count:
                    df = pd.DataFrame(list(analytics.vehicle_count.items()), columns=["Vehicle Class", "Count"])
                    vehicle_dist_placeholder.bar_chart(df.set_index("Vehicle Class"))
                
                # Update events
                events_html = ""
                for event in events:
                    if event.severity == "HIGH":
                        events_html += f'<div style="background-color:rgba(255,0,0,0.1); border-left: 5px solid red; padding:12px; margin-bottom:10px; border-radius:6px; color:#ff4b4b;"><strong>🚨 {event.title}</strong>: {event.description}</div>'
                    elif event.severity == "MEDIUM":
                        events_html += f'<div style="background-color:rgba(255,165,0,0.1); border-left: 5px solid orange; padding:12px; margin-bottom:10px; border-radius:6px; color:#ffaa00;"><strong>⚠️ {event.title}</strong>: {event.description}</div>'
                    else:
                        events_html += f'<div style="background-color:rgba(0,255,0,0.1); border-left: 5px solid green; padding:12px; margin-bottom:10px; border-radius:6px; color:#00ff00;"><strong>ℹ️ {event.title}</strong>: {event.description}</div>'
                if not events_html:
                    events_html = '<div style="color:gray; font-style:italic;">No active events. Road is normal.</div>'
                events_placeholder.markdown(events_html, unsafe_allow_html=True)
                
                # Update SQL historical trends every 30 frames to limit DB traffic
                if frame_index % 30 == 0:
                    history = repository.get_history(limit=50)
                    if history:
                        hist_data = {
                            "Time": [h.timestamp for h in history],
                            "Current Vehicles": [h.current_vehicle_count for h in history],
                            "Unique Vehicles": [h.unique_vehicle_count for h in history]
                        }
                        df_hist = pd.DataFrame(hist_data)
                        history_chart_placeholder.line_chart(df_hist.set_index("Time"))
                        
                frame_index += 1
                
            progress_bar.progress(100)
            st.sidebar.success("Video processed and streamed successfully!")
            
    # Clean up local temporary file
    os.remove(file_path)