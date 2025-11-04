📘 README.md (Detailed and Professional)
# 🎌 AniSuggest — ML-Based Anime Recommender System

> "You finish a great anime, wait months for the next season... and wish someone could tell you what to watch next."  
> That's why I built **AniSuggest** — a smart Machine Learning–powered anime recommender that finds shows similar to the ones you love.

---

## 🌐 Live Demo
🔗 **Try it here:** [https://anisuggest.streamlit.app/](https://anisuggest.streamlit.app/)  
💻 **Source Code:** [https://github.com/divyTechS/nextanime](https://github.com/divyTechS/nextanime)

---

## 🎯 Project Overview
**AniSuggest** is a **content-based recommendation system** built using **Machine Learning (TF-IDF + Cosine Similarity)** and **Streamlit**.  
It intelligently recommends anime similar to your selected title, letting you filter results by **genre**, **popularity**, or **average score** — all inside a sleek **glassmorphic interface**.

---

## 🧠 How It Works
1. **Data Preparation**
   - Fetched data using the **AniList GraphQL API** (title, description, cover, genres, popularity, score).
   - Cleaned and preprocessed the text using **Pandas** and **regex**.
   - Stored the final dataset as `anime_data.pkl`.

2. **Model Training**
   - Used **Scikit-learn's TF-IDF Vectorizer** to convert anime descriptions into numerical vectors.
   - Computed **Cosine Similarity** between every pair of anime.
   - Stored precomputed similarity matrix as `anime_similarity.pkl` for fast lookups.

3. **Recommendation Engine**
   - Input: Anime title  
   - Finds index in dataframe → fetches top N most similar anime using similarity matrix.  
   - Allows user-defined sorting (Similarity / Score / Popularity).  
   - Genre filters applied dynamically via Streamlit UI.

4. **Frontend (Streamlit App)**
   - Designed a custom **glassmorphic interface** using HTML + CSS inside Streamlit markdown.
   - Interactive sidebar for genre selection, number of recommendations, and sorting.
   - Displays each anime with:
     - Cover image
     - Title (clickable AniList link)
     - Genres
     - Average score
     - Truncated description

---

## 🧰 Tech Stack
| Layer | Tools Used |
|:------|:------------|
| **Frontend** | Streamlit + Custom CSS (Glassmorphism, animations) |
| **Machine Learning** | Scikit-learn (TF-IDF, Cosine Similarity) |
| **Data Processing** | Pandas, NumPy, Regex |
| **API & Data Source** | AniList GraphQL API |
| **Storage** | Pickle (pre-saved model + dataset) |

---

## ✨ Features
- 🔍 **Smart ML recommendations** — finds anime similar to your favorite shows.
- 🎭 **Genre filters** — narrow results by genre or tags.
- ⭐ **Sorting options** — sort by similarity, average score, or popularity.
- 🎨 **Glass UI** — custom CSS with glow, blur, and hover effects.
- ⚡ **Fast performance** — uses cached data for instant loading.
- 💻 **Fully deployed** — hosted on Streamlit Cloud.

---


## 📦 Installation

### 1️⃣ Clone the repo
```bash
git clone https://github.com/divyTechS/nextanime.git
cd nextanime

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the Streamlit app
streamlit run app.py

📂 Project Structure
├── app.py                  # Main Streamlit application
├── anime_data.pkl          # Preprocessed anime dataset
├── anime_similarity.pkl    # Precomputed similarity matrix
├── requirements.txt        # All dependencies
└── README.md               # Documentation

🧩 Core Functions
recommend_anime(title, top_n=5)

Finds anime similar to the given title based on cosine similarity.

Returns list of top recommendations with cover, score, genres, and description.

truncate_description(text, max_len=250)

Truncates long anime summaries gracefully, ending at the last sentence.

load_data()

Loads cached anime data and similarity matrix using Streamlit’s @st.cache_data.

🧑‍💻 Developer Notes

Used Streamlit custom HTML & CSS to create a translucent, glowing UI.

Applied regex-based text cleaning for consistent TF-IDF vectorization.

Used Pickle to pre-serialize the similarity matrix for fast loading.

🤝 Contributing

Suggestions, issues, and pull requests are welcome!
If you’d like to add new features (like collaborative filtering or trending anime tab), feel free to open a PR.

📜 License

Licensed under the MIT License — free to use, modify, and distribute.

👨‍💻 Author

Divyesh Shivdas Swarge
🎓 B.Tech CSE, IIITDM Jabalpur
Portfolio: (https://divytechs.vercel.app/)

📧 divyeshtechs@gmail.com

💼 LinkedIn
