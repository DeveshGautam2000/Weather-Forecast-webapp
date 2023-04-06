import streamlit as st
import plotly.express as px
from backEnd import get_data

st.title("Weather Forecast for the Next Days")

place = st.text_input("Place: ")

days = st.slider("Forecast Days", min_value=1, max_value=5, 
                 help="Select the number of forecasted days")

option = st.selectbox("Select the data to view", 
                      ("Temperature", "Sky"))

if place:
    try:
        filtered_data = get_data(place, days)

        st.subheader(f"{option} for the next {days} days in {place}")

        if option == "Temperature":
            temperature = [dict["main"]["temp"]/10 for dict in filtered_data]
            dates = [dict["dt_txt"] for dict in filtered_data]
            figure = px.line(x=dates, y=temperature, labels={"x":"Dates", "y": "Temperatur (C)"} )
            st.plotly_chart(figure)

        if option == "Sky":
            images = {"Clear":"images/clear.png",
                        "Clouds":"images/cloud.png",
                        "Rain":"images/rain.png", 
                        "Snow":"images/snow.png"}
                
            sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
            images_path = [images[condition] for condition in sky_conditions]
            st.image(images_path, width=115)
    except KeyError:
        st.error('That Place does not exist.', icon="🚨")