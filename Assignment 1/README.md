# Netflix Marathon-Watch Planner

LINK TO THE DEMO: "https://urledu-my.sharepoint.com/:v:/g/personal/lucas_brunengo_alumni_esade_edu/EaTdT9HBhvZNuu42WWOCuz0BRVPqSSnQK9z8RdL_PT27Gg?e=Nzp1oo&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D"

LINK TO GIT HUB REPOSITORY: "https://github.com/LucasBrunengo/Prototyping-Products-with-Data-and-Artificial-Intelligence/tree/main"

## Overview
The Netflix Marathon-Watch Planner is a Streamlit application that helps users plan optimal marathon-watching sessions based on their available time and content preferences. This app intelligently generates viewing plans that fit precisely within your available time, eliminating the endless scrolling and decision paralysis that often comes with choosing what to watch.

## Features
- **Time-Based Planning**: Input your available hours and minutes to get recommendations that fit your schedule
- **Customizable Filters**: Filter content by genre, rating, release year, and country
- **Multiple Mood Selection**: Select multiple moods simultaneously for more nuanced recommendations
- **Multiple Viewing Plans**: Compare different combinations of content across multiple tabs
- **Content Exploration**: Visualize Netflix content trends and statistics
- **Social Sharing**: Share your marathon plans on social media or via link
- **Download Plans**: Save your marathon plans for later reference
- **Accessibility Options**: Customize text size and enable high contrast mode
- **Personalization**: Input your favorite shows for more tailored recommendations
- **Progress Tracking**: Visual indicators of plan generation progress
- **Responsive Design**: Optimized for both desktop and mobile viewing

## Unique Widgets Used
1. **Time Input with Hours and Minutes**: Separate number inputs for hours and minutes with combined calculation
2. **Calendar Input with Weekday Display**: Date picker that also shows the corresponding day of the week
3. **Multi-select with Genre Tags**: Select multiple genres with clean tag display
4. **Multiple Mood Selection**: Choose several moods simultaneously with a custom-styled multiselect component
5. **Range Slider for Release Years**: Select a range of years for content filtering
6. **Country Selector with Checkbox Group**: Filter by multiple countries with count information
7. **Personalization Expander**: Collapsible section for entering favorite shows and uploading viewing history
8. **Accessibility Sidebar**: Customization options for text size and contrast
9. **Social Sharing Buttons**: Integrated Twitter and Facebook sharing capabilities

## Installation

1. Create the required directory structure:
```bash
mkdir -p .streamlit
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Make sure you have the Netflix dataset (`netflix_titles.csv`) in the same directory as the application file.

4. Run the application:
```bash
streamlit run Assignment1.py
```

## Deploying to Streamlit Cloud

To make your application accessible online:

1. Fork or push your code to GitHub
2. Sign up for [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Configure the deployment settings:
   - Main file path: Assignment1.py
   - Python version: 3.9 or 3.10

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
   - Select one or more moods that match how you're feeling
   - Click "Find My Marathon Plan" to get recommendations

2. **Explore Content**:
   - View visualizations of Netflix content trends
   - Analyze content by type, genre, rating, release year, and country
   - Discover patterns and interesting insights

3. **Personalize Your Experience**:
   - Enter shows you've enjoyed to receive similar recommendations
   - Upload your Netflix viewing history for even more tailored suggestions
   - Adjust accessibility settings to match your preferences

4. **Share and Save**:
   - Download your marathon plan as a JSON file
   - Share your plan on social media
   - Add your marathon to your calendar (feature in development)

## Error Handling
The application includes comprehensive error handling to ensure a smooth user experience:
- Friendly error messages for data loading issues
- Fallback options when filters return no results
- Input validation to prevent impossible time configurations
- Graceful handling of all potential runtime exceptions

## Author
Lucas Brunengo
