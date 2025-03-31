"""
Configuration and initialization module for CarMatch AI app.
"""

import streamlit as st
import os
import sys

def load_css(css_file_path):
    """
    Load CSS from a file and return as a string.
    
    Args:
        css_file_path (str): Path to the CSS file
        
    Returns:
        str: CSS content
    """
    try:
        with open(css_file_path, 'r') as f:
            return f.read()
    except Exception as e:
        st.error(f"Error loading CSS file: {str(e)}")
        return ""

def add_bg_from_url():
    """
    Add a semi-transparent overlay to the background
    """
    st.markdown(
        f"""
        <style>
        .stApp {{
            position: relative;
        }}
        .stApp:before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 45%;
            height: 100%;
            background-color: rgba(20, 20, 20, 0.8);
            z-index: 0;
            pointer-events: none;
            border-radius: 10px;
            margin: 20px;
            max-width: 90%;
            left: 27%;
            padding-top: 0 !important;
            margin-top: 0 !important;
        }}
        .stApp > * {{
            position: relative;
            z-index: 1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def initialize_app():
    """
    Initialize the Streamlit app with configurations and session state.
    """
    # Set page configuration for the Streamlit app
    st.set_page_config(
        page_title="CarMatch AI",  # Set the title of the browser tab
        page_icon="🚗",  # Set the icon for the browser tab
        layout="wide",  # Use wide layout to maximize screen space
        initial_sidebar_state="collapsed"  # Start with sidebar collapsed
    )

    # Add the background overlay
    add_bg_from_url()

    # Add CSS
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'style.css')
    st.markdown(f'<style>{load_css(css_path)}</style>', unsafe_allow_html=True)

def initialize_session_state():
    """
    Initialize session state variables if they don't exist
    """
    # API and validation
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ''  # Store Cohere API key
    if 'api_key_valid' not in st.session_state:
        st.session_state.api_key_valid = None  # Store API key validation status
    if 'last_validated_key' not in st.session_state:
        st.session_state.last_validated_key = ''  # Last key that was validated
    
    # Data storage
    if 'answers' not in st.session_state:
        st.session_state.answers = {}  # Store questionnaire answers
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []  # Store car recommendations
    if 'persona' not in st.session_state:
        st.session_state.persona = {}  # Store user persona derived from answers
    if 'feature_importance' not in st.session_state:
        st.session_state.feature_importance = {}  # Store importance of car features
    if 'co' not in st.session_state:
        st.session_state.co = None  # Cohere client instance
    
    # Loading states
    if 'loading_recommendations' not in st.session_state:
        st.session_state.loading_recommendations = False  # Loading state for recommendations
    if 'loading_analysis' not in st.session_state:
        st.session_state.loading_analysis = False  # Loading state for analysis
    if 'sentiment_analysis' not in st.session_state:
        st.session_state.sentiment_analysis = None  # Store sentiment analysis of user preferences

    # Form values
    if 'form_passengers' not in st.session_state:
        st.session_state.form_passengers = 4
    if 'form_min_budget' not in st.session_state:
        st.session_state.form_min_budget = 5000
    if 'form_max_budget' not in st.session_state:
        st.session_state.form_max_budget = 30000
    if 'form_car_type' not in st.session_state:
        st.session_state.form_car_type = "New"
    if 'form_fuel' not in st.session_state:
        st.session_state.form_fuel = "Gasoline"
    if 'form_priority' not in st.session_state:
        st.session_state.form_priority = "Balanced"
    if 'form_transmission' not in st.session_state:
        st.session_state.form_transmission = "Automatic"
    if 'form_feature1' not in st.session_state:
        st.session_state.form_feature1 = "Fuel efficiency"
    if 'form_feature2' not in st.session_state:
        st.session_state.form_feature2 = "Comfort"
    if 'form_feature3' not in st.session_state:
        st.session_state.form_feature3 = "Safety features"