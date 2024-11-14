import pickle

# Load data from the pickle files
movies = pickle.load(open('movies_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie_title, similarity_threshold=0.3):
    # Normalize the input title
    normalized_title = movie_title.strip().lower()
    movies['normalized_title'] = movies['title'].str.strip().str.lower()
    
    try:
        # Find the index of the movie that matches the title
        movie_idx = movies[movies['normalized_title'] == normalized_title].index[0]
        print("Movie index found:", movie_idx)  # Debugging print

        # Get the similarity scores for the movie
        distances = list(enumerate(similarity[movie_idx]))
        print("Distances calculated:", distances[:10])  # Print first 10 distances for debugging

        # Sort by similarity score
        distances = sorted(distances, reverse=True, key=lambda x: x[1])

        # Get the top 5 recommendations (excluding the first as it’s the same movie)
        recommended_movies = [movies.iloc[i[0]].title for i in distances[1:6] if i[1] > similarity_threshold]

        print("Recommended movies:", recommended_movies)  # Debugging print
        return recommended_movies if recommended_movies else ["No recommendations found."]
    except IndexError:
        print("Movie not found in dataset.")
        return ["Movie not found. Please try a different title."]

# Test the function
print("Recommendations for 'Inception':", recommend("Inception", similarity_threshold=0.05))
print("Recommendations for 'The Godfather':", recommend("The Godfather", similarity_threshold=0.05))

