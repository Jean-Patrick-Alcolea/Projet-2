import streamlit as st
import pandas as pd
from streamlit_cookies_controller import CookieController


col1, col2, col3 = st.columns(3)
with col2:
    st.image("app/img/logo.png", width=300)
st.title("Creuse Toujours")

# **************Initialization cookies et fonctions ************************

query_params = st.query_params


def initialize():
    return pd.read_parquet("data/movie_df.gzip")


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

current_view = "Accueil"

page_key = f"{current_view}_page"


st.markdown(
    """
Cette application vous permet de découvrir des films similaires à ceux que vous aimez, d’explorer par titre ou par genre, et de sauvegarder vos coups de cœur.

### 🧭 Comment utiliser l'application :

#### 🎥 Trouver des films
- Recherchez un film ou un acteur dans la barre de recherche.
- Filtrez les films par **genre**.
- Cliquez sur un titre pour voir plus de **détails** et obtenir des **recommandations personnalisées** ainsi que les **"Ajouter à vos favoris ❤️"**.

#### 🎬 Recommandations des films
- Allez dans l’onglet **Recommandations** pour découvrir des suggestions basées sur vos films préférés.
            
#### ❤️ Vos films favoris
- Consultez tous les films que vous avez aimés.



---

### 🍪 Astuce :
Vos favoris sont enregistrés dans votre navigateur à l’aide de cookies. Ils seront disponibles à votre prochaine visite sur ce navigateur.

---
"""
)
