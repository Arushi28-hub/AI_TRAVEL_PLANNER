import streamlit as st
import pandas as pd
import os
import folium
import streamlit.components.v1 as components

from recommender import (
    recommend_trip,
    recommend_by_preferences
)

from trip_planner import (
    plan_trip,
    trip_summary,
    get_attractions_list
)

from itinerary_generator import (
    create_prompt,
    generate_itinerary
)

from geocode_utils import geocode_df_locations

st.set_page_config(
    page_title="Itinera - AI Travel Planner",
    page_icon="🌍",
    layout="wide"
)

# -----------------------
# Load Dataset
# -----------------------

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(_BASE_DIR, "data", "processed_travel_dataset.csv"))

# -----------------------
# Header
# -----------------------

st.title("🌍 Itinera")
st.subheader("AI Powered Travel Planner for Students")

st.markdown("---")

# -----------------------
# Sidebar
# -----------------------

st.sidebar.header("Trip Preferences")

city = st.sidebar.selectbox(
    "Select City",
    sorted(df["City"].unique())
)

interest = st.sidebar.selectbox(
    "Interest",
    [
        "Historical",
        "Religious",
        "Nature",
        "Adventure",
        "Wildlife",
        "Beach",
        "Museum"
    ]
)

budget = st.sidebar.slider(
    "Budget (₹)",
    1000,
    20000,
    5000,
    step=500
)

days = st.sidebar.slider(
    "Number of Days",
    1,
    7,
    2
)

st.sidebar.markdown("---")

generate = st.sidebar.button(
    "Generate Trip Plan"
)

# -----------------------
# Main
# -----------------------

if generate:

    st.header("Recommended Attractions")

    trip = plan_trip(
        interest=interest,
        budget=budget,
        days=days,
        city=city
    )

    if trip.empty:

        st.warning(
            "No attractions found."
        )

        st.stop()

    st.dataframe(
        trip[
            [
                "Name",
                "Type",
                "City",
                "Entrance Fee in INR",
                "Student Score"
            ]
        ],
        use_container_width=True
    )

    st.markdown("---")

    summary = trip_summary(
        trip,
        budget,
        days
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Places",
        summary["Attractions Selected"]
    )

    c2.metric(
        "Entry Fee",
        f"₹{summary['Entry Fees']}"
    )

    c3.metric(
        "Estimated Cost",
        f"₹{summary['Estimated Total Cost']}"
    )

    c4.metric(
        "Budget Left",
        f"₹{summary['Remaining Budget']}"
    )

    st.markdown("---")

    attractions = get_attractions_list(trip)

    # Map of selected attractions (geocoded)
    st.header("Map of Selected Attractions")

    with st.spinner("Geocoding attractions and creating map..."):
        geo_df = geocode_df_locations(trip[["Name", "City", "Type"]])

    if geo_df is None or geo_df.empty:
        st.info("No coordinates available to render map.")
    else:
        # center map on mean coordinates
        lat_mean = geo_df["latitude"].dropna().mean()
        lon_mean = geo_df["longitude"].dropna().mean()

        if pd.isna(lat_mean) or pd.isna(lon_mean):
            st.info("No valid coordinates found for the selected attractions.")
        else:
            m = folium.Map(location=[lat_mean, lon_mean], zoom_start=12)

            for _, row in geo_df.iterrows():
                if pd.isna(row.get("latitude")) or pd.isna(row.get("longitude")):
                    continue
                popup = f"{row['Name']} ({row.get('Type','')})"
                folium.Marker([row['latitude'], row['longitude']], popup=popup).add_to(m)

            components.html(m._repr_html_(), height=500)

    st.header("AI Generated Itinerary")

    prompt = create_prompt(
        budget=budget,
        days=days,
        interest=interest,
        city=city,
        attractions=attractions
    )

    with st.spinner("Creating itinerary using Gemini AI..."):

        itinerary = generate_itinerary(prompt)
        st.success("Your itinerary is ready!")

    st.markdown(itinerary)

    st.download_button(
        label="📥 Download Itinerary",
        data=itinerary,
        file_name="AI_Itinerary.txt",
        mime="text/plain"
    )

    st.markdown("---")

    

    st.markdown("---")

    st.header("Recommendation by Preferences")

    recommendation = recommend_by_preferences(
        attraction_type=None,
        budget="Low"
    )

    st.dataframe(
        recommendation[
            [
                "Name",
                "Type",
                "City",
                "Student Score"
            ]
        ],
        use_container_width=True
    )

    st.markdown("---")

    st.header("Top Attractions Based on Interest")

    top_places = recommend_trip(
        interest
    )

    st.dataframe(
        top_places,
        use_container_width=True
    )

st.markdown("---")

st.caption(
    "Made with ❤️ using Streamlit, Scikit-Learn and Google Gemini"
)