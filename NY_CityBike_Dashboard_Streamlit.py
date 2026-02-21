#################################### NEW YORK CITY BIKES DASHBOARD ##########################################

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
import plotly.io as pio
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
warnings.filterwarnings('ignore')

# ───────────────────────────────────────────────
# CONFIGURATION
# ───────────────────────────────────────────────
sns.set_theme(style="darkgrid")
plt.style.use('dark_background')

st.set_page_config(page_title="New York CitiBike 2022", layout="wide")

# ─────────────────────────────────────────────────
# TITLE
# ─────────────────────────────────────────────────

st.title("New York CitiBike 2022")

st.markdown("The dashboard’s purpose is to visually synthesize Citi Bike usage, weather patterns, and station dynamics to help decision‑makers quickly identify distribution bottlenecks and guide strategic improvements to bike availability across New York City.")

####################### Import data #########################################

top15 = pd.read_csv(r"C:\Users\ZenBook\top15_start_NY_2022.csv", index_col = 0)
df_1 = pd.read_csv(r"C:\Users\ZenBook\df_1_reduced_data.csv", index_col = 0)
df_daily = pd.read_csv(r"C:\Users\ZenBook\df_daily_trips_temp.csv", index_col = 0)

############################# DEFINE THE CHARTS #############################

st.markdown(
    """ 
### CitiBike in New York City

CitiBike is New York City’s flagship bike‑sharing program, offering residents and visitors a fast, sustainable alternative to traditional transportation. **Since its launch in 2013**, the system has expanded into one of the largest in the world, serving Manhattan, Brooklyn, Queens, and parts of the Bronx with thousands of bikes and docking stations. **As ridership continues to grow, so do the operational challenges—stations frequently run empty in high‑demand areas while others remain full, limiting users’ ability to pick up or return bikes**. This dashboard explores CitiBike’s 2022 usage patterns to reveal when and where these imbalances occur, helping identify opportunities to improve distribution efficiency and enhance the overall rider experience.
"""
)

## Bar chart 

fig = go.Figure(go.Bar(x = top15['start_station_name'], y = top15['value'], marker={'color': top15['value'],'colorscale': 'gnbu'}))
fig.update_layout(
    title = 'Top 15 most popular start stations in New York in 2022',
    xaxis_title = 'Start stations',
    yaxis_title ='Number of trips',
    width = 900, height = 600)
st.plotly_chart(fig, use_container_width = True)


## Line chart 

fig_2 = make_subplots(specs=[[{"secondary_y": True}]])

# Daily bike rides (primary axis) 
fig_2.add_trace(
    go.Scatter(
        x=df_daily.index,
        y=df_daily['bike_rides_daily'],
        name='Daily Bike Trips',
        mode='lines',
        line=dict(color="#1f3b73", width=2)),
    secondary_y=False)

# Daily temperature (secondary axis)
fig_2.add_trace(
    go.Scatter(
        x=df_daily.index,
        y=df_daily['avgTemp'],
        name='Daily Temperature',
        mode='lines',
        line=dict(color="#2ca6a4", width=2)),
    secondary_y=True)

# Layout 
fig_2.update_layout(
    title="Daily Bike Trips and Average Temperature (New York, 2022)",
    template="plotly_white",
    height=500,
    width=900,
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5))

# Show only month names
fig_2.update_xaxes(
    title_text="Date",
    dtick="M1",
    tickformat="%b")

# Color the y-axis labels + add padding
fig_2.update_yaxes(
    title_text="Daily Bike Trips",
    title_font=dict(color="#1f3b73"),
    tickfont=dict(color="#1f3b73"),
    secondary_y=False,
    range=[
        df_daily['bike_rides_daily'].min() * 0.9,
        df_daily['bike_rides_daily'].max() * 1.05])

fig_2.update_yaxes(
    title_text="Average Temperature (°C)",
    title_font=dict(color="#2ca6a4"),
    tickfont=dict(color="#2ca6a4"),
    secondary_y=True,
    range=[
        df_daily['avgTemp'].min() - 2,
        df_daily['avgTemp'].max() + 2])

st.plotly_chart(fig_2, use_container_width=True)


## Add the Kepler map (HTML)

path_to_html = r"C:\Users\ZenBook\NY_2022_CityBike_Map.html"

# Read file and keep in variable 
with open(path_to_html, 'r') as f:
    html_data = f.read()

# Show in web page 
st.markdown(
    "<h3 style='font-size:17px;'><b>Aggregated CitiBike Trips in New York</b></h3>", unsafe_allow_html=True)

st.components.v1.html(html_data,height = 900, scrolling=True)
