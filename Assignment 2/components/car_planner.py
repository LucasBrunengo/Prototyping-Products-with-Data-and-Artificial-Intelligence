"""
Car Planner component for the CarMatch AI app.
"""

import streamlit as st
import time
from utils.helpers import validate_api_key
from utils.cohere_api import get_car_recommendations, generate_sentiment_analysis

def render_api_key_input():
    """
    Render the API key input section.
    """
    # Create a container just for the API key input
    with st.container():
        # Add styling for this container if needed
        st.markdown("""
            <style>
            .api-key-container {
                background-color: rgba(20, 20, 20, 0.8);
                padding: 20px;
                border-radius: 10px;
                margin: 20px auto;
                max-width: 70%;
            }
            </style>
            """, unsafe_allow_html=True)
    
    # API key input
    api_key = st.text_input("Cohere API Key", value=st.session_state.get('api_key', ''), 
                          type="password", 
                          help="Enter your Cohere API key to get started. You can get one from cohere.ai")
    
    # Validate key button
    if st.button("Validate API Key", key="validate_key_button"):
        if api_key:
            with st.spinner("Validating API key..."):
                if validate_api_key(api_key):
                    st.session_state.api_key = api_key
                    st.success("✅ Valid Cohere API key!")
                    # Use st.rerun() instead of st.experimental_rerun()
                    st.rerun()
                # Error messages are shown by the validation function
        else:
            st.error("Please enter an API key.")

def render_buyer_profile():
    """
    Render the buyer profile section.
    """
    st.markdown("<h1 style='text-align: center; font-size: 3rem;'>Your Driver Profile</h1>", unsafe_allow_html=True)
    st.markdown('<div class="section-container driver-profile-section">', unsafe_allow_html=True)
    
    # Buyer Profile section
    if st.session_state.persona:
        # Center the "Lifestyle & Motivations" title across the entire page
        st.markdown("<h2 style='text-align: center; font-size: 2rem;'>Lifestyle & Motivations</h2>", unsafe_allow_html=True)
        
        # Create a horizontal layout for lifestyle and motivations
        col1, col2 = st.columns(2)
        
        with col1:
            # Lifestyle content
            lifestyle = "Not available"
            if 'lifestyle' in st.session_state.persona and st.session_state.persona['lifestyle']:
                lifestyle = st.session_state.persona['lifestyle']
            
            st.markdown(f"""
            <div>
            <strong>Lifestyle:</strong><br>
            {lifestyle}
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # Motivations content
            motivations = "Not available"
            if 'motivations' in st.session_state.persona and st.session_state.persona['motivations']:
                motivations = st.session_state.persona['motivations']
            
            st.markdown(f"""
            <div>
            <strong>Motivations:</strong><br>
            {motivations}
            </div>
            """, unsafe_allow_html=True)
        
        # Center the "Priorities" title
        st.markdown("<h2 style='text-align: center; font-size: 2rem;'>Priorities</h2>", unsafe_allow_html=True)
        
        # Create a horizontal layout for priorities
        col1, col2 = st.columns(2)
        
        with col1:
            # Key priorities content
            key_priorities = "Not available"
            if 'key_priorities' in st.session_state.persona:
                if isinstance(st.session_state.persona['key_priorities'], list):
                    key_priorities = "<br>".join([f"• {priority}" for priority in st.session_state.persona['key_priorities']])
                elif st.session_state.persona['key_priorities']:
                    key_priorities = f"• {st.session_state.persona['key_priorities']}"
            
            st.markdown(f"""
            <div>
            <strong>Key Priorities:</strong><br>
            {key_priorities}
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # Secondary considerations content
            secondary = "Not available"
            if 'secondary_considerations' in st.session_state.persona:
                if isinstance(st.session_state.persona['secondary_considerations'], list):
                    secondary = "<br>".join([f"• {consideration}" for consideration in st.session_state.persona['secondary_considerations']])
                elif st.session_state.persona['secondary_considerations']:
                    secondary = f"• {st.session_state.persona['secondary_considerations']}"
            
            st.markdown(f"""
            <div>
            <strong>Secondary Considerations:</strong><br>
            {secondary}
            </div>
            """, unsafe_allow_html=True)

def render_car_recommendations():
    """
    Render the car recommendations section.
    """
    st.markdown('<div class="section-container recommendations-section">', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 3rem;'>Your Car Recommendation</h1>", unsafe_allow_html=True)
    st.markdown('<div class="section-container driver-profile-section">', unsafe_allow_html=True)
    
    # Create car recommendation cards
    cols = st.columns(3)

    # Display each car recommendation in its own column
    for i, recommendation in enumerate(st.session_state.recommendations[:3]):
        with cols[i]:
            # Calculate match score for this recommendation
            match_score = min(int(recommendation.get('match_score', 50)), 100)
            
            # Car title - these are already aligned
            st.markdown(f"""
                <h3 style="color: #E50914; width: 250px; text-align: left; margin-right: 100px; margin-bottom: 5px; height: 30px;">{recommendation['make_model']}</h3>
            """, unsafe_allow_html=True)
            
            # Add proper space BETWEEN title and car type
            st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

            # Car type with fixed height
            st.markdown(f'<p class="car-type">{recommendation["body_type"]}</p>', unsafe_allow_html=True)
            
            # Match score with formatted percentage
            st.markdown(f"""
                <div class="match-score">
                    {match_score}% Match
                </div>
            """, unsafe_allow_html=True)
            
            # Price tag
            st.markdown(f"""
                <div style="background-color: #E50914; color: white; display: inline-block;
                        padding: 5px 10px; border-radius: 4px; font-weight: 600; margin-bottom: 15px;">
                    ${recommendation['price']:,}
                </div>
            """, unsafe_allow_html=True)
            
            # Car description with FIXED height (important for alignment)
            st.markdown(f"""
                <div style="color: #DDDDDD; margin-bottom: 20px; height: 500px; overflow: auto;">
                    {recommendation['description']}
                </div>
            """, unsafe_allow_html=True)
            

    # Now, create a new row of columns for the specifications (this ensures they align)
    spec_cols = st.columns(3)

    for i, recommendation in enumerate(st.session_state.recommendations[:3]):
        with spec_cols[i]:
            # Key specifications section
            st.markdown("<h4>Key Specifications</h4>", unsafe_allow_html=True)
            
            # Specifications in a table format
            specs = [
                ("Year", recommendation['year']),
                ("Fuel", recommendation['fuel']),
                ("Transmission", recommendation['transmission']),
                ("Power", f"{recommendation['hp']} HP"),
                ("Mileage", f"{int(recommendation['mileage']):,} mi")
            ]
            
            # Create table with only 3 vertical lines
            st.markdown("""
            <style>
            .clean-table {
                width: 100%;
                color: #DDDDDD;
                border-collapse: collapse;
            }
            .clean-table td {
                padding: 8px;
                border: none;
            }
            .spec-label {
                background-color: #B30000;
                color: white;
                font-weight: 600;
                width: 50%;
                text-align: left;
                padding-left: 15px;
            }
            .spec-value {
                background-color: #1A1A1A;
                width: 50%;
                font-weight: 600;
                text-align: left;
                padding-left: 15px;
            }
            .clean-table {
                border-left: 1px solid #444;
                border-right: 1px solid #444;
            }
            .clean-table tr:first-child td {
                border-top: 1px solid #444;
            }
            .clean-table tr:last-child td {
                border-bottom: 1px solid #444;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown("<table class='clean-table'>", unsafe_allow_html=True)
            for label, value in specs:
                st.markdown(f"""
                    <tr>
                        <td class='spec-label'>{label}</td>
                        <td class='spec-value'>{value}</td>
                    </tr>
                """, unsafe_allow_html=True)
            st.markdown("</table>", unsafe_allow_html=True)

    # Another row for features
    feature_cols = st.columns(3)

    for i, recommendation in enumerate(st.session_state.recommendations[:3]):
        with feature_cols[i]:
            # Features section
            st.markdown("<h4 style='margin-top:15px'>Top Features</h4>", unsafe_allow_html=True)
            
            # Display a mix of features
            features_shown = set()
            feature_count = 0
            
            # Helper to create feature tags for display
            def create_feature_tag(feature):
                return f"<span class='feature-tag'>{feature}</span>"
            
            # Display comfort features first
            if 'comfort_features' in recommendation and recommendation['comfort_features']:
                for feature in recommendation['comfort_features'][:2]:
                    if feature and feature not in features_shown:
                        st.markdown(create_feature_tag(feature), unsafe_allow_html=True)
                        features_shown.add(feature)
                        feature_count += 1
            
            # Display safety features next
            if 'safety_features' in recommendation and recommendation['safety_features']:
                for feature in recommendation['safety_features'][:2]:
                    if feature_count >= 5:
                        break
                    if feature and feature not in features_shown:
                        st.markdown(create_feature_tag(feature), unsafe_allow_html=True)
                        features_shown.add(feature)
                        feature_count += 1
            
            # Display entertainment features last
            if 'entertainment_features' in recommendation and recommendation['entertainment_features']:
                for feature in recommendation['entertainment_features'][:2]:
                    if feature_count >= 5:
                        break
                    if feature and feature not in features_shown:
                        st.markdown(create_feature_tag(feature), unsafe_allow_html=True)
                        features_shown.add(feature)
                        feature_count += 1

def render_explanation_section():
    """
    Render the explanation section with "Why These Cars Are Perfect For You" button.
    """
    # Explanation button and section
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-container driver-profile-section">', unsafe_allow_html=True)
    if st.button("Why These Cars Are Perfect For You", key="explain_button"):
        st.session_state.loading_analysis = True
        
        # Generate explanation
        with st.spinner("Analyzing your preferences..."):
            analysis = generate_sentiment_analysis()
            st.session_state.sentiment_analysis = analysis
            
            # Simulating processing time for better UX
            time.sleep(1)
            
            st.session_state.loading_analysis = False
            
            # Rerun to show the analysis
            st.rerun()
    
    # Display the analysis if available
    if 'sentiment_analysis' in st.session_state and st.session_state.sentiment_analysis:
        st.markdown('<div class="section-title animated-title">Why These Cars Match Your Needs</div>', unsafe_allow_html=True)
        st.write(st.session_state.sentiment_analysis)

def render_questionnaire_form():
    """
    Render the questionnaire form.
    """
    # Passengers input - modified to ask for maximum passengers
    st.markdown('<div class="input-item">', unsafe_allow_html=True)
    st.markdown('<div class="section-title animated-title">Passenger Capacity</div>', unsafe_allow_html=True)
    passengers = st.number_input("What is the maximum number of passengers you need to accommodate?", 1, 12, value=st.session_state.form_passengers)
    st.session_state.form_passengers = passengers
    st.session_state.answers['passengers'] = passengers
    
    # Budget input
    st.markdown('<div class="input-item">', unsafe_allow_html=True)
    st.markdown('<div class="section-title animated-title">Budget</div>', unsafe_allow_html=True)

    # Define budget options
    budget_options = [5000, 10000, 15000, 20000, 25000, 30000, 40000, 50000, 60000, 75000, 100000, 150000, 200000, 300000, 500000]
    
    col1, col2 = st.columns(2)
    with col1:
        min_budget = st.selectbox("Minimum (USD)", budget_options, index=budget_options.index(st.session_state.form_min_budget) if st.session_state.form_min_budget in budget_options else 0)
    
    with col2:
        # Filter max budget options to be greater than or equal to min budget
        max_budget_options = [b for b in budget_options if b >= min_budget]
        
        # Find the index of current max budget in filtered options
        try:
            max_index = max_budget_options.index(st.session_state.form_max_budget)
        except ValueError:
            max_index = 0
            
        max_budget = st.selectbox("Maximum (USD)", max_budget_options, index=max_index)
    
    st.session_state.form_min_budget = min_budget
    st.session_state.form_max_budget = max_budget
    st.session_state.answers['budget'] = (min_budget, max_budget)
    
    # Car Type input
    st.markdown('<div class="input-item">', unsafe_allow_html=True)
    st.markdown('<div class="section-title animated-title">Car Type</div>', unsafe_allow_html=True)
    car_type = st.selectbox("Select preferred type", ["New", "Used", "No preference"], index=["New", "Used", "No preference"].index(st.session_state.form_car_type) if st.session_state.form_car_type in ["New", "Used", "No preference"] else 0)
    st.session_state.form_car_type = car_type
    st.session_state.answers['car_type'] = car_type  
    
    # Second row of inputs
    
    # Fuel type
    st.markdown('<div class="input-item">', unsafe_allow_html=True)
    st.markdown('<div class="section-title animated-title">Fuel Type</div>', unsafe_allow_html=True)
    fuel_options = ["Gasoline", "Diesel", "Electric", "Hybrid", "Plug-in Hybrid", "No preference"]
    fuel = st.selectbox("Select fuel preference", fuel_options, index=fuel_options.index(st.session_state.form_fuel) if st.session_state.form_fuel in fuel_options else 0)
    st.session_state.form_fuel = fuel
    st.session_state.answers['fuel'] = fuel
    
    # Vehicle Use input - Add after Transmission type
    st.markdown('<div class="input-item">', unsafe_allow_html=True)
    st.markdown('<div class="section-title animated-title">Primary Vehicle Use</div>', unsafe_allow_html=True)
    use_options = ["Daily Commuting", "Family Trips", "Off-Road Adventures", "Business Travel", 
                "Urban Driving", "Long Distance Travel", "Weekend Recreation"]
    vehicle_use = st.selectbox("What will you primarily use this car for?", use_options)
    st.session_state.form_vehicle_use = vehicle_use if 'form_vehicle_use' in st.session_state else "Daily Commuting"
    st.session_state.answers['vehicle_use'] = vehicle_use

    # Vehicle Longevity - Add after Vehicle Use
    st.markdown('<div class="input-item">', unsafe_allow_html=True)
    st.markdown('<div class="section-title animated-title">Ownership Period</div>', unsafe_allow_html=True)
    longevity_options = ["Brand New", "1-2 years", "3-5 years", "5-10 years", "10+ years"]
    expected_ownership = st.selectbox("How long do you plan to keep this vehicle?", longevity_options)
    st.session_state.form_expected_ownership = expected_ownership if 'form_expected_ownership' in st.session_state else "3-5 years"
    st.session_state.answers['expected_ownership'] = expected_ownership

    # Parking Situation - Add after Vehicle Longevity
    st.markdown('<div class="input-item">', unsafe_allow_html=True)
    st.markdown('<div class="section-title animated-title">Parking Situation</div>', unsafe_allow_html=True)
    parking_options = ["Street Parking", "Small Garage/Tight Spaces", "Standard Garage", "Spacious Parking Available"]
    parking_situation = st.selectbox("What is your typical parking situation?", parking_options)
    st.session_state.form_parking_situation = parking_situation if 'form_parking_situation' in st.session_state else "Standard Garage"
    st.session_state.answers['parking_situation'] = parking_situation

    # Performance vs Economy
    st.markdown('<div class="input-item">', unsafe_allow_html=True)
    st.markdown('<div class="section-title animated-title">Priority</div>', unsafe_allow_html=True)
    priority_options = ["Economy", "Balanced", "Performance"]
    priority = st.select_slider("Economy vs Performance", priority_options, value=st.session_state.form_priority)
    st.session_state.form_priority = priority
    st.session_state.answers['priority'] = priority
    
    # Transmission type
    st.markdown('<div class="input-item">', unsafe_allow_html=True)
    st.markdown('<div class="section-title animated-title">Transmission</div>', unsafe_allow_html=True)
    transmission_options = ["Automatic", "Manual", "Semi-automatic", "No preference"]
    transmission = st.selectbox("Select transmission type", transmission_options, index=transmission_options.index(st.session_state.form_transmission) if st.session_state.form_transmission in transmission_options else 0)
    st.session_state.form_transmission = transmission
    st.session_state.answers['transmission'] = transmission
    
    
    # Features selection
    st.markdown('<div class="input-item">', unsafe_allow_html=True)
    st.markdown('<div class="section-title animated-title">Important Features</div>', unsafe_allow_html=True)
    
    # List of possible car features
    features = [
        "Fuel efficiency", "Comfort", "Safety features", "Advanced technology",
        "Performance", "Reliability", "Low maintenance", "Interior space",
        "Aesthetics/style", "Brand reputation", "Resale value", "Environmental impact"
    ]
    
    # Create 3 columns for feature selection
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # First feature selection
        feature1 = st.selectbox("1st most important", features, index=features.index(st.session_state.form_feature1) if st.session_state.form_feature1 in features else 0)
    
    with col2:
        # Second feature selection (remove first selection from options)
        features2 = [f for f in features if f != feature1]
        feature2_index = features2.index(st.session_state.form_feature2) if st.session_state.form_feature2 in features2 else 0
        feature2 = st.selectbox("2nd most important", features2, index=feature2_index)
    
    with col3:
        # Third feature selection (remove first two selections from options)
        features3 = [f for f in features2 if f != feature2]
        feature3_index = features3.index(st.session_state.form_feature3) if st.session_state.form_feature3 in features3 else 0
        feature3 = st.selectbox("3rd most important", features3, index=feature3_index)
    
    st.session_state.form_feature1 = feature1
    st.session_state.form_feature2 = feature2
    st.session_state.form_feature3 = feature3
    st.session_state.answers['top_features'] = [feature1, feature2, feature3]

    # Get recommendations button
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("Find My Perfect Car Match", type="primary", key="find_cars_button", help="Click to get personalized car recommendations"):
        with st.spinner('Finding your perfect car match...'):
            # Start loading indicator
            st.session_state.loading_recommendations = True
            
            # Generate recommendations
            get_car_recommendations()
            
            # Simulating some processing time for better UX
            time.sleep(2)
            
            # Turn off loading state
            st.session_state.loading_recommendations = False
            
            # Rerun the app to refresh the display
            st.rerun()

def render_car_planner():
    """
    Render the Car Planner tab.
    """
    # API Key section - only show if not validated
    if not st.session_state.api_key_valid:
        render_api_key_input()
    
    # Only proceed if API key is valid
    elif st.session_state.api_key_valid:
        # Check if we have recommendations already
        if st.session_state.recommendations:
            # RECOMMENDATIONS DISPLAY SECTION
            # Display the Driver Profile, Car Recommendations, etc.
            render_buyer_profile()
            render_car_recommendations()
            render_explanation_section()
            
            # Add a "Start Over" button to allow users to return to the form
            if st.button("Start Over", key="start_over_button"):
                # Clear recommendations to show the form again
                st.session_state.recommendations = []
                st.rerun()
        
        else:
            # FORM SECTION - Only shown when no recommendations exist
            render_questionnaire_form()