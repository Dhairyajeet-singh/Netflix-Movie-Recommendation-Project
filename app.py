import streamlit as st
import pickle
import pandas as pd
import requests
from dotenv import load_dotenv
import os
import gzip

# Page configuration
st.set_page_config(
    page_title="CineMatch - Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load data
@st.cache_data
def load_movie_data():
    with gzip.open("similarity.pkl.gz", "rb") as f:
        similarity = pickle.load(f)
    movies_dict = pickle.load(open('movies.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    return similarity, movies

similarity, movies = load_movie_data()

load_dotenv()  
api = os.getenv("api_key")

# Custom CSS for modern, cinematic design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
    text-align: center;
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: #d3d3d3; /* Light gray */
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .search-container {
        background: gray;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 2rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .movie-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.8);
        height: 100%;
        text-align: center;
    }
    
    .movie-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
    }
    
    .movie-poster {
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        width: 100%;
        max-width: 200px;
        height: auto;
    }
    
    .movie-poster:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    
    .movie-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 1rem;
        line-height: 1.4;
        min-height: 2.8rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .recommend-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .recommend-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    .results-header {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 3rem 0 2rem 0;
        position: relative;
    }
    
    .results-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 3px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 2px;
    }
    
    .loading-container {
        text-align: center;
        padding: 3rem;
    }
    
    .loading-text {
        font-size: 1.2rem;
        color: #667eea;
        font-weight: 500;
    }
    
    .selectbox-container {
        margin: 1rem 0;
    }
    
    .stSelectbox > div > div {
        background: #006400;
        border: 2px solid #e1e8ed;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .footer {
        text-align: center;
        margin-top: 4rem;
        padding: 2rem;
        color: #666;
        font-style: italic;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom animation */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Header section
st.markdown('<h1 class="main-header">🎬 CineMatch</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover your next favorite movie with AI-powered recommendations</p>', unsafe_allow_html=True)

# Search section
with st.container():
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("### 🔍 Find Your Perfect Movie Match")
        st.markdown('<div class="selectbox-container">', unsafe_allow_html=True)
        selected_movie = st.selectbox(
            'Choose a movie you enjoyed:',
            movies['title'].values,
            key="movie_selector",
            help="Select a movie and we'll recommend similar ones you might love!"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Center the button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            recommend_clicked = st.button('✨ Get Recommendations', key="recommend_btn")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Functions
def fetch_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api}&language=en-US')
        response.raise_for_status()
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750/cccccc/666666?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750/cccccc/666666?text=No+Image"

def get_movie_details(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api}&language=en-US')
        response.raise_for_status()
        data = response.json()
        return {
            'rating': data.get('vote_average', 'N/A'),
            'year': data.get('release_date', '')[:4] if data.get('release_date') else '',
            'overview': data.get('overview', '')[:100] + '...' if len(data.get('overview', '')) > 100 else data.get('overview', '')
        }
    except:
        return {'rating': 'N/A', 'year': '', 'overview': ''}

def recommend_movies(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommendations = []
        for i in movie_list:
            movie_id = movies.iloc[i[0]].movie_id
            title = movies.iloc[i[0]].title
            poster = fetch_poster(movie_id)
            details = get_movie_details(movie_id)
            
            recommendations.append({
                'title': title,
                'poster': poster,
                'rating': details['rating'],
                'year': details['year'],
                'overview': details['overview']
            })
        
        return recommendations
    except Exception as e:
        st.error(f"Error getting recommendations: {str(e)}")
        return []

# Recommendation results
if recommend_clicked:
    with st.spinner('🎭 Finding perfect matches for you...'):
        recommendations = recommend_movies(selected_movie)
    
    if recommendations:
        st.markdown('<h2 class="results-header fade-in-up">Recommended Movies</h2>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; color: #666; font-size: 1.1rem; margin-bottom: 2rem;">Based on your selection: <strong>{selected_movie}</strong></p>', unsafe_allow_html=True)
        
        # Display recommendations in a responsive grid
        cols = st.columns(5, gap="medium")
        
        for idx, movie in enumerate(recommendations):
            with cols[idx]:
                st.markdown(f'''
                <div class="movie-card fade-in-up">
                    <img src="{movie['poster']}" class="movie-poster" alt="{movie['title']}">
                    <div class="movie-title">{movie['title']}</div>
                    <div style="margin-top: 0.5rem; color: #666; font-size: 0.9rem;">
                        {f"⭐ {movie['rating']}" if movie['rating'] != 'N/A' else ""} 
                        {f"• {movie['year']}" if movie['year'] else ""}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Add some spacing and a subtle call-to-action
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('''
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                         border-radius: 15px; margin: 1rem 0;">
                <h4 style="color: #495057; margin-bottom: 1rem;">🎯 Found something interesting?</h4>
                <p style="color: #6c757d; margin-bottom: 0;">Try selecting one of these recommended movies to discover even more hidden gems!</p>
            </div>
            ''', unsafe_allow_html=True)

# Footer
st.markdown('''
<div class="footer">
    <p>🎬 Powered by AI • Built with ❤️ • Discover • Watch • Enjoy</p>
</div>
''', unsafe_allow_html=True)

# Add some JavaScript for enhanced interactions
st.markdown("""
<script>
// Add smooth scrolling behavior
document.documentElement.style.scrollBehavior = 'smooth';

// Add loading states to buttons
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            // Add loading state styling
            this.style.opacity = '0.7';
            this.style.transform = 'scale(0.98)';
            
            setTimeout(() => {
                this.style.opacity = '1';
                this.style.transform = 'scale(1)';
            }, 200);
        });
    });
});
</script>
""", unsafe_allow_html=True)