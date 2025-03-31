"""
CarMatch AI - A Streamlit application that uses Cohere's API to recommend cars
based on user preferences through a questionnaire.
"""

import streamlit as st
from utils.config import initialize_app, initialize_session_state
from components.car_planner import render_car_planner
from components.car_explorer import render_car_explorer
from components.about import render_about

def main():
    """
    Main function to run the CarMatch AI app.
    """
    # Initialize the app with configurations
    initialize_app()
    
    # Initialize session state variables
    initialize_session_state()
    
    # Create styled header with logo
    st.markdown(
        '<div class="logo-container"><img src="https://i.ibb.co/KzFPtdxx/CAR-2-Photoroom.png" alt="CarMatch AI Logo"/></div>', 
        unsafe_allow_html=True
    )

    # Add description
    st.markdown('<div class="description">Find your perfect car match based on your lifestyle, preferences, and budget.</div>', unsafe_allow_html=True)

    # Create application tabs
    tab1, tab2, tab3 = st.tabs(["🚘 Car Planner", "📊 Car Explorer", "ℹ️ About"])

    # Render the Car Planner tab
    with tab1:
        render_car_planner()
    
    # Render the Car Explorer tab
    with tab2:
        render_car_explorer()
    
    # Render the About tab
    with tab3:
        render_about()

if __name__ == "__main__":
    main()