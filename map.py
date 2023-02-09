import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px

# Read the data
eco_footprints = pd.read_csv("footprint_clean.csv")

max_eco_footprint = eco_footprints["Ecological footprint"].max()

political_countries_url = (
    "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson")


# Streamlit part

st.set_page_config(layout="centered", page_title="Streamlit / Folium Example")
st.write("## :green[Ecological Footprint] per Country Per Capita")

st.sidebar.write("## This is a Work in Progress :wrench:") # Sidebar title
st.sidebar.write("Drag and zoom in/out the image to change the map view.") # Sidebar text
br() # Line break
st.sidebar.write("Note that this list contains only 188 countries, covering most of the countries with more than one million inhabitants.") # Sidebar text


# Create a folium map

m = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron", use_container_width=True)
folium.Choropleth(
    geo_data=
    political_countries_url,  # geo_data takes a path to the GeoJSON geometries
    data=eco_footprints,  # data takes a pandas DataFrame
    columns=["Country/region", "Ecological footprint"],
    key_on=
    "feature.properties.name",  # key_on takes the name of the property in the GeoJSON file that contains the country name
    bins=[
        0, 1, 1.5, 2, 3, 4, 5, 6, 7, 8, max_eco_footprint
    ],  # bins takes a list of values that will be used to divide the data into intervals
    fill_color="RdYlGn_r",
    fill_opacity=0.8,
    line_opacity=0.3,
    nan_fill_color="white",
    legend_name="Ecological footprint per capita",
    name="Countries by ecological footprint per capita",
).add_to(m)
folium.LayerControl().add_to(m)  # Add a layer control to the map

st_data = st_folium(m, width=700)
st.caption('Source: [Wikipedia](https://en.wikipedia.org/wiki/List_of_countries_by_ecological_footprint)')




# FOOTER
# Footer
def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
    </style>
    """

    style_div = styles(
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        text_align="center",
        # height="60px",
        # opacity=0.6
    )

    style_hr = styles(
    )

    body = p()
    foot = div(style=style_div)(hr(style=style_hr), body)

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)
        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        "<b>Made with ❤️ by</b> ",
        link("https://www.arkhad.com/", " xJuggl3r"),

        " using Python ",
        link("https://www.python.org/", image('https://i.imgur.com/ml09ccU.png',
                                              width=px(18), height=px(18), margin="0em")),
        ", Streamlit ",
        link("https://streamlit.io/", image('https://streamlit.io/images/brand/streamlit-mark-color.svg',
                                            width=px(24), height=px(25), margin="0em")),
        
        " and Folium",
        link("https://python-visualization.github.io/folium/", image('https://objectstorage.sa-saopaulo-1.oraclecloud.com/p/-r_mKAXilWI8gDoNF56tYrBZRTrb9o2mEAHfxEzb5KPE5zqAakvfA4IJa-rwhYwQ/n/gr6gnqikyfe4/b/geral/o/folium_logo.png',
                                            width=px(24), height=px(25), margin="0em")),
        
        ". A 👏 to ", link("https://github.com/randyzwitch/streamlit-folium", "streamlit-folium."),
    ]
    layout(*myargs)


if __name__ == "__main__":
    footer()

