import streamlit as st
import pandas as pd
import pickle
import re

# Page Configuration
st.set_page_config(
    page_title="AniSuggest",
    layout="wide",
    page_icon="🎌",
)

# Load Data
@st.cache_data
def load_data():
    with open("anime_data.pkl", "rb") as f:
        anime_df = pickle.load(f)
    with open("anime_similarity.pkl", "rb") as f:
        similarity = pickle.load(f)
    return anime_df, similarity

anime_df, similarity = load_data()

# Utility
def truncate_description(text, max_len=250):
    if len(text) <= max_len:
        return text
    truncated = text[:max_len]
    last_period = truncated.rfind('.')
    return truncated[:last_period + 1] if last_period != -1 else truncated + "..."

def recommend_anime(title, top_n=5):
    title = title.lower()
    matches = anime_df[anime_df['title'].str.lower() == title]
    if matches.empty:
        st.error("No match found. Please try another title.")
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

# 🎨 Advanced Modern Glass UI
st.markdown("""
<style>
/* Animated gradient background */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top left, #0b0b15 0%, #111122 35%, #191933 100%);
    color: #f2f2f2;
    padding-top: 1.5rem;
}

/* Glass container */
.main-container {
    background: rgba(25, 25, 40, 0.85);
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(12px);
    border-radius: 18px;
    padding: 2.5rem;
    margin: 2rem auto;
    width: 90%;
    box-shadow: 0 0 25px rgba(0,0,0,0.4);
    transition: all 0.4s ease;
}
.main-container:hover {
    box-shadow: 0 0 40px rgba(0,119,255,0.35);
}

/* Title & text */
h1 {
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
    color: #a2c8ff;
    text-align: center;
    letter-spacing: 1px;
    text-shadow: 0 0 12px rgba(162, 200, 255, 0.4);
}
h3 {
    color: #e4e4f7;
}

/* Description */
.desc {
    text-align: center;
    font-size: 1.05rem;
    color: #cfd8ff;
    margin-bottom: 2rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(18, 18, 30, 0.9);
    backdrop-filter: blur(8px);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #005bea, #00c6fb);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    font-size: 1rem;
    transition: 0.3s;
    box-shadow: 0 0 10px rgba(0,150,255,0.3);
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(0,150,255,0.6);
}

/* Anime cards */
.anime-card {
    display: flex;
    flex-direction: row;
    gap: 1.5rem;
    align-items: flex-start;
    background: rgba(255,255,255,0.05);
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 1rem;
    transition: all 0.3s ease;
    margin-bottom: 1rem;
}
.anime-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 0 20px rgba(0,150,255,0.25);
}

/* Image */
.anime-card img {
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.15);
}

/* Links */
a {
    color: #82b1ff;
    text-decoration: none;
}
a:hover {
    color: #bbdefb;
    text-decoration: underline;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: #3b3b52;
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: #5a5a7a;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🎭 Filter & Preferences")
    all_genres = sorted(set(genre for genres in anime_df["genres"].str.split(", ") for genre in genres if genre))
    selected_genres = st.multiselect("Select Genres", all_genres)
    top_n = st.slider("Number of Recommendations", 3, 15, 6)
    sort_by = st.selectbox("Sort By", ["Similarity", "Average Score", "Popularity"])
    st.markdown("💡 **Tip:** Use genres to fine-tune your discovery.")

# 🧊 Main Glass Container with Title Inside
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

st.title("🎬 AniSuggest: Smart Anime Recommender")
st.markdown("""
<p class='desc'>
    Discover your next great anime — powered by intelligent similarity search.  
    Filter by genre, popularity, or score for refined and elegant recommendations.
</p>
""", unsafe_allow_html=True)

# Anime Selection & Recommendations
selected_anime = st.selectbox("🎞️ Choose Anime Title", sorted(anime_df["title"].dropna().unique()))

if st.button("🔍 Discover Similar Anime"):
    results = recommend_anime(selected_anime, top_n=top_n)
    if selected_genres:
        results = [r for r in results if any(g in r["genres"].split(", ") for g in selected_genres)]

    if sort_by == "Average Score":
        results = sorted(results, key=lambda x: x["score"] or 0, reverse=True)
    elif sort_by == "Popularity":
        results = sorted(results, key=lambda x: anime_df[anime_df["title"] == x["title"]]["popularity"].iloc[0], reverse=True)

    if not results:
        st.warning("No matches found for the selected filters.")
    else:
        st.markdown(f"### ✨ Top {len(results)} Recommendations for **{selected_anime}**")
        for rec in results:
            st.markdown(f"""
            <div class="anime-card">
                <img src="{rec['cover']}" width="120">
                <div>
                    <h3><a href="{rec['anilist_url']}" target="_blank">{rec['title']}</a></h3>
                    <p><b>Genres:</b> {rec['genres']}</p>
                    <p><b>Average Score:</b> {rec['score'] or 'N/A'}</p>
                    <p>{truncate_description(rec['description'])}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
