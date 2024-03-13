import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Clean movie titles
def clean_title(title):
    return re.sub("[^a-zA-Z0-9 ]", "", title)

# Load data
movies = pd.read_csv("movie.csv")
ratings = pd.read_csv("rating.csv")

# Preprocess titles
movies["clean_title"] = movies["title"].apply(clean_title)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
tfidf_matrix = vectorizer.fit_transform(movies["clean_title"])

# Search function to find movies
def search_movies(query):
    query = clean_title(query)
    query_vec = vectorizer.transform([query])
    similarity = cosine_similarity(query_vec, tfidf_matrix).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    return movies.iloc[indices][::-1]

# Find similar movies based on user ratings
def find_similar_movies(movie_id):
    similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] >= 4)]["userId"].unique()
    similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] >= 4)]["movieId"]
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)
    similar_user_recs = similar_user_recs[similar_user_recs > 0.1]
    all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] >= 4)]
    all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
    rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1, sort=False)
    rec_percentages.columns = ["similar", "all"]
    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    recommendations = rec_percentages.sort_values("score", ascending=False).head(10)
    return recommendations.merge(movies, left_index=True, right_on="movieId")

# Main interaction loop
if __name__ == "__main__":
    while True:
        search_query = input("Enter a movie title to search (or type 'exit' to quit): ")
        if search_query.lower() == 'exit':
            break
        search_results = search_movies(search_query)
        if not search_results.empty:
            print("Search results:")
            print(search_results[["movieId", "title"]])
            movie_id = int(input("Enter a movie ID from the above list to find similar movies: "))
            similar_movies = find_similar_movies(movie_id)
            print("Movies similar to your choice:")
            print(similar_movies[["title", "genres", "score"]])
        else:
            print("No results found. Please try another title.")