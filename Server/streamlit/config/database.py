import streamlit as st
import pymongo

# ---- DATABASE ----
MONGODB_CONN = "mongodb://TGR_GROUP30:NJ485O@mongoDB:27017"
@st.cache_resource
def init_conn():
    return pymongo.MongoClient(MONGODB_CONN)

mongo_client = init_conn()

@st.cache_data(ttl=300)
def get_data() -> list:
    return list(mongo_client["mockupdata"]["waterdata"].find())

def get_data_realtime() -> list:
    return list(mongo_client["mockupdata"]["waterdata"].find())
# ---- DATABASE ----

