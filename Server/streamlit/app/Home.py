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
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import requests

st.set_page_config(page_title="Water Data",
                    page_icon=":bar_chart:",
                    layout="wide")

# ---- DATABASE ----
MONGODB_CONN = "mongodb://TGR_GROUP30:NJ485O@mongoDB:27017"
@st.cache_resource
def init_conn():
    return pymongo.MongoClient(MONGODB_CONN)

mongo_client = init_conn()

data = list()
pd_data = list()

df = pd.DataFrame()
pd_df = pd.DataFrame()

# @st.cache_data(ttl=300)
def get_water_data() -> list:
    global data, df, pd_data, pd_df
    data = list(mongo_client["TGR2023"]["water_data"].find())
    pd_data = list(mongo_client["TGR2023"]["predict_water_data"].find())

    df = pd.DataFrame(data)
    pd_df = pd.DataFrame(pd_data)

get_water_data()
# ---- DATABASE ----
col000, col001, col002 = st.columns([4,8,4])
with col000:
    st.title("")
with col001:
    st.image("SEE-IT.png", use_column_width=True)
with col002:
    st.title("")
st.write("<center><h1>ระบบแจ้งเตือนภัยพิบัติ</h1></center>", unsafe_allow_html=True)
col00, col01, col02 = st.columns([4,8,4])
with col00:
    st.title("")
with col01:
    bt = st.button("[Hardware] Detect Current Water Level", use_container_width=True)
    if bt:
        try:
            r = requests.get("http://192.168.1.98/mqtt/command")
            st.toast("ส่งคำสั่งให้ Hardware แล้ว")
            st.balloons()
        except:
            st.toast("ส่งคำสั่งไม่สำเร็จ")
            st.snow()
with col02:
    st.title("")

selectable_list = df["name"].unique().tolist() if "name" in df.columns else ["- ไม่มีข้อมูล -"]
station = st.selectbox(label="สถานีตรวจวัดระดับน้ำ",
    options=selectable_list,index=0,
    key="aaa"
)

st.sidebar.image("TESA.png", use_column_width=True)
st.sidebar.image("SEE-IT_BG.png", use_column_width=True)
st.sidebar.image("Embed.png", use_column_width=True)


cont,cont2,cont3 = st.empty(), st.empty(), st.empty()
# cont4 = st.empty()

while True:
    get_water_data()
    if (station != "แสดงทั้งหมด" and station != "- ไม่มีข้อมูล -"):
        df = df.query(
            "name == @station"
        )
        if not pd_df.empty:
            pd_df = pd_df.query(
                "name == @station"
            )
    selectable_list = df["name"].unique().tolist() if "name" in df.columns else ["- ไม่มีข้อมูล -"]
    with cont.container():
        dfm = df.values.tolist()
        st.subheader("ข้อมูลระดับน้ำล่าสุด")
        col1, col2, col3 = st.columns(3)
        if not len(dfm):
            with col1:
                st.metric("ระดับน้ำ", value="- เมตร", delta="-")
            with col2:
                st.metric("อัตราการไหล", value="- ลบ.ม./วิ", delta="-")
            with col3:
                st.metric("อัปเดตล่าสุด", value="----/--/-- --:--")
            # with cont4.container():
            #     st.warning('ไม่พบข้อมูลใน Database, โปรดเพิ่มข้อมูลน้ำใน Database `water_data` ก่อน')
        else:
            latest = dfm[-1]
            pre_latest = (dfm[-2] if len(dfm) > 1 else {3: 0, 4: 0, 5: 0})
            with col1:
                level_key = 3 #"height"
                level_delta = latest[level_key]-pre_latest[level_key]
                latest_level = latest[level_key]
                st.metric("ระดับน้ำ", value=f"{latest_level:.2f} เมตร", delta=f"{level_delta:.2f} เมตร")
            with col2:
                discharge_key = 4 #"discharge_rate"
                discharge_delta = latest[discharge_key]-pre_latest[discharge_key]
                latest_discharge = latest[discharge_key]
                st.metric("อัตราการไหล", value=f"{latest_discharge:.2f} ลบ.ม./วิ", delta=f"{discharge_delta:.2f} เมตร")
            with col3:
                time_key = 5 #"time"
                dateandtime = datetime.utcfromtimestamp(latest[time_key]) + timedelta(hours=7)
                st.metric("อัปเดตล่าสุด", value=f"{dateandtime.strftime('%Y/%m/%d %H:%M')}")
    with cont2.container():
        if len(dfm):
            # st.write("<hr>", unsafe_allow_html=True)
            st.subheader("สถานการณ์น้ำ")
            col11, col12 = st.columns(2)
            with col11:
                st.metric("ระดับความสูงน้ำเฉลี่ย", value=f"{df['height'].mean():.2f} เมตร")
            with col12:
                st.metric("อัตราการไหลของน้ำเฉลี่ย", value=f"{df['discharge_rate'].mean():.2f} ลบ.ม./วิ")
            b_df = df
            b_pd_df = pd_df
            b_df["Flag"] = "Actual"
            b_pd_df["Flag"] = "Forecast"

            ndf = pd.concat([b_df, b_pd_df])
            fig = px.line(ndf, x="day", y="height", color="Flag", color_discrete_map={'Actual': 'blue', 'Forecast': 'lightblue'}, line_dash_map={'Actual': 'none', 'Forecast': 'dash'})

            st.plotly_chart(fig, use_container_width=True)

            ddd = df.copy()
            ddd.drop(columns=["_id", "time", "Flag"], inplace=True)
            ddd.rename(columns={"height": "ระดับน้ำ (ม.)", "discharge_rate": "อัตราการไหล (ลบ.ม./วิ)", "day": "วันที่", "name":"สถานี"}, inplace=True)
            ddd.set_index("วันที่", inplace=True)


            nddd = pd.DataFrame({
                "วันที่": df["day"],
                "สถานี": df["name"],
                "ระดับน้ำ (ม.)": df["height"],
                "ส่วนต่างระดับน้ำ": df["height"].diff().apply(
                    lambda x: '🔺 เพิ่มขึ้น' if x > 0 else ('🟢 ลดลง' if x < 0 else '🔸 คงที่')
                ),
                "อัตราการไหล (ลบ.ม./วิ)": df["discharge_rate"],
                "ส่วนต่างอัตราการไหล": df["discharge_rate"].diff().apply(
                    lambda x: '🔺 เพิ่มขึ้น' if x > 0 else ('🟢 ลดลง' if x < 0 else '🔸 คงที่')
                ),
            })
            nddd.set_index("วันที่", inplace=True)
            st.dataframe(nddd.sort_values(by=['วันที่'], ascending=False), use_container_width=True, height=500)
    time.sleep(1)
