"""
Helper functions for CarMatch AI app.
"""

import streamlit as st
import cohere
import pandas as pd
import numpy as np
import datetime

def validate_api_key(key):
    """
    Validate the Cohere API key with improved error handling.
    
    Args:
        key (str): The API key to validate
        
    Returns:
        bool: True if key is valid, False otherwise
    """
    # Remove any leading/trailing whitespace
    key = key.strip()
    
    if not key:
        st.session_state.api_key_valid = False
        return False
    
    # Skip validation if we've already validated this key
    if key == st.session_state.last_validated_key and st.session_state.api_key_valid is not None:
        return st.session_state.api_key_valid
    
    # Store this key as the last one we validated
    st.session_state.last_validated_key = key
    
    try:
        # Try to initialize a Cohere client with the provided key
        client = cohere.Client(key)
        
        # Try a simple API call to validate the key
        response = client.generate(
            prompt="Validate API key",
            max_tokens=10,
            temperature=0.1,
            model='command'
        )
        
        # If we get here, the key is valid
        st.session_state.co = client  # Save the client for future use
        st.session_state.api_key_valid = True
        return True
    except Exception as e:
        # Provide more specific error feedback
        error_msg = str(e)
        if "Unauthorized" in error_msg:
            st.error("Invalid API key. Please check your Cohere API key.")
        elif "connection" in error_msg.lower():
            st.error("Network error. Please check your internet connection.")
        else:
            st.error(f"API validation error: {error_msg}")
        
        # Reset session state
        st.session_state.co = None
        st.session_state.api_key_valid = False
        return False

@st.cache_data
def load_car_data():
    """
    Load and process the car dataset from the CSV file.
    
    Returns:
        pd.DataFrame: The processed car dataset
    """
    # Load the dataset
    df = pd.read_csv('autoscout24-germany-dataset.csv')
    
    # Basic data cleaning
    # Filter out outliers (cars with extremely high prices or likely data errors)
    df = df[df['price'] < 500000]
    df = df[df['price'] > 500]  # Remove extremely low prices (likely errors)
    
    # Filter out extreme mileage values
    df = df[df['mileage'] < 500000]  # Remove extremely high mileage
    
    # Convert year to age
    current_year = datetime.datetime.now().year
    df['age'] = current_year - df['year']
    
    # Add age categories for better visualization
    df['age_category'] = pd.cut(df['age'], 
                                bins=[-1, 1, 3, 5, 10, 15, 20, 100],
                                labels=['New', '1-3', '3-5', '5-10', '10-15', '15-20', '20+'])
    
    # Create price categories for grouping
    price_bins = [0, 10000, 20000, 30000, 50000, 75000, 100000, 1000000]
    price_labels = ['< €10K', '€10K-€20K', '€20K-€30K', '€30K-€50K', '€50K-€75K', '€75K-€100K', '> €100K']
    df['price_category'] = pd.cut(df['price'], bins=price_bins, labels=price_labels)
    
    return df