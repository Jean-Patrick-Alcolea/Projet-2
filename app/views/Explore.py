# ***************Imports***********************

import streamlit as st
import pandas as pd

# *********Initialization dataframe************


def initialize():
    return pd.read_parquet("data/app_df.gzip")


if "df" not in st.session_state:
    df = initialize()
    st.session_state["df"] = df
else:
    df = st.session_state["df"]


st.title("Trouvez les films que vous aimez")

# ******************Filters***************************

# **************Title***************
if "prev_title" not in st.session_state:
    st.session_state["prev_title"] = ""

title = st.text_input("Titre", placeholder="Entrez un titre de film")

if title != st.session_state["prev_title"]:
    st.session_state["page"] = 1
    st.session_state["prev_title"] = title

# **************Genre***************
if "prev_genre" not in st.session_state:
    st.session_state["prev_genre"] = []

genre_series = df["Genres"].str.split(",")
genre_list = [genre for sublist in genre_series for genre in sublist]
genre_list = list(filter(lambda x: x not in ["\\N", "Adult"], genre_list))
genre_list = pd.Series(genre_list)

genre = st.multiselect(
    "Genre", options=genre_list.unique(), placeholder="Choisissez un genre"
)

if genre != st.session_state["prev_genre"]:
    st.session_state["page"] = 1
    st.session_state["prev_genre"] = genre


if genre:
    df = df[df["Genres"].str.contains(genre[0])]

# **************Apply filters***************

if title:
    df = df[df["Title"].str.contains(title, case=False)]

if genre:
    df = df[df["Genres"].str.contains(genre[0])]

# **************Pagination setup*********************

items_per_page = 30

total_pages = (len(df) - 1) // items_per_page + 1

if "page" not in st.session_state:
    st.session_state["page"] = 1

# **************Pagination buttons*********************

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("⬅️ Avant", use_container_width=True) and st.session_state["page"] > 1:
        st.session_state["page"] -= 1
with col5:
    if (
        st.button("Suivant ➡️", use_container_width=True)
        and st.session_state["page"] < total_pages
    ):
        st.session_state["page"] += 1

with col3:
    st.markdown(
        f"<div style='text-align: center;'>Page {st.session_state['page']} sur {total_pages}</div>",
        unsafe_allow_html=True,
    )

# **************Images*********************************

start_idx = (st.session_state.page - 1) * items_per_page
end_idx = start_idx + items_per_page
current_page_images = df.iloc[start_idx:end_idx]["Poster"]
images_per_row = 5
image_urls = [
    f"https://image.tmdb.org/t/p/w185/{image}" for image in current_page_images
]

for i in range(0, len(image_urls), images_per_row):
    cols = st.columns(images_per_row)
    for idx, image in enumerate(image_urls[i : i + images_per_row]):
        with cols[idx]:
            st.image(image)
            if st.button(
                f"{df[df['Poster'] == '/'+ image.split('/')[-1]]['Title'].iloc[0]}",
                key=f"{df[df['Poster'] == '/'+ image.split('/')[-1]]['tconst'].iloc[0]}",
                use_container_width=True,
            ):
                st.session_state["selected_movie"] = (
                    f"{df[df['Poster'] == '/'+ image.split('/')[-1]]['tconst'].iloc[0]}"
                )
# ****************Movie details*****************************
