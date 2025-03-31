"""
About component for the CarMatch AI app.
"""

import streamlit as st

def render_about():
    """
    Render the About tab.
    """
    # About tab title
    st.markdown('<div class="section-title animated-title">About This App</div>', unsafe_allow_html=True)
    
    # App description
    st.markdown("""
    ### CarMatch AI
    
    This app helps you find your perfect car match based on your lifestyle, preferences, and budget. Using AI-powered recommendations, we analyze your needs and suggest vehicles that would be ideal for you.
    
    #### How It Works
    1. **Enter your preferences** - Tell us about what you're looking for in a car
    2. **AI analysis** - Our AI analyzes your inputs to understand your needs
    3. **Get recommendations** - Receive personalized car suggestions with detailed information
    4. **Explore options** - View features, specifications, and why each car is a good match
    
    #### Features
    - **Personalized Recommendations** - Get car suggestions tailored to your unique needs
    - **Driver Profile** - See an analysis of your driving style and priorities
    - **Detailed Car Information** - View specifications, features, and match scores
    - **Explanations** - Understand why each car matches your preferences
    - **Car Data Explorer** - Discover trends and insights about the car market
    
    #### Technologies Used
    This app uses Cohere's AI to generate personalized recommendations. The AI analyzes your preferences and matches them with vehicle attributes to find the best options for you.
    
    #### Privacy Notice
    Your data is only used to generate recommendations within this application and is not stored or shared.
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # User feedback section
    st.markdown("### User Feedback")
    
    # Feedback input fields
    feedback = st.text_area("How can we improve this app?", height=100)
    rating = st.slider("Rate your experience (1-5 stars)", 1, 5, 5)
    
    # Feedback submission
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("Submit Feedback", key="feedback_button"):
        st.success("Thank you for your feedback! We'll use it to improve the app.")
    
    # Credits and attribution
    st.markdown("### Credits")
    st.markdown("""
    - Powered by [Cohere](https://cohere.ai/) AI technology
    - Developed by CarMatch AI Team
    """)
    st.markdown('</div>', unsafe_allow_html=True)