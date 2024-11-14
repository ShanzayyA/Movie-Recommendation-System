
# Movie Recommendation System

This project is a Flask-based web application that delivers personalized movie recommendations based on user input. By integrating machine learning, API data, and a structured interface, this application offers a feature-rich and user-friendly experience for movie enthusiasts.

## Features

- **Personalized Recommendations**: Uses a machine learning model to suggest movies based on user-provided titles, enabling highly customized recommendations.
- **Real-Time Data Integration**: Connects with the OMDb API to fetch the latest details, including ratings, cast, and summaries, ensuring each recommendation is up-to-date.
- **Search History Logging and Pagination**: Saves each search with relevant details in an SQLite database, allowing users to revisit and browse through previous searches via pagination.
- **Customizable Filters**: Allows users to adjust similarity levels and apply genre filters to refine recommendations further.

## File Overview

1. **`app.py`** - The main Flask application script that:
   - Handles routes and user input via a form in the HTML interface.
   - Fetches and displays real-time movie data from the OMDb API.
   - Manages the SQLite database for logging and paginating user searches.
   
2. **`generate_files.py`** - Script for dataset management and recommendation generation.
   - This file may include data processing and machine learning logic to enhance recommendations.

3. **`index.html`** - Main HTML template file containing:
   - The form for user input, including movie title, similarity level, and genre filter options.
   - Sections for displaying movie recommendations and recent search history with pagination controls.

4. **`styles.css`** - Custom styling to enhance the UI, including:
   - Background, typography, and button styling for an aesthetically pleasing user experience.
   - Specific styles for recommendations and recent searches to improve readability.

5. **`test_recommend.py`** - Contains unit tests for recommendation functionality, ensuring reliable outputs and validation for the machine learning model and API data handling.

## Installation

1. **Clone the repository**:
   ```bash
   git clone [your-repository-url]
   cd [repository-folder]
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Create a `.env` file to store sensitive API keys.
   ```plaintext
   OMDB_API_KEY=your_api_key_here
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the app**:
   Open `http://127.0.0.1:5000/` in your web browser.

## Usage

- **Input Preferences**: On the homepage, enter a movie title and customize your recommendations by selecting similarity levels and genres.
- **Explore Recommendations**: View a list of similar movies with real-time IMDb data, including ratings and cast information.
- **Browse Search History**: Easily access past recommendations with paginated search history, allowing you to revisit previous sessions.

## Technologies

- **Backend**: Flask, SQLite
- **Frontend**: HTML, CSS, Bootstrap
- **Machine Learning**: Scikit-Learn, Pandas, NumPy
- **API Integration**: OMDb API

## Dataset

The recommendation model was trained using data from [Chitranjan Upadhyay's Movie Recommendation System Dataset](https://github.com/ChitranjanUpadhayay/ML_Projects/tree/main/Datasets/Movies%20Recommendation%20System), providing the foundational movie data for generating suggestions.

## Acknowledgments

- Dataset: [Chitranjan Upadhyay’s Movie Recommendation System Dataset](https://github.com/ChitranjanUpadhayay/ML_Projects/tree/main/Datasets/Movies%20Recommendation%20System).
- OMDb API for real-time movie details.
