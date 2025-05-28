# ***************Imports***********************

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from streamlit_cookies_controller import CookieController
import json

# **************Initialization cookies et fonctions ************************

query_params = st.query_params


def initialize():
    return pd.read_parquet("data/app_df.gzip")


cookie_manager = CookieController()

liked_cookie = cookie_manager.get("liked_movies")
if liked_cookie:
    if isinstance(liked_cookie, str):
        liked_movies = [liked_cookie]
    else:
        liked_movies = liked_cookie
else:
    liked_movies = []

if "df" not in st.session_state:
    df = initialize()
    st.session_state["df"] = df
else:
    df = st.session_state["df"]

# **************titres*********************
st.title("Nos recommandations pour vous")
