import streamlit as st
import pandas as pd
from PIL import Image
import hashlib
import folium
from streamlit_folium import st_folium
@st.cache_data
# Function to hash passwords
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# Function to check hashed passwords
def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

# Function to create user table if not exists
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

# Function to load reservoir data
@st.cache_data
def load_data():
    data = {
        'Reservoir': ['Siruvani', 'Pillur',"Bhavanisagar",'Amaravathi','Malampuzha Dam'],
        'LAT': [10.9702, 11.2567,11.4459,10.4039,10.8306],
        'LNG': [76.6478, 76.8022,77.0737,77.2621,76.6838]
    }
    return pd.DataFrame(data)

# Function to draw Folium map
def draw_folium_map(df_reservoirs):
    map_center = [df_reservoirs['LAT'].mean(), df_reservoirs['LNG'].mean()]
    reservoirs_map = folium.Map(location=map_center, zoom_start=12, control_scale=True, tiles='openstreetmap')

    for index, reservoir_info in df_reservoirs.iterrows():
        folium.Marker([reservoir_info['LAT'], reservoir_info['LNG']],
                      popup=reservoir_info['Reservoir'],
                      icon=folium.Icon(color='blue')).add_to(reservoirs_map)

    bounds = [[df_reservoirs['LAT'].min(), df_reservoirs['LNG'].min()],
              [df_reservoirs['LAT'].max(), df_reservoirs['LNG'].max()]]
    reservoirs_map.fit_bounds(bounds)

    return reservoirs_map

# Function to add user data to the database


# Main function
def main():
    st.markdown("<h1 style='text-align: center; color: lightblue;'>Aqua Insight - Water Supply Network</h1>", unsafe_allow_html=True)
    menu = ["HOME","GIS MAPPING","STATISTICAL REPORT","ABOUT US"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "HOME":
        st.markdown("<h1 style='text-align: center;'>HOMEPAGE</h1>", unsafe_allow_html=True)
        image = Image.open(r"image.jpg")
        st.image(image, caption='', use_column_width=True)
        st.subheader(" ")
        st.write("<p style='text-align: center;'> AquaInsight is an advanced GIS tool for mapping, monitoring, and managing Coimbatore's water supply. It integrates IoT sensors, real-time monitoring, and user-friendly interfaces.", unsafe_allow_html=True)
        st.warning("Go to the Menu Section To Know More!")

    elif choice == "ABOUT US":
        st.header("CREATED BY _**TEAM STARK MATRIX**_")

    elif choice == "GIS MAPPING":
        st.title('Coimbatore Water Supply Network')

        # Display the image using st.image
        st.subheader('Map of Coimbatore City')
        image = st.image("coimbatore-corporation-ward-map-scaled.jpg", use_column_width=True)

        st.subheader('Map of Coimbatore Water Reservoirs')

        # Load Data into a DataFrame
        df_reservoirs = load_data()

        # Draw the Folium Map
        reservoirs_map = draw_folium_map(df_reservoirs)

        # Display the map in Streamlit
        st_folium(reservoirs_map, width=800, height=600)
        
        st.subheader('Map of Coimbatore City Water Supply Pipelines')
        map_iframe = '<iframe src="https://www.google.com/maps/d/embed?mid=1ERWmdpAQf9v8vIQS1ylflyU9Oj6NuF4&ehbc=2E312F" width="700" height="600"></iframe>'
        # Embed the Google Maps iframe in the Streamlit app
        st.markdown(map_iframe, unsafe_allow_html=True)

    elif choice == "STATISTICAL REPORT":
        print()


if __name__ == '__main__':
    main()
