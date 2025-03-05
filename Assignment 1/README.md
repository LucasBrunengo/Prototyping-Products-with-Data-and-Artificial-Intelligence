# Netflix Marathon-Watch Planner

## Overview
The Netflix Marathon-Watch Planner is a Streamlit application that helps users plan optimal marathon-watching sessions based on their available time and content preferences. This app was developed as part of a Streamlit prototyping exercise.

## Features
- **Time-Based Planning**: Input your available hours and minutes to get recommendations that fit your schedule
- **Customizable Filters**: Filter content by genre, rating, release year, and country
- **Multiple Viewing Plans**: Compare different combinations of content
- **Content Exploration**: Visualize Netflix content trends and statistics
- **Download Plans**: Save your marathon plans for later reference

## Unique Widgets Used
1. **Time Input with Hours and Minutes**: Separate number inputs for hours and minutes with combined calculation
2. **Calendar Input with Weekday Display**: Date picker that also shows the corresponding day of the week
3. **Multi-select with Genre Tags**: Select multiple genres with clean tag display
4. **Range Slider for Release Years**: Select a range of years for content filtering
5. **Country Selector with Checkbox Group**: Filter by multiple countries with count information

## Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Make sure you have the Netflix dataset (`netflix_titles.csv`) in the same directory as the "your file app".py file.

3. Run the application:
```bash
streamlit run "your name app".py
```

## Dataset
The application uses the Netflix titles dataset which contains information about movies and TV shows available on Netflix. The dataset includes details such as:
- Show title and description
- Content type (Movie/TV Show)
- Release year
- Rating
- Duration
- Genre information
- Country of origin

## Usage

1. **Plan Your Marathon**:
   - Set your available viewing time
   - Select your preferred date
   - Choose content preferences (genres, ratings, etc.)
   - Click "Find My Marathon Plan" to get recommendations

2. **Explore Content**:
   - View visualizations of Netflix content trends
   - Analyze content by type, genre, rating, release year, and country
   - Discover patterns and interesting insights

3. **About**:
   - Learn more about the app
   - Provide feedback

## Author
Lucas Brunengo
