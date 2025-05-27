import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from streamlit_cookies_controller import CookieController
import json


st.title("Cinema Sénéchal")

# **************Initialization cookies et fonctions ************************

query_params = st.query_params


def initialize():
    return pd.read_parquet("data/app_df.gzip")


cookie_manager = CookieController()

liked_cookie = cookie_manager.get("liked_movies")
if liked_cookie:
    liked_movies = json.loads(liked_cookie)
else:
    liked_movies = set()

if "df" not in st.session_state:
    df = initialize()
    st.session_state["df"] = df
else:
    df = st.session_state["df"]

st.dataframe(df)
