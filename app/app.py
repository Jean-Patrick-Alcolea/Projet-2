# ***************Imports***********************

import streamlit as st
import pandas as pd
import duckdb as db

# ***************Page Config*******************

accueil = st.Page(page="views/Accueil.py", title="Accueil", icon="🏠", default=True)

recom = st.Page(
    page="views/Recommandations.py", title="Recommandations de films", icon="🎬"
)

exp = st.Page(page="views/Explore.py", title="Trouver des films", icon="🎥")

fav = st.Page(page="views/Favoris.py", title="Vos films favoris", icon="❤️")

# ***************Navigation setup***************

pg = st.navigation(pages=[accueil, exp, recom, fav])

pg.run()
