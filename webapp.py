import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="NextAnime Recommender 🎌", layout="wide")

# Load Data
@st.cache_data
def load_data():
    with open("anime_data.pkl", "rb") as f:
        anime_df = pickle.load(f)
    with open("anime_similarity.pkl", "rb") as f:
        similarity = pickle.load(f)
    return anime_df, similarity

anime_df, similarity = load_data()

# Helper
def truncate_description(text, max_len=300):
    if not text:
        return "No description available."
    if len(text) <= max_len:
        return text
    truncated = text[:max_len]
    last_period = truncated.rfind('.')
    return truncated[:last_period + 1] if last_period != -1 else truncated + "..."

def recommend_anime(title, top_n=5):
    title = title.lower()
    matches = anime_df[anime_df['title'].str.lower() == title]
    if matches.empty:
        st.error("❌ Anime not found. Try another title.")
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


# 🌈 — Modern Anime-Themed CSS
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    color: #e5e7eb;
    background: radial-gradient(circle at top left, #101820, #000000);
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0d0d0f 30%, #141826 100%);
}
[data-testid="stSidebar"] {
    background: rgba(10, 10, 20, 0.6);
    backdrop-filter: blur(15px);
    border-right: 1px solid rgba(255,255,255,0.1);
}
h1, h2, h3 {
    color: #89CFF0 !important;
    font-weight: 700;
}
.stButton>button {
    background: linear-gradient(90deg, #1e90ff, #8a2be2);
    border: none;
    color: white;
    border-radius: 10px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    transition: all 0.25s ease;
    box-shadow: 0 0 15px rgba(138,43,226,0.4);
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(30,144,255,0.6);
}
.stImage>img {
    border-radius: 16px;
    box-shadow: 0 0 10px rgba(255,255,255,0.08);
}
.stContainer {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    padding: 1rem 1.5rem;
    border-radius: 12px;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
    border: 1px solid rgba(255,255,255,0.08);
}
.stContainer:hover {
    transform: translateY(-3px);
    box-shadow: 0 0 25px rgba(138,43,226,0.25);
}
a {
    color: #93c5fd;
    text-decoration: none;
    font-weight: 600;
}
a:hover {
    text-decoration: underline;
    color: #60a5fa;
}
</style>
""", unsafe_allow_html=True)

# 🎴 Main Title
st.markdown("<h1 style='text-align:center;'>🌸 NextAnime — Your AI Otaku Companion</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color: #b3b3b3;'>Find your next obsession. Powered by data. Styled for weebs.</p>", unsafe_allow_html=True)
st.markdown("---")

# 🎭 Genre filter
all_genres = sorted(set(genre for genres in anime_df["genres"].str.split(", ") for genre in genres if genre))
selected_genres = st.multiselect("🎭 Filter by Genres", all_genres, help="Select genres to narrow down recommendations.")

# 🎞️ Main Input
col1, col2 = st.columns([2, 1])
with col1:
    selected_anime = st.selectbox("🎬 Choose Your Anime", sorted(anime_df["title"].dropna().unique()))
with col2:
    top_n = st.slider("🔢 How Many Recs?", 3, 10, 5)

sort_by = st.selectbox("⚙️ Sort Recommendations By", ["Similarity", "Average Score", "Popularity"])

# 🚀 Action
if st.button("✨ Recommend Me Something Cool!"):
    results = recommend_anime(selected_anime, top_n=top_n)
    if selected_genres:
        results = [rec for rec in results if any(g in rec["genres"].split(", ") for g in selected_genres)]
    if sort_by == "Average Score":
        results = sorted(results, key=lambda x: x["score"] or 0, reverse=True)
    elif sort_by == "Popularity":
        results = sorted(results, key=lambda x: anime_df[anime_df["title"] == x["title"]]["popularity"].iloc[0], reverse=True)

    if not results:
        st.warning("😔 No recommendations match the selected genres. Try fewer filters!")
    else:
        st.markdown(f"<h2>🔥 Top Picks for <span style='color:#8be9fd'>{selected_anime}</span>:</h2>", unsafe_allow_html=True)
        for rec in results:
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(rec["cover"], use_container_width=True)
                with col2:
                    st.markdown(f"### [{rec['title']}]({rec['anilist_url']})")
                    st.markdown(f"⭐ **Score:** {rec['score'] or 'N/A'}")
                    st.markdown(f"🎭 **Genres:** _{rec['genres']}_")
                    st.markdown(f"📝 **Description:** {truncate_description(rec['description'])}")

st.markdown("<br><hr><center><small>Made with 💙 by Otaku Devs for Otaku Fans — powered by Streamlit</small></center>", unsafe_allow_html=True)
