from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__, static_url_path='/static')

# Load data
movies = pd.read_csv("movie.csv")
ratings = pd.read_csv("rating.csv")

# Clean movie titles
def clean_title(title):
    return re.sub("[^a-zA-Z0-9 ]", "", title)

# Preprocess titles
movies["clean_title"] = movies["title"].apply(clean_title)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
tfidf_matrix = vectorizer.fit_transform(movies["clean_title"])

# Search function to find movies
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search_movies', methods=['POST'])
def search_movies():
    query = clean_title(request.form['query'])
    query_vec = vectorizer.transform([query])
    similarity = cosine_similarity(query_vec, tfidf_matrix).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = movies.iloc[indices][::-1]
    return render_template('search_results.html', results=results)

# Find similar movies based on user ratings
@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    movie_id = int(request.form['movieId'])
    similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] >= 4)]["userId"].unique()
    similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] >= 4)]["movieId"]
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)
    similar_user_recs = similar_user_recs[similar_user_recs > 0.1]
    all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] >= 4)]
    all_user_recs =all_users["movieId"].value_counts() / len(all_users["userId"].unique())
    rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1, sort=False)
    rec_percentages.columns = ["similar", "all"]
    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    recommendations = rec_percentages.sort_values("score", ascending=False).head(10)
    recommended_movies = recommendations.merge(movies, left_index=True, right_on="movieId")
    return render_template('recommendations.html', recommendations=recommended_movies)

if __name__ == '__main__':
    app.run(debug=True)