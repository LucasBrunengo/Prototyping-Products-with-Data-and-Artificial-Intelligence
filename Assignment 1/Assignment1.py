import streamlit as st  # Web application framework
import pandas as pd     # Data manipulation
import numpy as np      # Numerical operations
import plotly.express as px  # Interactive visualizations
import plotly.graph_objects as go  # Advanced graph creation
from datetime import datetime, timedelta  # Date and time handling
import calendar  # Calendar-related operations
import json  # JSON data handling
import matplotlib.pyplot as plt
import seaborn as sns


# Load custom CSS from a file
def local_css(file_name):
    with open(file_name) as f:  # Open and read the CSS file
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)  # Inject CSS into Streamlit app


local_css("Css.css") # Apply custom CSS styling

# Create styled header
st.markdown('<div class="netflix-header">🍿 Netflix Marathon-Watch Planner</div>', unsafe_allow_html=True)

# Add description
st.markdown('<div class="description">Plan your perfect marathon-watching session based on the time you have available and your content preferences.</div>', unsafe_allow_html=True)

# Function to parse duration into minutes or seasons
def process_duration(duration_str):
    if not duration_str or pd.isna(duration_str):  # Check for empty or NaN input
        return {'minutes': None, 'seasons': None}
    
    if 'min' in duration_str:  # Check if input is movie duration
        try:
            minutes = int(duration_str.split(' ')[0])  # Extract minutes as integer
            return {'minutes': minutes, 'seasons': None}  # Return movie duration
        except (ValueError, IndexError):  # Handle parsing errors
            return {'minutes': None, 'seasons': None}
    elif 'Season' in duration_str:  # Check if input is TV show seasons
        try:
            seasons = int(duration_str.split(' ')[0])  # Extract seasons as integer
            return {'minutes': None, 'seasons': seasons}  # Return TV show seasons
        except (ValueError, IndexError):  # Handle parsing errors
            return {'minutes': None, 'seasons': None}
    
    return {'minutes': None, 'seasons': None}  # Default return for unhandled cases

# Function to extract genres
def extract_genres(listed_in):
    if not listed_in or pd.isna(listed_in):  # Check for empty input
        return []
    return [genre.strip() for genre in listed_in.split(',')]  # Split and clean genres

# Load and process Netflix dataset
@st.cache_data
def load_data():
    df = pd.read_csv('netflix_titles.csv', low_memory=False)  # Read CSV file
    
    # Create processed dataframe with selected columns
    df_processed = pd.DataFrame()
    df_processed['title'] = df['title']
    df_processed['type'] = df['type']
    df_processed['rating'] = df['rating']
    df_processed['release_year'] = df['release_year']
    
    # Process content durations
    durations = df['duration'].apply(process_duration)  # Apply duration parsing
    df_processed['duration_minutes'] = [d['minutes'] for d in durations]  # Extract minutes
    df_processed['seasons'] = [d['seasons'] for d in durations]  # Extract seasons
    
    # Extract and process genres
    df_processed['genres'] = df['listed_in'].apply(extract_genres)  # Convert genres to list
    
    # Optimize categorical data types
    for col in ['type', 'rating']:
        if col in df_processed.columns:
            df_processed[col] = df_processed[col].astype('category')  # Convert to category
    
    # Add additional columns
    df_processed['country'] = df['country']
    df_processed['description'] = df['description']
    
    # Set default TV show estimates
    df_processed['avg_episode_minutes'] = 30  # Default episode length
    df_processed['episodes_per_season'] = 10  # Default episodes per season
    
    # Define genre categories
    hour_long_genres_list = ['TV Dramas', 'Crime TV Shows', 'TV Mysteries', 'TV Action & Adventure']
    comedy_genres = ['TV Comedies']
    reality_genres = ['Docuseries', 'Reality TV']
    
    # Filter for TV shows
    tv_mask = df_processed['type'] == 'TV Show'
    
    # Adjust episode details based on genre
    for idx, row in df_processed[tv_mask].iterrows():
        genres_str = df.loc[idx, 'listed_in'] if idx in df.index else ""  # Get genre string
        if any(genre in genres_str for genre in hour_long_genres_list):
            df_processed.at[idx, 'avg_episode_minutes'] = 45  # Longer episodes for dramas
        elif any(genre in genres_str for genre in comedy_genres):
            df_processed.at[idx, 'avg_episode_minutes'] = 22  # Shorter comedy episodes
            df_processed.at[idx, 'episodes_per_season'] = 12
        elif any(genre in genres_str for genre in reality_genres):
            df_processed.at[idx, 'avg_episode_minutes'] = 42  # Reality show episode length
            df_processed.at[idx, 'episodes_per_season'] = 8
    
    # Calculate total content duration
    df_processed['total_duration'] = df_processed.apply(
        lambda row: row['duration_minutes'] if row['type'] == 'Movie' else 
                    (row['seasons'] * row['episodes_per_season'] * row['avg_episode_minutes'] 
                     if pd.notna(row['seasons']) else None), 
        axis=1
    )
    
    # Remove problematic entries
    problematic_ratings = ['74 min', '84 min', '66 min']
    df_processed = df_processed[~df_processed['rating'].isin(problematic_ratings)]  # Filter out bad ratings
    
    return df_processed

# Function to format duration
def format_duration(minutes):
    if pd.isna(minutes):  # Check for missing input
        return "Unknown"
    
    hours = int(minutes) // 60  # Calculate whole hours
    remaining_minutes = int(minutes) % 60  # Calculate remaining minutes
    
    if hours > 0 and remaining_minutes > 0:
        return f"{hours}h {remaining_minutes}m"  # Hours and minutes
    elif hours > 0:
        return f"{hours}h"  # Only hours
    else:
        return f"{remaining_minutes}m"  # Only minutes

def filter_by_mood(df, selected_mood):
    if not selected_mood or selected_mood == "Any Mood":  # Check for default mood
        return df
    
    # Comprehensive mood-based content mapping
    mood_mapping = {
        "Happy": {
            "genres": ["Comedies", "Children & Family Movies", "Stand-Up Comedy", "Feel-Good", "Music & Musicals"],
            "keywords": ["comedy", "funny", "laugh", "humor", "cheerful", "light-hearted", "family", "uplifting"]
        },
        "Sad": {
            "genres": ["Dramas", "Tearjerkers", "Documentaries", "International Movies"],
            "keywords": ["drama", "emotional", "grief", "moving", "sad", "tragic", "bittersweet"]
        },
        "Excited": {
            "genres": ["Action & Adventure", "Sci-Fi & Fantasy", "Thrillers", "Sports Movies", "Blockbusters"],
            "keywords": ["action", "thrilling", "adventure", "fast-paced", "epic", "battle", "spectacular"]
        },
        "Relaxed": {
            "genres": ["Documentaries", "Travel & Adventure Documentaries", "Food & Wine", "Nature & Wildlife Docs"],
            "keywords": ["gentle", "calm", "peaceful", "nature", "soothing", "meditative", "aesthetic"]
        },
        "Romantic": {
            "genres": ["Romantic Movies", "Romantic Comedies", "K-dramas", "Spanish-Language TV Shows"],
            "keywords": ["romance", "love", "date", "relationship", "couple", "wedding", "passion"]
        },
        "Curious": {
            "genres": ["Documentaries", "Science & Nature TV", "Docuseries", "Historical Documentaries"],
            "keywords": ["fascinating", "educational", "informative", "enlightening", "thought-provoking"]
        },
        "Nostalgic": {
            "genres": ["Classic Movies", "Cult Movies", "Classic TV Shows", "Retro TV"],
            "keywords": ["classic", "nostalgic", "vintage", "retro", "cult", "throwback", "timeless"]
        },
        "Tense": {
            "genres": ["Horror Movies", "Thrillers", "Crime TV Shows", "Psychological Thrillers"],
            "keywords": ["suspenseful", "scary", "intense", "gripping", "dark", "mysterious", "shocking"]
        }
    }
    
    if selected_mood not in mood_mapping:  # Validate mood selection
        return df
    
    mood_genres = mood_mapping[selected_mood]["genres"]  # Get mood-specific genres
    mood_keywords = mood_mapping[selected_mood]["keywords"]  # Get mood-specific keywords
    
    # Filter by matching genres
    genre_filtered = df[df['genres'].apply(
        lambda x: any(genre in mood_genres for genre in x if isinstance(x, list))
    )]
    
    # Return genre-filtered if sufficient content
    if len(genre_filtered) > 100:
        return genre_filtered
    
    # Filter by keywords in description
    keyword_filtered = df[df['description'].str.lower().apply(
        lambda x: any(keyword in str(x).lower() for keyword in mood_keywords)
    ) if 'description' in df.columns else False]
    
    # Combine and remove duplicates
    combined = pd.concat([genre_filtered, keyword_filtered]).drop_duplicates()
    
    # Return combined or original if not enough content
    if len(combined) < 20:
        return df
    
    return combined

# Function to find content combinations for marathon watching
def find_marathon_plan(available_time, filtered_df, content_type="mixed", max_items=5, mood="Any Mood"):
    if mood != "Any Mood":  # Apply mood filtering if specified
        filtered_df = filter_by_mood(filtered_df, mood)
    
    available_minutes = available_time * 60  # Convert hours to minutes
    
    # Filter content type
    if content_type == "movies_only":  # Only movies
        filtered_df = filtered_df[filtered_df['type'] == 'Movie']
    elif content_type == "series_only":  # Only TV shows
        filtered_df = filtered_df[filtered_df['type'] == 'TV Show']
    
    # Check for empty dataset after filtering
    if len(filtered_df) == 0:
        return []
    
    # Reduce sample size for large datasets
    if len(filtered_df) > 5000:
        filtered_df = filtered_df.sample(5000, random_state=42)
    
    plans = []
    
    # Try multiple plan combinations
    for _ in range(min(3, max(1, int(5000/len(filtered_df))))):  # Adaptive plan count
        current_plan = []
        remaining_time = available_minutes
        temp_df = filtered_df.sample(frac=1, random_state=np.random.randint(1, 1000))  # Shuffle
        
        # Find content that fits within available time
        for idx, content in temp_df.iterrows():
            # Limit plan to max items
            if len(current_plan) >= max_items:
                break
                
            if content['type'] == 'Movie':
                # Check if movie fits in remaining time
                if pd.notna(content['duration_minutes']) and content['duration_minutes'] <= remaining_time:
                    current_plan.append({
                        'title': content['title'],
                        'type': 'Movie',
                        'duration_minutes': content['duration_minutes'],
                        'genres': content['genres'],
                        'description': content['description'],
                        'rating': content['rating'],
                        'release_year': content['release_year']
                    })
                    remaining_time -= content['duration_minutes']
                    temp_df = temp_df.drop(idx)
            else:  # TV Show
                # Check if TV show episodes fit in remaining time
                if pd.notna(content['avg_episode_minutes']) and content['avg_episode_minutes'] <= remaining_time:
                    # Calculate episodes to watch
                    episodes_to_watch = min(
                        int(remaining_time / content['avg_episode_minutes']),
                        content['episodes_per_season'] * content['seasons'] if pd.notna(content['seasons']) else 10
                    )
                    
                    if episodes_to_watch > 0:
                        watch_time = episodes_to_watch * content['avg_episode_minutes']
                        current_plan.append({
                            'title': content['title'],
                            'type': 'TV Show',
                            'episodes': episodes_to_watch,
                            'episode_length': content['avg_episode_minutes'],
                            'duration_minutes': watch_time,
                            'genres': content['genres'],
                            'description': content['description'],
                            'rating': content['rating'],
                            'seasons': content['seasons'],
                            'release_year': content['release_year']
                        })
                        remaining_time -= watch_time
                        temp_df = temp_df.drop(idx)
        
        # Add plan if content exists
        if current_plan:
            total_time = sum(item['duration_minutes'] for item in current_plan)
            plans.append({
                'content': current_plan,
                'total_duration': total_time,
                'remaining_time': remaining_time,
                'utilization': (total_time / available_minutes) * 100
            })
    
    # Sort plans by time utilization
    plans.sort(key=lambda x: x['utilization'], reverse=True)
    
    return plans

# Load the data with progress indicator
with st.spinner('Loading data...'):
    df = load_data()  # Load Netflix dataset

# Create application tabs
tab1, tab2, tab3 = st.tabs(["📅 Plan Your Marathon", "📊 Content Explorer", "ℹ️ About"])

with tab1:
    st.markdown('<div class="section-title animated-title">Create Your Marathon-Watch Plan</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-container fadeIn">', unsafe_allow_html=True)
    
    # Create input layout
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # Available Time input
    st.markdown('<div class="input-item">', unsafe_allow_html=True)
    st.markdown('<div class="section-title animated-title">Available Time</div>', unsafe_allow_html=True)
    col_hrs, col_min = st.columns(2)
    with col_hrs:
        hours = st.number_input("Hours", min_value=0, max_value=24, value=3)  # Hours input
    with col_min:
        minutes = st.number_input("Minutes", min_value=0, max_value=59, value=0)  # Minutes input
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Calendar input
    st.markdown('<div class="input-item">', unsafe_allow_html=True)
    st.markdown('<div class="section-title animated-title">When are you watching?</div>', unsafe_allow_html=True)
    selected_date = st.date_input("Select Date", datetime.now().date())  # Date selection
    weekday = calendar.day_name[selected_date.weekday()]  # Get day of week
    st.markdown(f"<p style='text-align: center; color: white;'>You're planning to watch on <strong>{weekday}</strong></p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Content Type input
    st.markdown('<div class="input-item">', unsafe_allow_html=True)
    st.markdown('<div class="section-title animated-title">Content Type</div>', unsafe_allow_html=True)
    content_type = st.radio("Select type", ["Mixed", "Movies Only", "TV Shows Only"], horizontal=True)  # Content type selection
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close input container
    
    # Second row of inputs
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # Mood selection
    st.markdown('<div class="input-item">', unsafe_allow_html=True)
    st.markdown('<div class="section-title animated-title">Current Mood</div>', unsafe_allow_html=True)

    # Mood options with emojis
    moods = [
        "Any Mood",
        "Happy 😊",
        "Sad 😢", 
        "Excited 🤩",
        "Relaxed 😌",
        "Romantic 💖",
        "Curious 🧐",
        "Nostalgic 🕰️",
        "Tense 😰"
    ]

    # Mood radio button
    selected_mood_with_emoji = st.radio(
        "How are you feeling today?",
        moods,
        horizontal=True
    )

    # Process selected mood
    selected_mood = selected_mood_with_emoji.split()[0] if selected_mood_with_emoji != "Any Mood" else "Any Mood"

    # Store mood in session state
    st.session_state.selected_mood = selected_mood

    st.markdown('</div>', unsafe_allow_html=True)

    # Genres input
    st.markdown('<div class="input-item">', unsafe_allow_html=True)
    st.markdown('<div class="section-title animated-title">Genres</div>', unsafe_allow_html=True)
    
    # Get unique genres
    all_genres = set()
    for genres_list in df['genres']:
        if isinstance(genres_list, list):
            all_genres.update(genres_list)
    
    # Genres multiselect
    selected_genres = st.multiselect(
        "Select Genres", 
        sorted(list(all_genres)),
        default=["Comedies", "Dramas"] if "Comedies" in all_genres and "Dramas" in all_genres else []
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Ratings input
    st.markdown('<div class="input-item">', unsafe_allow_html=True)
    st.markdown('<div class="section-title animated-title">Content Rating</div>', unsafe_allow_html=True)
    
    # Get unique ratings
    valid_ratings = sorted([r for r in df['rating'].dropna().unique() if isinstance(r, str)])
    
    # Rating selection
    default_ratings = [r for r in ["TV-14", "TV-MA", "PG-13", "R"] if r in valid_ratings]
    selected_ratings = st.multiselect(
        "Select Ratings", 
        valid_ratings,
        default=default_ratings
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Release Years input
    st.markdown('<div class="input-item">', unsafe_allow_html=True)
    st.markdown('<div class="section-title animated-title">Release Years</div>', unsafe_allow_html=True)
    
    # Year range slider
    min_year = int(df['release_year'].min())
    max_year = int(df['release_year'].max())
    
    year_range = st.slider(
        "Select Range", 
        min_value=min_year, 
        max_value=max_year, 
        value=(max_year-10, max_year),
        step=1
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close input container
    
    # Countries input
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    st.markdown('<div class="input-item">', unsafe_allow_html=True)
    st.markdown('<div class="section-title animated-title">Country Filter (Optional)</div>', unsafe_allow_html=True)
    
    # Get top countries function
    @st.cache_data
    def get_top_countries(dataframe):
        country_counts = {}
        for country_str in dataframe['country'].dropna():
            if isinstance(country_str, str):
                for country in country_str.split(','):
                    country = country.strip()
                    country_counts[country] = country_counts.get(country, 0) + 1
        
        return sorted(
            [(country, count) for country, count in country_counts.items()],
            key=lambda x: x[1], 
            reverse=True
        )[:24]
    
    # Get and display top countries
    top_countries = get_top_countries(df)
    countries = [country for country, _ in top_countries]
    
    selected_countries = []
    
    # Country checkboxes
    cols = st.columns(5)
    for i, (country, count) in enumerate(top_countries[:22]):
        col_idx = i % 5
        with cols[col_idx]:
            if st.checkbox(f"{country} ({count})", value=False):
                selected_countries.append(country)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close input container
    
    # Find Marathon Plan button
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("Find My Marathon Plan", type="primary", key="find_plan_button", 
                help="Click to generate your personalized marathon plans"):
        with st.spinner('Creating your marathon plan...'):
            # Apply filters to dataset
            filtered_df = df.copy()
            
            # Genre filtering
            if selected_genres:
                filtered_df = filtered_df[filtered_df['genres'].apply(
                    lambda x: any(genre in selected_genres for genre in x if isinstance(x, list))
                )]
            
            # Rating filtering
            if selected_ratings:
                filtered_df = filtered_df[filtered_df['rating'].isin(selected_ratings)]
            
            # Release year filtering
            filtered_df = filtered_df[
                (filtered_df['release_year'] >= year_range[0]) & 
                (filtered_df['release_year'] <= year_range[1])
            ]
            
            # Country filtering
            if selected_countries:
                filtered_df = filtered_df[filtered_df['country'].apply(
                    lambda x: any(country in str(x).split(',') for country in selected_countries) 
                    if pd.notna(x) and isinstance(x, str) else False
                )]
            
            # Content type mapping
            content_type_map = {
                "Mixed": "mixed",
                "Movies Only": "movies_only",
                "TV Shows Only": "series_only"
            }
            
            # Generate marathon plans
            if len(filtered_df) == 0:
                st.error("No content matches your filters. Please adjust your preferences.")
            else:
                st.session_state.filtered_df = filtered_df
                st.session_state.marathon_plans = find_marathon_plan(
                    hours + minutes/60, 
                    filtered_df, 
                    content_type_map[content_type],
                    5,
                    selected_mood
                )
                st.session_state.show_results = True
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close form container
    
    # Results display
    if 'show_results' in st.session_state and st.session_state.show_results:
        plans = st.session_state.marathon_plans
        
        if not plans:
            st.error("Couldn't find any suitable content combinations. Try adjusting your time or preferences.")
        else:
            st.markdown('<div class="section-title animated-title">Your Marathon-Watch Recommendations</div>', unsafe_allow_html=True)
            
            # Create plan tabs
            plan_tabs = st.tabs([f"Plan {i+1}" for i in range(min(3, len(plans)))])
            
            # Display each plan
            for i, (plan_tab, plan) in enumerate(zip(plan_tabs, plans[:3])):
                with plan_tab:
                    st.markdown('<div class="form-container fadeIn">', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <div class="time-info">
                            <span class="highlight">{format_duration(plan['total_duration'])}</span> of content 
                            ({plan['utilization']:.1f}% of your available time)
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display each content item in the plan
                    for item in plan['content']:
                        st.markdown('<div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #333;">', unsafe_allow_html=True)
    
                        # Title and basic info
                        st.markdown(f"""
                        <div class="recommendation-title">{item['title']}</div>
                        <div>{item['type']} • {item['rating'] if 'rating' in item and pd.notna(item['rating']) else 'Not Rated'} • {item.get('release_year', 'Unknown Year')}</div>
                        """, unsafe_allow_html=True)
                        
                        # Duration information
                        if item['type'] == 'Movie':
                            st.markdown(f"""
                            <div class="time-info">Duration: {format_duration(item['duration_minutes'])}</div>
                            """, unsafe_allow_html=True)
                        else:
                            # TV Show episode details
                            episodes_text = f"{item['episodes']} episode{'s' if item['episodes'] > 1 else ''}"
                            if 'seasons' in item and pd.notna(item['seasons']):
                                episodes_text += f" (from {item['seasons']} season{'s' if item['seasons'] > 1 else ''})"
                            
                            st.markdown(f"""
                            <div class="time-info">Watch {episodes_text} • {format_duration(item['duration_minutes'])}</div>
                            """, unsafe_allow_html=True)
                        
                        # Genres display
                        if 'genres' in item and item['genres']:
                            genres_html = ""
                            for genre in item['genres'][:3]:  # Show up to 3 genres
                                genres_html += f'<span class="genre-badge">{genre}</span>'
                            st.markdown(f"""
                            <div style="margin: 10px 0;">
                                {genres_html}
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Description
                        if 'description' in item and pd.notna(item['description']):
                            st.markdown(f"""
                            <div style="margin-top: 10px; font-size: 0.9em; color: #cccccc;">
                                {item['description']}
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)

                    # Add to calendar and download buttons
                    st.markdown('<div class="button-container">', unsafe_allow_html=True)
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.button(f"📅 Add to Calendar", key=f"calendar_{i}")
                    
                    with col2:
                        # Download plan as JSON
                        st.download_button(
                            label=f"⬇️ Download Plan",
                            data=json.dumps({
                                'date': selected_date.isoformat(),
                                'total_duration': plan['total_duration'],
                                'content': [
                                    {k: v for k, v in item.items() if k not in ['genres']}
                                    for item in plan['content']
                                ]
                            }),
                            file_name=f"netflix_marathon_plan_{i+1}.json",
                            mime="application/json",
                            key=f"download_{i}"
                        )
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)  # Close form container

with tab2:
    # Add main section title
    st.markdown('<div class="section-title animated-title">Explore Netflix Content</div>', unsafe_allow_html=True)
    
    # Add descriptive subtitle
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px; color: white;">
        Explore Netflix content by different criteria to better understand what's available.
    </div>
    """, unsafe_allow_html=True)
    
    # Create dropdown for selecting visualization type
    viz_type = st.selectbox(
        "Select Visualization",
        ["Content by Type", "Top Genres", "Content by Rating", "Release Year Trends", "Content by Country"]
    )
    
    # Wrap visualization in loading spinner
    with st.spinner('Loading visualization...'):
        if viz_type == "Content by Type":
            # Aggregate content type counts
            type_counts = df['type'].value_counts().reset_index()
            type_counts.columns = ['Type', 'Count']
            
            # Generate pie chart to visualize content distribution
            fig = px.pie(
                type_counts, 
                values='Count', 
                names='Type',
                title='Netflix Content by Type',
                color_discrete_sequence=['#E50914', '#4CAF50'],  # Custom color scheme
                hole=0.4  # Create donut chart effect
            )
            # Customize chart appearance
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
            # Display detailed content statistics
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            st.markdown(f"""
            ### Content Distribution
            - **Total Movies:** {type_counts[type_counts['Type'] == 'Movie']['Count'].values[0]:,}
            - **Total TV Shows:** {type_counts[type_counts['Type'] == 'TV Show']['Count'].values[0]:,}
            - **Movie to TV Show Ratio:** {type_counts[type_counts['Type'] == 'Movie']['Count'].values[0] / type_counts[type_counts['Type'] == 'TV Show']['Count'].values[0]:.2f}
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
        elif viz_type == "Top Genres":
            # Create cached function to efficiently count genres
            @st.cache_data
            def get_genre_counts(dataframe):
                genre_counts = {}
                for genres_list in dataframe['genres']:
                    if isinstance(genres_list, list):
                        for genre in genres_list:
                            genre_counts[genre] = genre_counts.get(genre, 0) + 1
                return genre_counts
            
            # Calculate genre frequencies
            genre_counts = get_genre_counts(df)
            
            # Convert genre counts to DataFrame for visualization
            genre_df = pd.DataFrame([
                {'Genre': genre, 'Count': count}
                for genre, count in genre_counts.items()
            ]).sort_values('Count', ascending=False).head(15)
            
            # Create horizontal bar chart of top genres
            fig = px.bar(
                genre_df,
                x='Count',
                y='Genre',
                orientation='h',
                title='Top 15 Genres on Netflix',
                color='Count',
                color_continuous_scale=['#E50914', '#EE4C0E', '#FF6B35']  # Gradient color scheme
            )
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
            # Create detailed genre breakdown
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            st.markdown("### Top Genres by Content Type")
            
            # Split view for movie and TV show genres
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Movies")
                # Count genres specifically for movies
                movie_genres = {}
                for _, row in df[df['type'] == 'Movie'].iterrows():
                    if isinstance(row['genres'], list):
                        for genre in row['genres']:
                            movie_genres[genre] = movie_genres.get(genre, 0) + 1
                
                # Prepare movie genre DataFrame
                movie_genre_df = pd.DataFrame([
                    {'Genre': genre, 'Count': count}
                    for genre, count in movie_genres.items()
                ]).sort_values('Count', ascending=False).head(10)
                
                # Visualize movie genres
                fig = px.bar(
                    movie_genre_df,
                    x='Count',
                    y='Genre',
                    orientation='h',
                    color='Count',
                    color_continuous_scale=['#E50914', '#FF6B35'],
                    height=400
                )
                fig.update_layout(template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### TV Shows")
                # Count genres specifically for TV shows
                tv_genres = {}
                for _, row in df[df['type'] == 'TV Show'].iterrows():
                    if isinstance(row['genres'], list):
                        for genre in row['genres']:
                            tv_genres[genre] = tv_genres.get(genre, 0) + 1
                
                # Prepare TV show genre DataFrame
                tv_genre_df = pd.DataFrame([
                    {'Genre': genre, 'Count': count}
                    for genre, count in tv_genres.items()
                ]).sort_values('Count', ascending=False).head(10)
                
                # Visualize TV show genres
                fig = px.bar(
                    tv_genre_df,
                    x='Count',
                    y='Genre',
                    orientation='h',
                    color='Count',
                    color_continuous_scale=['#E50914', '#FF6B35'],
                    height=400
                )
                fig.update_layout(template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        elif viz_type == "Content by Rating":
            # Aggregate content ratings
            rating_counts = df['rating'].value_counts().reset_index()
            rating_counts.columns = ['Rating', 'Count']
            rating_counts = rating_counts.sort_values('Count', ascending=False)
            
            # Create bar chart of overall ratings
            fig = px.bar(
                rating_counts,
                x='Rating',
                y='Count',
                title='Netflix Content by Rating',
                color='Count',
                color_continuous_scale=['#E50914', '#EE4C0E', '#FF6B35']
            )
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
            # Split view for movie and TV show ratings
            col1, col2 = st.columns(2)
            
            with col1:
                # Process movie ratings
                movie_ratings = df[df['type'] == 'Movie']['rating'].value_counts().reset_index()
                movie_ratings.columns = ['Rating', 'Count']
                movie_ratings = movie_ratings.sort_values('Count', ascending=False)
                
                # Pie chart of top movie ratings
                fig = px.pie(
                    movie_ratings.head(5),
                    values='Count',
                    names='Rating',
                    title='Top 5 Ratings for Movies',
                    color_discrete_sequence=['#E50914', '#4CAF50', '#EE4C0E', '#1E88E5', '#FF6B35'],
                    hole=0.3
                )
                fig.update_layout(template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Process TV show ratings
                tv_ratings = df[df['type'] == 'TV Show']['rating'].value_counts().reset_index()
                tv_ratings.columns = ['Rating', 'Count']
                tv_ratings = tv_ratings.sort_values('Count', ascending=False)
                
                # Pie chart of top TV show ratings
                fig = px.pie(
                    tv_ratings.head(5),
                    values='Count',
                    names='Rating',
                    title='Top 5 Ratings for TV Shows',
                    color_discrete_sequence=['#E50914', '#4CAF50', '#FFA500', '#1E88E5', '#FF6B35'],
                    hole=0.3
                )
                fig.update_layout(template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Release Year Trends":
            # Aggregate content by release year
            year_counts = df.groupby('release_year').size().reset_index(name='Count')
            
            # Create line chart of content over time
            fig = px.line(
                year_counts,
                x='release_year',
                y='Count',
                title='Netflix Content by Release Year',
                markers=True,
                line_shape='spline'
            )
            fig.update_traces(line=dict(color='#58D68D', width=3))
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
            # Create container for additional year-based insights
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            st.markdown("### Content Release Years by Type")
            
            # Box plot to show distribution of release years
            fig = px.box(
                df,
                x='type',
                y='release_year',
                color='type',
                title='Distribution of Release Years by Content Type',
                labels={'type': 'Content Type', 'release_year': 'Release Year'},
                color_discrete_map={'Movie': '#E50914', 'TV Show': '#FF6B35'}
            )
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
            # Recent trends section
            st.markdown("### Recent Trends (Last 20 Years)")
            
            # Filter and process recent content
            recent_df = df[df['release_year'] >= 2000].copy()
            recent_years = recent_df.groupby(['release_year', 'type']).size().reset_index(name='Count')
            
            # Create line chart of recent content trends
            fig = px.line(
                recent_years,
                x='release_year',
                y='Count',
                color='type',
                title='Trends in Netflix Content (2000-Present)',
                markers=True,
                line_shape='spline',
                color_discrete_map={'Movie': '#E50914', 'TV Show': '#FF6B35'}
            )
            fig.update_layout(xaxis_title='Release Year', yaxis_title='Number of Titles')
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        elif viz_type == "Content by Country":
            # Cached function to efficiently count countries
            @st.cache_data
            def get_country_data(dataframe):
                country_counts = {}
                for country_str in dataframe['country'].dropna():
                    if isinstance(country_str, str):
                        for country in country_str.split(','):
                            country = country.strip()
                            country_counts[country] = country_counts.get(country, 0) + 1
                
                # Convert to DataFrame for easy visualization
                country_df = pd.DataFrame([
                    {'Country': country, 'Count': count}
                    for country, count in country_counts.items()
                ]).sort_values('Count', ascending=False)
                
                return country_df
            
            # Get country content distribution
            country_df = get_country_data(df)
            
            # Create horizontal bar chart of top countries
            fig = px.bar(
                country_df.head(15),
                x='Count',
                y='Country',
                orientation='h',
                title='Top 15 Countries by Content Count',
                color='Count',
                color_continuous_scale=['#E50914', '#EE4C0E', '#FF6B35']
            )
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
            # US vs. International content section
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            st.markdown("### US vs. International Content Over Time")
            
            # Categorize content as US or International
            df['is_us'] = df['country'].apply(
                lambda x: 'US' if pd.notna(x) and isinstance(x, str) and 'United States' in x else 'International'
            )
            
            # Process recent content by country
            recent_df = df[df['release_year'] >= 2000].copy()
            us_vs_intl = recent_df.groupby(['release_year', 'is_us']).size().reset_index(name='Count')
            
            # Create line chart of US vs International content
            fig = px.line(
                us_vs_intl,
                x='release_year',
                y='Count',
                color='is_us',
                title='US vs. International Content (2000-Present)',
                markers=True,
                line_shape='spline',
                color_discrete_map={'US': '#E50914', 'International': '#FF6B35'}
            )
            fig.update_layout(xaxis_title='Release Year', yaxis_title='Number of Titles')
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-title animated-title">About This App</div>', unsafe_allow_html=True)  # Add title
    
    st.markdown('<div class="form-container fadeIn">', unsafe_allow_html=True)  # Start form container
    
    # Detailed app description markdown
    st.markdown("""
    ### Netflix Marathon-Watch Planner
    
    This app helps you plan the perfect marathon-watching session based on your available time and content preferences. Instead of spending time browsing through Netflix trying to decide what to watch, let our app create an optimized plan for you!
    
    #### How It Works
    1. **Input your available time** - Tell us how many hours and minutes you have available
    2. **Set your preferences** - Select genres, ratings, and other filters
    3. **Get personalized recommendations** - We'll create multiple marathon plans that fit your time perfectly
    4. **Explore content** - Use the Content Explorer to discover trends and patterns in Netflix content
    
    #### Features
    - **Custom Marathon Plans** - Get plans that maximize your available watching time
    - **Multiple Options** - Compare different combinations of movies and TV shows
    - **Content Insights** - Explore Netflix trends and statistics
    - **Calendar Integration** - Add your marathon plan to your calendar (conceptual feature)
    - **Plan Downloads** - Save your plans for offline reference
    
    #### About the Data
    This app uses a dataset of Netflix content covering movies and TV shows. The dataset includes information such as:
    - Titles and descriptions
    - Content type (Movie or TV Show)
    - Release year
    - Duration information
    - Content ratings
    - Genres
    - Country of origin
    
    #### Netflix & Chill Responsibly
    Remember to take breaks during your marathon-watching sessions! Experts recommend getting up and moving around for at least 5 minutes every hour.
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close first container
    
    # User feedback section
    st.markdown('<div class="form-container fadeIn">', unsafe_allow_html=True)  # Start feedback container
    
    st.markdown("### User Feedback")  # Feedback section title
    
    # Feedback input fields
    feedback = st.text_area("How can we improve this app?", height=100)  # Feedback text input
    rating = st.slider("Rate your experience (1-5 stars)", 1, 5, 5)  # Experience rating
    
    # Feedback submission
    st.markdown('<div class="button-container">', unsafe_allow_html=True)  # Button container
    if st.button("Submit Feedback", key="feedback_button"):  # Feedback submission button
        st.success("Thank you for your feedback! We'll use it to improve the app.")  # Confirmation message
    st.markdown('</div>', unsafe_allow_html=True)  # Close button container
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close feedback container

# Main function placeholder
if __name__ == "__main__":
    pass  # Entry point for potential script execution