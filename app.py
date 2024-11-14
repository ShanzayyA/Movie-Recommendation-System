from flask import Flask, request, render_template
import pandas as pd
import sqlite3
import pickle
import requests  # Import requests to make API calls

# IMDb API key and base URL
OMDB_API_KEY = '209a89e5'
OMDB_BASE_URL = 'http://www.omdbapi.com/'

app = Flask(__name__)

# Load the dataset and similarity matrix from pickle files
movies = pickle.load(open('movies_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie_title, similarity_threshold=0.3, genre_filter=None):
    """Generate movie recommendations with additional IMDb data."""
    try:
        normalized_title = movie_title.strip().lower()
        movies['normalized_title'] = movies['title'].str.strip().str.lower()

        # Find the index of the movie
        movie_idx = movies[movies['normalized_title'] == normalized_title].index[0]
        distances = list(enumerate(similarity[movie_idx]))
        distances = sorted(distances, reverse=True, key=lambda x: x[1])

        recommended_movies = []
        for i in distances[1:]:
            # Skip the first item since it’s the movie itself
            if distances[i[0]][1] > similarity_threshold and (genre_filter is None or genre_filter.lower() in movies.iloc[i[0]].genre.lower()):
                movie_data = {
                    "title": movies.iloc[i[0]].title,
                    "release_date": movies.iloc[i[0]].release_date,
                    "genre": movies.iloc[i[0]].genre,
                    "rating": movies.iloc[i[0]].vote_average
                }
                
                # Fetch additional IMDb data
                imdb_data = get_movie_details(movies.iloc[i[0]].title)
                if imdb_data:
                    movie_data.update(imdb_data)
                
                recommended_movies.append(movie_data)

        return recommended_movies if recommended_movies else [{"title": "No recommendations found."}]
    except IndexError:
        return [{"title": "Movie not found. Please try a different title."}]

def log_search(movie_title, similarity_level, genre_filter, recommendations):
    """Logs each search into the SQLite database."""
    conn = sqlite3.connect('search_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO history (movie_title, similarity_level, genre_filter, recommendations)
        VALUES (?, ?, ?, ?)
    ''', (movie_title, similarity_level, genre_filter, ', '.join(recommendations)))
    conn.commit()
    conn.close()

def get_search_history(limit=5):
    """Retrieve recent search history from the database."""
    conn = sqlite3.connect('search_history.db')
    cursor = conn.cursor()
    cursor.execute('SELECT movie_title, similarity_level, genre_filter, recommendations, timestamp FROM history ORDER BY timestamp DESC LIMIT ?', (limit,))
    history = cursor.fetchall()
    conn.close()
    return history

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if request.method == 'POST':
        movie_title = request.form.get('movie_title')
        similarity_level = request.form.get('similarity_level', 'medium')
        genre_filter = request.form.get('genre_filter', None)
        
        THRESHOLDS = {"low": 0.05, "medium": 0.3, "high": 0.5}
        threshold = THRESHOLDS.get(similarity_level, 0.3)

        recommendations = recommend(movie_title, similarity_threshold=threshold, genre_filter=genre_filter)
        log_search(movie_title, similarity_level, genre_filter, [rec['title'] for rec in recommendations])

    # Retrieve paginated search history
    conn = sqlite3.connect('search_history.db')
    cursor = conn.cursor()
    offset = (page - 1) * per_page
    cursor.execute("SELECT movie_title, similarity_level, genre_filter, recommendations, timestamp FROM history ORDER BY timestamp DESC LIMIT ? OFFSET ?", (per_page, offset))
    search_history = cursor.fetchall()
    conn.close()

    # Check if there are more results for the next page
    conn = sqlite3.connect('search_history.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM history")
    total_items = cursor.fetchone()[0]
    conn.close()

    has_next = total_items > page * per_page

    return render_template('index.html', recommendations=recommendations, search_history=search_history, page=page, has_next=has_next)

def get_movie_details(movie_title):
    """Fetch additional movie details from the OMDb API."""
    # Construct the API URL for movie search by title
    search_url = f"{OMDB_BASE_URL}?t={movie_title}&apikey={OMDB_API_KEY}"    
    # Send a request to the OMDb API
    response = requests.get(search_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Check if the movie was found
        if data.get("Response") == "True":
            # Return relevant movie details
            return {
                "imdb_rating": data.get("imdbRating"),
                "cast": data.get("Actors"),
                "plot": data.get("Plot"),
                "director": data.get("Director")
            }
    return None  # Return None if the movie wasn't found or an error occurred

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)

