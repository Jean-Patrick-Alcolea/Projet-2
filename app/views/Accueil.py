import streamlit as st
import pandas as pd

st.title("Cinema Sénéchal")


def initialize():
    return pd.read_parquet("data/app_df.gzip")


if "df" not in st.session_state:
    df = initialize()
    st.session_state["df"] = df
else:
    df = st.session_state["df"]

st.dataframe(df)
