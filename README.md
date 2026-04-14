🎬 Cinescope — Movie Recommender System

A smart content-based movie recommendation system built using Python, Machine Learning, and Streamlit.
Cinescope helps users discover movies similar to their favorites using TF-IDF + cosine similarity on movie metadata.

🚀 Live Demo
👉 Try the app here:
  https://cinescopehq.streamlit.app/

📌 Features

🎯 Content-Based Recommendation Engine

Suggests movies based on similarity of plot, genres, keywords, and metadata
🔍 Smart Search System
Search any movie and get relevant recommendations instantly

🎥 Interactive Streamlit UI
Clean and user-friendly interface

⚡ Fast Prediction Engine
Uses precomputed similarity matrix for quick recommendations

📊 TF-IDF Vectorization
Converts movie metadata into numerical features

🧠 Cosine Similarity Model
Measures similarity between movies efficiently

💾 Optimized Model Storage
Uses .pkl files for fast loading:
tfidf.pkl
tfidf_matrix.pkl
indices.pkl
df.pkl

🧠 How It Works
Movie dataset is cleaned and preprocessed
Important features (overview, genres, keywords, cast, etc.) are combined
TF-IDF vectorization is applied
Cosine similarity matrix is computed
When a user selects a movie:
System finds closest vectors
Returns top-N similar movies

🛠️ Tech Stack
Frontend: Streamlit
Backend: Python
ML/NLP: Scikit-learn (TF-IDF, cosine similarity)
Data Handling: Pandas, NumPy
Model Storage: Pickle (.pkl files)

📂 Project Structure
TMDBMOVIE/
│
├── app.py                  # Streamlit frontend
├── main.py                 # Recommendation logic
├── movies_metadata.csv     # Dataset
├── tfidf.pkl              # TF-IDF model
├── tfidf_matrix.pkl       # Feature matrix
├── indices.pkl            # Movie index mapping
├── df.pkl                 # Processed dataframe
├── requirements.txt       # Dependencies
├── runtime.txt            # Python version
└── .gitignore

⚙️ Installation & Setup
1. Clone the repository
git clone https://github.com/your-username/cinescope-movie-recommender.git
cd cinescope-movie-recommender
2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
3. Install dependencies
pip install -r requirements.txt
4. Run Streamlit app
streamlit run app.py

🌐 Deployment

This project is deployed using Streamlit Cloud.

To redeploy:

Push changes to GitHub
Streamlit auto-builds the latest version

📊 Dataset
Source: TMDB Movie Dataset
Contains metadata like:
Title
Overview
Genres
Cast
Keywords

👨‍💻 Author

Aneek Saha
GitHub: https://github.com/aneeksaha2015-hub

⭐ Show Your Support

If you like this project:

⭐ Star the repository
🍴 Fork it
🚀 Share it
