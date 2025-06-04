# ***************Imports***********************

import streamlit as st
import pandas as pd
from streamlit_cookies_controller import CookieController

# **************Initialization cookies et fonctions ************************

query_params = st.query_params


def initialize():
    return pd.read_parquet("data/df_similar.gzip")


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

current_view = "Favoris"

page_key = f"{current_view}_page"

# ****************Movie details*****************************

if query_params.get("page") == "detail":
    st.title("Details")
    cookie_manager.set("liked_movies", liked_movies)
    tconst = query_params.get("tconst")
    info_film = df[df["tconst"] == tconst].reset_index().squeeze()

    recomended_df = df.loc[info_film["similar_films"]]
    col1, col2 = st.columns(2)
    with col1:
        st.image(f"https://image.tmdb.org/t/p/w342/{info_film['Poster']}")

        liked = tconst in liked_movies
        like_text = "Eliminer des favoris 💔" if liked else "Ajouter à mes favoris ❤️"
        if st.button(like_text, use_container_width=True):
            if liked:
                liked_movies.remove(tconst)
            else:
                liked_movies.append(tconst)
            st.rerun()
    with col2:
        st.markdown(f"**Titre :** {info_film['Title']}")
        st.markdown(f"**Realisateur :** {info_film['Director']}")
        st.markdown(f"**Note :** {info_film['Rating']}")
        st.markdown(f"**Année :** {info_film['Year']}")
        st.write(f"{info_film['Resume']}")
        st.markdown(f"**Genres :** {info_film['Genres']}")
        st.markdown(f"**Acteurs :** {info_film['Actors']}")
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("⬅️ Retour", use_container_width=True):
            st.query_params.clear()
            st.rerun()
    st.header("Films similaires", divider="gray")
    images_per_row = 5
    for i in range(0, len(recomended_df), images_per_row):
        cols = st.columns(images_per_row)
        for idx, row in enumerate(
            recomended_df.iloc[i : i + images_per_row].itertuples()
        ):
            with cols[idx]:
                st.image(f"https://image.tmdb.org/t/p/w185/{row.Poster}")
                if st.button(row.Title, key=row.tconst, use_container_width=True):
                    st.query_params.update({"page": "detail", "tconst": row.tconst})
                    st.rerun()
    st.stop()

# **************Title***************


if liked_movies:
    df_liked_movies = df[df["tconst"].isin(liked_movies)]
    st.title("Vos favoris")
else:
    st.title("Vous n'avez pas encore de favoris")
    st.stop()
# ******************Filters***************************

if "prev_title" not in st.session_state:
    st.session_state["prev_title"] = ""

if "prev_genre" not in st.session_state:
    st.session_state["prev_genre"] = []

# ***********Titre*******************

search = st.text_input(
    "Titre",
    placeholder="Indiquez un titre de film ou le nom d'un acteur",
    label_visibility="hidden",
)

if search != st.session_state["prev_title"]:
    st.session_state[page_key] = 1
    st.session_state["prev_title"] = search

# **************Genre***************

genre_series = df_liked_movies["Genres"].str.split(",")
genre_list = [genre for sublist in genre_series for genre in sublist]
genre_list = list(filter(lambda x: x not in ["\\N", "Adult"], genre_list))
genre_list = pd.Series(genre_list)

genre = st.multiselect(
    "Genre",
    options=genre_list.unique(),
    placeholder="Choisissez un genre",
    label_visibility="hidden",
)

if genre != st.session_state["prev_genre"]:
    st.session_state[page_key] = 1
    st.session_state["prev_genre"] = genre

# **************Apply filters***************

if search:
    df_liked_movies = df_liked_movies[
        (df_liked_movies["Title"].str.contains(search, case=False))
        | (df_liked_movies["Actors"].str.contains(search, case=False))
    ]

if genre:
    for g in genre:
        df_liked_movies = df_liked_movies[
            df_liked_movies["Genres"].str.contains(g, case=False)
        ]

# **************Pagination setup*********************

items_per_page = 30

total_pages = (len(df_liked_movies) - 1) // items_per_page + 1

if "last_view" not in st.session_state:
    st.session_state["last_view"] = current_view


if page_key not in st.session_state:
    st.session_state[page_key] = 1


if "last_view" not in st.session_state:
    st.session_state["last_view"] = current_view
elif st.session_state["last_view"] != current_view:
    st.session_state[f"{st.session_state['last_view']}_page"] = 1
    st.session_state["last_view"] = current_view
# **************Pagination buttons*********************

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if (
        st.button("⬅️ Avant", use_container_width=True)
        and st.session_state[page_key] > 1
    ):
        st.session_state[page_key] -= 1
with col5:
    if (
        st.button("Suivant ➡️", use_container_width=True)
        and st.session_state[page_key] < total_pages
    ):
        st.session_state[page_key] += 1

with col3:
    st.markdown(
        f"<div style='text-align: center;'>Page {st.session_state[page_key]} sur {total_pages}</div>",
        unsafe_allow_html=True,
    )

# **************Images*********************************

current_page = st.session_state[page_key]
start_idx = (current_page - 1) * items_per_page
end_idx = start_idx + items_per_page
page_df = df_liked_movies.iloc[start_idx:end_idx]
images_per_row = 5

for i in range(0, len(page_df), images_per_row):
    cols = st.columns(images_per_row)
    for idx, row in enumerate(page_df[i : i + images_per_row].itertuples()):
        with cols[idx]:
            st.image(f"https://image.tmdb.org/t/p/w185/{row.Poster}")
            if st.button(row.Title, key=row.tconst, use_container_width=True):
                st.query_params.update({"page": "detail", "tconst": row.tconst})
                st.rerun()
