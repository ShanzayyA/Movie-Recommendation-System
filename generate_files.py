import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load dataset
movies = pd.read_csv('dataset.csv')

# Create 'tags' by combining relevant information
movies['tags'] = (
    movies['title'] + " " +
    movies['genre'] + " " +
    movies['overview']
)

# Keep necessary columns, including 'genre', 'release_date', and 'vote_average' for display
new_data = movies[['id', 'title', 'genre', 'release_date', 'vote_average', 'tags']]

# Convert text to vector
cv = TfidfVectorizer(max_features=3000, stop_words='english')
vector = cv.fit_transform(new_data['tags'].values.astype('U')).toarray()

# Compute similarity matrix
similarity = cosine_similarity(vector)

# Save processed data and similarity matrix
pickle.dump(new_data, open('movies_list.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

