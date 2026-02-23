################################# NEW YORK CITI BIKE DASHBOARD ####################################

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import plotly.io as pio
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from PIL import Image
from numerize.numerize import numerize
import warnings
warnings.filterwarnings('ignore')


# ───────────────────────────────────────────────────────────────────
# INITIAL SETTINGS
# ───────────────────────────────────────────────────────────────────

st.set_page_config(page_title="New York Citi Bike Strategy Dashboard", layout="wide")
st.title("New York Citi Bike Strategy Dashboard")

# Define side bar

st.sidebar.title("STRUCTURE")

page = st.sidebar.selectbox('Select part of analysis',
    ["Intro page",
     "Most popular Citi Bike stations",
     "Weather component and bike usage", 
     "Interactive map with aggregation", 
     "Recommendations"])


# ────────────────────────────────────────────────────────────────────
# DATA IMPORT
# ────────────────────────────────────────────────────────────────────

top15 = pd.read_csv('top15_start_NY_2022.csv', index_col = 0)
df_1 = pd.read_csv('df_1_reduced_data.csv.gz', index_col = 0)
df_daily = pd.read_csv('df_daily_trips_temp.csv', index_col = 0)


# ────────────────────────────────────────────────────────────────────
# DEFINE THE PAGES
# ────────────────────────────────────────────────────────────────────

################################# Intro page ######################################

if page == "Intro page":
    st.write("")
    
    myImage = Image.open("CitiBike_pic_6.png")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
         st.image(myImage, width=300)
    
    st.write("")
        
    st.markdown(
        "#### Dashboard explores CitiBike’s company usage patterns in 2022 to reveal when and where "    
        "imbalances occur, helping identify opportunities to improve distribution efficiency and" 
        "enhance the overall rider experience."
)
    
    st.markdown(
        "##### Who is Citi Bike?"
)
        
    st.markdown(
    "**Citi Bike** - New York City's flagship bike-sharing program, offering residents and visitors "
    "a fast, sustainable alternative to traditional transportation. **Since its launch in 2013**, "
    "the system has expanded into one of the largest in the world, serving Manhattan, Brooklyn, "
    "Queens, and parts of the Bronx with thousands of bikes and docking stations. **As ridership "
    "continues to grow, so do the operational challenges—stations frequently run empty in high-demand "
    "areas while others remain full, limiting users ability to pick up or return bikes**."
)
    st.write("")

    myImage1 = Image.open("CitiBike_pic_1.jpg")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(myImage1, width=1000)

    st.write("")
    
    st.markdown(
    "The **purpose** of this project is to pinpoint the operational bottlenecks that lead to bike shortages "
    "and station imbalances, helping decision-makers quickly identify distribution bottlenecks and guide "
    "strategic improvements to bike availability across New York City."
)

    st.write("")

    st.markdown(" ##### Dashboard consist next **sections**:")
    st.markdown("**- Most popular stations**")
    st.markdown("**- Weather component and bike usage**")
    st.markdown("**- Interactive map with aggregated bike trips**")
    st.markdown("**- Recommendations**")

    myImage2 = Image.open("CitiBike_pic_2.jpg")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(myImage2, width=1000)

    st.markdown("For analysis were used the Citi Bike database for 2022 (https://s3.amazonaws.com/tripdata/index.html) and NOAA’s weather data (https://www.noaa.gov/).")



######################### Most popular bike stations page ############################ 

elif page == 'Most popular Citi Bike stations':

    st.header("Most popular Citi Bike start stations in 2022")

    st.write("")
    
    # Create the Season filter on the side bar
    with st.sidebar:
        season_filter = st.multiselect(
            label='**Select the season**',
            options=df_daily['Season'].unique(),
            default=df_daily['Season'].unique()
        )
        df1 = df_daily.query('Season == @season_filter')

    # Define the total rides - Total Rides Icon
    total_rides = float(df1['bike_rides_daily'].sum())

    # Convert to millions with two decimals and comma separator
    value_season = f"{total_rides / 1_000_000:.2f}M".replace('.', ',')

    # Create the month filter on the side bar
    with st.sidebar:
        month_filter = st.multiselect(
            label='**Select the month**',
            options=df_daily['month'].unique(),
            default=df_daily['month'].unique()
        )
        df1 = df_daily.query('month == @month_filter')

    # Define the total rides - Total Rides Icon
    total_rides = float(df1['bike_rides_daily'].sum())

    # Convert to millions with two decimals and comma separator
    value_month = f"{total_rides / 1_000_000:.2f}M".replace('.', ',')

    # create two horizontal columns to hold metrics for Season and month
    col1, col2, col_space = st.columns([1, 1, 1])
    
    with col1:
        st.metric(label='**Total Bike Trips per season**', value=value_season)
        
        with col2:
            st.metric(label='**Total Bike Trips per month**', value=value_month)


    # Bar chart
    fig = go.Figure(go.Bar(
        x=top15['start_station_name'],
        y=top15['value'],
        marker={'color': top15['value'], 'colorscale': 'gnbu'}))
    fig.update_layout(
        title='Top 15 Citi Bike most popular start stations in New York in 2022',
        xaxis_title='Start stations',
        yaxis_title='Number of trips',
        width=900,
        height=600)
    
    st.plotly_chart(fig, use_container_width=True)

    # Insights
    st.markdown(
    """The bar chart highlights the start stations with the highest bike‑trip volumes, showing a strong concentration of activity at a small number of central locations.

**Most popular starting points** in NY in 2022 — **W 21 St & 6 Ave**, **1 Ave & E 68 St**,**Broadway & W 58 St**, and **West St & Chambers St** — stand out clearly (marked by blue color), with significantly taller bars than the rest.

This contrast underscores how heavily riders rely on a few key departure stations, particularly in **central Manhattan, where these stations consistently generate the highest volumes of Citi Bike trips**.

To further explore these patterns, please use the interactive map available through the sidebar selection box.
"""
)

    
############################ Dual-axis line chart page ############################### 

elif page == 'Weather component and bike usage':

    st.header("Weather component and bike usage")
    
    # Line chart
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
        title="Daily Bike Trips and Average Temperature in New York in 2022",
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
        title_text="Month",
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

    # Insights
    st.markdown(
    """
This dual-axis line chart demonstrates a strong, temperature‑driven pattern in bike usage: **as temperatures rise, daily ridership increases**, and **as temperatures fall, usage drops sharply**.

This indicates that **Citi Bike shortages are primarily a warm‑season issue**, concentrated between **May and October**.

Across many cities — and reflected in this dataset — summer ridership reaches peak levels (around 100%), while winter usage typically falls to **30–50%** of that peak, depending on weather conditions and holiday periods.
"""
)


############################### Interactive (Kepler) map page ################################# 

elif page == 'Interactive map with aggregation':

    st.header("Interactive map with aggregated bike trips")

    # Add the Kepler map (HTML)
    path_to_html = r"C:\Users\ZenBook\NY_2022_CityBike_Map.html"

    # Read file and keep in variable
    with open(path_to_html, 'r') as f:
        html_data = f.read()

    # Show in web page
    st.markdown(
        "<h3 style='font-size:17px;'><b>CitiBike Trips in New York in 2022</b></h3>",
        unsafe_allow_html=True)

    st.components.v1.html(html_data, height=900, scrolling=True)

    # Insights

    st.markdown(
        "The Kepler map visualizes Citi Bike "
        "start stations (depickted as green dots), and end stations (blue dots). "
        "Connection color intensity reflects route popularity: brighter (yellow) indicate more trips, "
        "while darker (violet) represents fewer trips."
    )

    st.write("")
    
    st.markdown(
        "#### By using the filter on the left-hand side of the map, you can check whether the most popular start stations "
        "also appear in the most frequently traveled routes. Map demonstrate that:"
    )

    st.write("")
    
    st.markdown("**- The densest clusters appear in Midtown and Lower Manhattan, driven by commuter flows and tourism.**")
    st.markdown("**- Strong recreational patterns are visible around Central Park and the Hudson River Greenway.**")
    st.markdown("**- Route density drops sharply outside Manhattan due to lower station density and less bike infrastructure.**")
    st.markdown("**- Outer boroughs (Queens, Bronx, deeper Brooklyn) show far fewer connections.**")
    st.markdown("**- Jersey City and Roosevelt Island appear as small, isolated pockets of activity.**")
    st.markdown("**- Overall, the map shows that Citi Bike demand is highly concentrated in Manhattan’s core, with short, repetitive, high‑volume trips.**")
    st.markdown("**- These patterns suggest that Citi Bike rebalancing and fleet distribution should prioritize central Manhattan and the highlighted corridors.**")


############################### Recommendations page #################################

else:

    st.header("Conclusion and Recommendations")

    myImage3 = Image.open("CitiBike_pic_4.jpg")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(myImage3, width=500)

    st.markdown("#### The analysis indicates that Citi Bike should prioritize the following strategic objectives moving forward:")

    st.markdown("##### 🚲 Increase docking capacity at top stations to reduce congestion and ensure bikes are consistently available.")

    st.markdown("##### 🔄 Implement dynamic bike rebalancing, especially during morning and evening peak hours when demand shifts rapidly.")

    st.markdown("##### ❄️ Adjust docking stations space seasonally — stations don’t need to be fully stocked during winter months.")

    st.markdown("##### 🌞 Plan for seasonal surges: waterfront and leisure‑area demand spikes in warm months, so use modular stations that can scale up for summer.")

    st.markdown("##### 📈 Stock bikes more heavily in warmer months to meet higher demand, and reduce supply in winter and late autumn to lower logistics costs.")

    st.markdown("##### 🚨 Use automated alerts to dispatch rebalancing crews when station levels cross critical thresholds.")
    
    myImage4 = Image.open("CitiBike_pic_5.png")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(myImage4, width=500)
