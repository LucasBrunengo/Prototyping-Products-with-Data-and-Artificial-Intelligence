"""
Functions for interacting with the Cohere API.
"""

import streamlit as st
import json
import traceback

def generate_buyer_persona():
    """
    Use Cohere to generate a buyer persona based on questionnaire responses.
    """
    # Skip if Cohere client not initialized
    if not st.session_state.co:
        st.error("Cannot generate persona without a valid Cohere API key.")
        return
    
    # Convert answers to a text description for Cohere
    answers_text = json.dumps(st.session_state.answers, indent=2)
    
    # Create a more reliable prompt for Cohere to generate a buyer persona
    prompt = f"""
You are an automotive marketing expert who specializes in creating buyer personas. Based on the following car buying questionnaire responses, create a detailed buyer persona.

QUESTIONNAIRE RESPONSES:
{answers_text}

TASK:
Create a buyer persona with the following fields:
1. lifestyle: The user's lifestyle profile, including daily activities, family situation, and relevant hobbies
2. motivations: The main reasons why this user is looking to buy a car and their key motivations
3. key_priorities: List of 3-4 key priorities this user has when selecting a vehicle
4. secondary_considerations: List of 2-3 secondary factors the user considers important
5. budget_sensitivity: How price-sensitive this user appears to be (High, Medium, or Low)

IMPORTANT INSTRUCTIONS:
- Consider all information, especially the vehicle use, ownership period, and parking situation
- Pay special attention to how the primary vehicle use (e.g., Family Trips, Off-Road, etc.) shapes their needs. The Weekends recreation could be for family trips, couple trips, off-road adventures or performance tests. Depends on the features that the persona is looking for (eg: Weeken recreation, 2 passengers max and looking for perfomance means a persona that is looking to take his sport car for a test drive over the weekend).
- Consider how long they plan to keep the vehicle and how that affects their priorities
- Factor in their parking situation and how that influences vehicle size requirements
- Even with limited information, create a complete and plausible persona
- Use typical car buyer profiles to fill in any gaps in the information
- If a field is unclear from the data, make a reasonable inference based on other answers
- Respond only with a valid JSON object containing all five fields
- Keep descriptions brief but insightful - 1-2 sentences per field
- Do not use "Not available" or placeholder text - provide actual content for each field
- Focus on the specific preferences mentioned in their answers

OUTPUT FORMAT:
{{
  "lifestyle": "Brief description of user lifestyle",
  "motivations": "Specific reasons for buying a car",
  "key_priorities": ["Priority 1", "Priority 2", "Priority 3"],
  "secondary_considerations": ["Consideration 1", "Consideration 2"],
  "budget_sensitivity": "Medium"
}}
"""

    try:
        # Call Cohere API with improved parameters
        response = st.session_state.co.generate(
            prompt=prompt,
            max_tokens=800,
            temperature=0.7,
            model='command',
            p=0.9,  # Use nucleus sampling for more creative but controlled responses
        )
        
        # Extract JSON from the response
        persona_text = response.generations[0].text
        start_idx = persona_text.find('{')
        end_idx = persona_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx != -1:
            json_str = persona_text[start_idx:end_idx]
            try:
                # Parse the JSON response
                persona = json.loads(json_str)
                st.session_state.persona = persona
            except json.JSONDecodeError as e:
                st.error(f"Could not parse buyer persona. Error: {str(e)}")
                st.session_state.persona = {}
        else:
            st.error("Could not extract buyer persona from Cohere response.")
            st.session_state.persona = {}
    except Exception as e:
        st.error(f"Error generating buyer persona: {str(e)}")
        st.session_state.persona = {}

def extract_feature_importance():
    """
    Use Cohere to extract which car features are most important to the user.
    """
    # Skip if Cohere client not initialized
    if not st.session_state.co:
        st.error("Cannot analyze feature importance without a valid Cohere API key.")
        return
    
    # Convert answers to a text description for Cohere
    answers_text = json.dumps(st.session_state.answers, indent=2)
    
    # Create the prompt for Cohere
    prompt = f"""
Based on this buyer's questionnaire responses:
{answers_text}

Analyze what car features would be most important to this buyer.
Search online for the features of the car recommended by the Cohere API and use them to create a list of features that are most important to this buyer.
Return a JSON object with three ranked lists of specific features (from most to least important) for each category:
1. comfort_features: List of 5 comfort and convenience features
2. entertainment_features: List of 5 entertainment and technology features 
3. safety_features: List of 5 safety and security features

The response should be a valid JSON object with these three arrays.
"""

    try:
        # Call Cohere API to extract feature importance
        response = st.session_state.co.generate(
            prompt=prompt,
            max_tokens=600,
            temperature=0.7,
        )
        
        # Extract JSON from the response
        importance_text = response.generations[0].text
        start_idx = importance_text.find('{')
        end_idx = importance_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx != -1:
            json_str = importance_text[start_idx:end_idx]
            try:
                # Parse the JSON response
                feature_importance = json.loads(json_str)
                st.session_state.feature_importance = feature_importance
            except json.JSONDecodeError as e:
                st.error(f"Could not parse feature importance. Error: {str(e)}")
                st.session_state.feature_importance = {}
        else:
            st.error("Could not extract feature importance from Cohere response.")
            st.session_state.feature_importance = {}
    except Exception as e:
        st.error(f"Error extracting feature importance: {str(e)}")
        st.session_state.feature_importance = {}

def get_car_recommendations():
    """
    Use Cohere to generate car recommendations based on user preferences.
    """
    # Check if Cohere client is initialized
    if not st.session_state.co:
        st.error("Cannot generate recommendations without a valid Cohere API key.")
        return
    
    # Generate buyer persona using Cohere
    generate_buyer_persona()
    
    # Extract feature importance using Cohere
    extract_feature_importance()
    
    # Convert answers to a text description for Cohere
    answers_text = json.dumps(st.session_state.answers, indent=2)
    
    # Create a more detailed and specific prompt for Cohere
    prompt = f"""
You are an expert automotive consultant with detailed knowledge of cars from 2010-2024. Your task is to recommend 3 specific vehicles based on a customer's preferences.

CUSTOMER PREFERENCES:
{answers_text}

CUSTOMER PERSONA:
{json.dumps(st.session_state.persona, indent=2)}

FEATURE PRIORITIES:
{json.dumps(st.session_state.feature_importance, indent=2)}

INSTRUCTIONS:
1. Analyze the customer's preferences carefully
2. Consider their budget range, passenger needs, fuel preferences, and transmission preferences as HARD requirements. Always respect these constraints. THE BUDGET MUST BE RESPECTED AT ALL TIMES.
3. Pay special attention to their primary vehicle use (e.g., Daily Commuting, Family Trips, Off-Road Adventures, etc.)
4. Consider their expected ownership period when recommending vehicle reliability and longevity
5. Factor in their parking situation when considering vehicle size and maneuverability
6. Search for real car models that precisely match these requirements
7. Prioritize vehicles that align with their top features and driving priorities
8. Consider the persona information to find cars that match their lifestyle

For each recommended car, provide the following specifications in a structured JSON format:

REQUIRED FIELDS:
- make_model: Full make and model with trim level if relevant (eg: BWM M24OI G42)
- body_type: The exact body style
- price: The typical market price in USD as an integer (must be within the customer's budget range)
- fuel: The exact fuel type
- transmission: The exact transmission type
- year: The specific model year as an integer (between 2010-2024)
- hp: The horsepower rating as an integer
- mileage: For used cars, typical mileage in miles as an integer; for new cars, use 0
- description: 2-3 sentences explaining why this specific car is recommended based on the user's preferences
- comfort_features: List of 5 specific comfort features this exact car model has
- entertainment_features: List of 5 specific entertainment/technology features this exact car model has
- safety_features: List of 5 specific safety features this exact car model has

IMPORTANT REQUIREMENTS:
- Only recommend REAL car models with ACCURATE specifications. Retrieve the specifications from a reliable source as AutoScout, Edmunds, or Kelley Blue Book.
- Ensure the make_model is the full name including trim level if applicable
- Strictly adhere to the customer's budget range
- Ensure each specification is precise and matches the actual vehicle
- Verify that the fuel type and transmission match customer preferences exactly
- If the customer prefers "New" cars, only recommend current/recent model years with 0 mileage
- If the customer prefers "Used" cars, recommend appropriate model years with realistic mileage
- Consider the primary vehicle use - recommend SUVs or trucks for off-road use, spacious vehicles for family trips, etc.
- Consider parking limitations - for tight parking situations, recommend smaller, more maneuverable vehicles
- Consider ownership period - for longer ownership periods, prioritize reliability and durability
- DO NOT make up features - only include actual features for the specific car model and year

FORMAT YOUR RESPONSE AS A VALID JSON ARRAY WITH 3 CAR OBJECTS.
"""

    try:
        # Call Cohere API with enhanced parameters
        response = st.session_state.co.generate(
            prompt=prompt,
            max_tokens=2500,  # Increased token limit for more detailed responses
            temperature=0.5,   # Slightly lower temperature for more factual responses
            model='command',   # Specify the model explicitly
        )

        
        # Get the raw response text
        raw_response = response.generations[0].text
        
        # Print the raw response for debugging
        print("Raw Cohere Response:")
        print(raw_response)
        
        # More robust JSON extraction using regex
        import re
        
        # Try to extract JSON between first [ and last ]
        json_match = re.search(r'\[.*\]', raw_response, re.DOTALL)
        
        if json_match:
            json_str = json_match.group(0)
            
            try:
                # Parse the JSON response
                cars_data = json.loads(json_str)
                recommendations = []
                
                # Process each recommended car
                for i, car in enumerate(cars_data):
                    # Create recommendation object
                    recommendation = {
                        'make_model': car.get('make_model', 'Unknown Model'),
                        'body_type': car.get('body_type', 'Unknown Type'),
                        'price': car.get('price', 0),
                        'fuel': car.get('fuel', 'Unknown'),
                        'transmission': car.get('transmission', 'Unknown'),
                        'mileage': car.get('mileage', 0),
                        'year': car.get('year', 0),
                        'hp': car.get('hp', 0),
                        'description': car.get('description', 'No description available'),
                        'comfort_features': car.get('comfort_features', []),
                        'entertainment_features': car.get('entertainment_features', []),
                        'safety_features': car.get('safety_features', []),
                        'match_score': 95 - (i * 5)  # 95%, 90%, 85% for the three recommendations
                    }
                    
                    recommendations.append(recommendation)
                
                st.session_state.recommendations = recommendations
            except json.JSONDecodeError as e:
                # Detailed JSON parsing error
                st.error(f"JSON Parsing Error: {str(e)}")
                st.error(f"Problematic JSON string: {json_str}")
                st.session_state.recommendations = []
        else:
            # No valid JSON found
            st.error("Could not extract a valid JSON array from the Cohere response.")
            st.error(f"Full response text: {raw_response}")
            st.session_state.recommendations = []
    except Exception as e:
        # Catch-all error handling
        st.error(f"Comprehensive error generating car recommendations: {str(e)}")
        st.session_state.recommendations = []

def generate_sentiment_analysis():
    """
    Use Cohere to analyze why the recommended cars are the best options for the user.
    If Cohere fails, return an error message.
    
    Returns:
        str: Analysis text from Cohere, or error message if API fails
    """
    # Skip if Cohere client not initialized
    if not st.session_state.co:
        return "Cannot analyze preferences without a valid Cohere API key."
    
    # Skip if there are no recommendations
    if not st.session_state.recommendations:
        return "No recommendations available to analyze."
    
    # Convert answers to a text description for Cohere
    answers_text = json.dumps(st.session_state.answers, indent=2)
    # Create a simplified version of recommendations for the prompt
    recommendations_text = json.dumps([{
        'make_model': r['make_model'],
        'body_type': r['body_type'], 
        'price': r['price'],
        'fuel': r['fuel'],
        'transmission': r['transmission'],
        'year': r['year']
    } for r in st.session_state.recommendations], indent=2)
    
    # Create a comprehensive prompt for sentiment analysis
    prompt = f"""
Perform a detailed analysis on why the recommended cars are perfect matches for this customer based on their questionnaire responses.

USER'S QUESTIONNAIRE RESPONSES:
{answers_text}

TOP CAR RECOMMENDATIONS FOR THIS USER:
{recommendations_text}

USER'S PERSONA:
{json.dumps(st.session_state.persona, indent=2)}

ANALYSIS TASK:
Based on the user's responses, explain why these specific car recommendations are excellent matches. Your analysis should include:

1. How the cars align with the user's primary vehicle use (e.g., family trips, off-road adventures, daily commuting)
2. Why these cars are appropriate for the user's parking situation
3. How the vehicles match the user's expected ownership period (reliability, longevity, etc.)
4. How each car addresses the user's top feature priorities and preferences
5. Why these vehicles represent good value within the user's budget range
6. How each car's characteristics align with the user's lifestyle (as described in the persona)

IMPORTANT INSTRUCTIONS:
- Be specific about how each car's features and capabilities address the user's stated needs
- Explain why these are better choices than other options in the same category
- Use a conversational, enthusiastic tone while maintaining accuracy
- Include concrete examples of how each car would enhance the user's specific use case
- Mention how the recommendations considered all aspects of the user's input
- Keep your analysis focused on practical benefits rather than technical specifications

Provide your analysis in a conversational, engaging tone. Be specific about how each car's features align with the user's stated and implied preferences.
"""

    try:
        # Call Cohere API to generate sentiment analysis
        response = st.session_state.co.generate(
            prompt=prompt,
            max_tokens=1000,  # Increased for more detailed analysis
            temperature=0.7,
        )
        
        # Return the generated analysis
        analysis = response.generations[0].text.strip()
        if not analysis:
            return "We couldn't generate an analysis of your preferences."
        return analysis
    except Exception as e:
        return f"Error analyzing preferences: {str(e)}"