from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import streamlit
import plotly.express as px
import pymongo
import time
st.set_page_config(page_title="TGR Group 30 - See-It 2023",
                    page_icon=":bar_chart:",
                    layout="wide")

st.title("TGR Group 30 - See-It 2023")
st.subheader("Member")
st.write("""
- Palapon Soontornpas
- Peeraphol Sudphutong
- Metee Yingyongwattanakit
- Peepat Khantaracha
- Amonrit Tungruedee
        """)

st.sidebar.image("TESA.png", use_column_width=True)
st.sidebar.image("SEE-IT_BG.png", use_column_width=True)

while True:
    st.balloons()
    time.sleep(3)