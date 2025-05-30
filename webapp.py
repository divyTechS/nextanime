import streamlit as st
import pandas as pd
import pickle
import re

st.set_page_config(page_title="Anime Recommender", layout="centered")

# Load data
@st.cache_data
def load_data():
    with open("anime_data.pkl", "rb") as f:
        anime_df = pickle.load(f)
    with open("anime_similarity.pkl", "rb") as f:
        similarity = pickle.load(f)
    return anime_df, similarity

anime_df, similarity = load_data()

def truncate_description(text, max_len=300):
    if len(text) <= max_len:
        return text
    truncated = text[:max_len]
    last_period = truncated.rfind('.')
    return truncated[:last_period + 1] if last_period != -1 else truncated + "..."

def recommend_anime(title, top_n=5):
    title = title.lower()
    matches = anime_df[anime_df['title'].str.lower() == title]
    if matches.empty:
        st.error("Anime not found.")
        return []
    idx = matches.index[0]
    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    recommendations = []
    for i, score in sim_scores:
        row = anime_df.loc[i]
        recommendations.append({
            "title": row["title"],
            "cover": row["cover_image"],
            "genres": row["genres"],
            "score": row["average_score"],
            "description": row["description"],
            "anilist_url": row["anilist_url"]
        })
    return recommendations

# Modern responsive and theme-aware CSS
st.markdown("""
<style>
html, body, [class*="css"]  {
    font-family: 'Segoe UI', sans-serif;
    scroll-behavior: smooth;
}
[data-testid="stAppViewContainer"] {
    padding: 1rem 1rem 2rem;
}
h1, h2, h3 {
    color: var(--text-color);
}
.stButton>button {
    background-color: #0077cc;
    color: white;
    border-radius: 8px;
    padding: 0.5rem 1.2rem;
    font-weight: 600;
}
.stButton>button:hover {
    background-color: #005fa3;
}
.stImage>img {
    border-radius: 12px;
    border: 2px solid var(--secondary-background-color);
}
.stContainer {
    background-color: var(--block-background-color);
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
a {
    color: #1f77b4;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# UI Controls
st.title("🎌 Anime Recommender System")
st.markdown("Discover anime similar to your favorites! Choose an anime below to get personalized recommendations.")

# Genre filter
all_genres = sorted(set(genre for genres in anime_df["genres"].str.split(", ") for genre in genres if genre))
selected_genres = st.multiselect("🎭 Filter by Genres (Optional)", all_genres)

# Main form
selected_anime = st.selectbox("🎞️ Select Anime", sorted(anime_df["title"].dropna().unique()))
top_n = st.slider("🔢 Number of Recommendations", 1, 10, 5)
sort_by = st.selectbox("📊 Sort Recommendations By", ["Similarity", "Average Score", "Popularity"])

# Recommend Button
if st.button("Recommend 🚀"):
    results = recommend_anime(selected_anime, top_n=top_n)
    if selected_genres:
        results = [rec for rec in results if any(g in rec["genres"].split(", ") for g in selected_genres)]
    if sort_by == "Average Score":
        results = sorted(results, key=lambda x: x["score"] or 0, reverse=True)
    elif sort_by == "Popularity":
        results = sorted(results, key=lambda x: anime_df[anime_df["title"] == x["title"]]["popularity"].iloc[0], reverse=True)

    if not results:
        st.warning("No recommendations match the selected genres.")
    else:
        st.subheader(f"✨ Recommendations for '{selected_anime}':")
        for rec in results:
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(rec["cover"], use_container_width=True)
                with col2:
                    st.markdown(f"### [{rec['title']}]({rec['anilist_url']})")
                    st.markdown(f"**Genres:** _{rec['genres']}_")
                    st.markdown(f"**Average Score:** `{rec['score'] or 'N/A'}`")
                    st.markdown(f"**Description:** {truncate_description(rec['description'])}")
