"""
Car Explorer component for the CarMatch AI app.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from scipy import stats
from utils.helpers import load_car_data

# Define harmonious color palettes
# Sequential palettes for gradient/ordered data
sand_sequential = ['#F5DEB3', '#EADDCA', '#E6C9A3', '#D2B48C', '#C2A278', '#B08F68']
blue_sequential = ['#B8D1DE', '#A5C0CE', '#859FAD', '#6E8B98', '#5A7986', '#476674']
terracotta_sequential = ['#E27D60', '#D76C56', '#C35A49', '#B0493C', '#9E3A2E', '#8C2E22']
pastel_blue_sequential = ['#E0FFFF', '#B0E0E6', '#ADD8E6', '#87CEEB', '#7AB6CC', '#6A9FB5']

# Main mixed palette for categorical data
mixed_palette = [
    '#D2B48C',  # Sand
    '#859FAD',  # Blue sand
    '#E27D60',  # Terracotta
    '#ADD8E6',  # Pastel light blue
    '#E6C9A3',  # Lighter sand
    '#6E8B98',  # Darker blue sand
    '#C35A49',  # Darker terracotta
    '#B0E0E6',  # Another pastel blue
    '#F5DEB3',  # Wheat
    '#A5C0CE'   # Another blue sand
]

def render_popular_car_makes(df):
    """
    Render the Popular Car Makes visualization.
    """
    st.markdown("### Most Popular Car Makes")
    
    # Count the vehicles by make and get top 10
    make_counts = df['make'].value_counts().reset_index()
    make_counts.columns = ['Make', 'Count']
    make_counts = make_counts.head(10)
    
    # Calculate percentage of total
    total_cars = len(df)
    make_counts['Percentage'] = (make_counts['Count'] / total_cars * 100).round(1)
    
    # Create the chart
    fig = px.bar(make_counts, 
                x='Make', 
                y='Count',
                color='Make',
                title="Top 10 Car Makes in the Market",
                color_discrete_sequence=mixed_palette,
                text='Percentage')
    
    # Add percentage labels
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    
    # Update layout for dark theme
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(20,20,20,0.8)",
        paper_bgcolor="rgba(20,20,20,0.8)",
        font=dict(color="white"),
        height=500,
        xaxis_title="Car Make",
        yaxis_title="Number of Vehicles"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add insights
    most_common = make_counts.iloc[0]['Make']
    percentage = make_counts.iloc[0]['Percentage']
    
    st.write(f"**Market insight:** {most_common} is the most common car make, representing {percentage}% of all vehicles in the market.")
    st.write(f"The top three manufacturers ({make_counts.iloc[0]['Make']}, {make_counts.iloc[1]['Make']}, and {make_counts.iloc[2]['Make']}) together account for {make_counts.iloc[0]['Percentage'] + make_counts.iloc[1]['Percentage'] + make_counts.iloc[2]['Percentage']:.1f}% of available vehicles.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_price_by_make(df):
    """
    Render the Price by Make visualization.
    """
    st.markdown("### Price Ranges by Car Make")
    
    # Get top 8 makes for cleaner visualization
    top_makes = df['make'].value_counts().head(8).index.tolist()
    filtered_df = df[df['make'].isin(top_makes)]
    
    # Create box plot
    fig = px.box(filtered_df,
                x='make',
                y='price',
                color='make',
                title="Price Distribution by Car Make",
                labels={'make': 'Make', 'price': 'Price (€)'},
                category_orders={"make": top_makes},
                color_discrete_sequence=mixed_palette)
    
    # Update layout for dark theme
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(20,20,20,0.8)",
        paper_bgcolor="rgba(20,20,20,0.8)",
        font=dict(color="white"),
        height=500,
        showlegend=False  # Hide legend as colors are shown on x-axis
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Calculate median prices
    median_prices = filtered_df.groupby('make')['price'].median().sort_values(ascending=False)
    highest_make = median_prices.index[0]
    highest_price = median_prices.iloc[0]
    lowest_make = median_prices.index[-1]
    lowest_price = median_prices.iloc[-1]
    
    st.write(f"**Price insight:** {highest_make} has the highest median price at €{highest_price:,.0f}, while {lowest_make} is typically more affordable with a median price of €{lowest_price:,.0f}.")
    st.write("This visualization helps you understand how your budget aligns with different car makes. The box plot shows the median (middle line), typical range (box), and outliers (points).")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_price_vs_performance(df):
    """
    Render the Price vs Performance visualization.
    """
    st.markdown("### Price vs. Horsepower Relationship")
    
    # Create a sample for better performance if dataset is large
    if len(df) > 5000:
        sample_df = df.sample(5000, random_state=42)
    else:
        sample_df = df
        
    # Define top 8 makes for color coding (increased from 5 to 8)
    top_makes = df['make'].value_counts().head(8).index.tolist()
    sample_df['make_group'] = sample_df['make'].apply(lambda x: x if x in top_makes else 'Other')
    
    # Define specific high-contrast colors for car brands - added more brands
    brand_colors = {
        'Volkswagen': '#1E88E5',  # Bright blue
        'Skoda': '#D81B60',       # Magenta/pink
        'Renault': '#FFC107',     # Amber/yellow
        'Opel': '#43A047',        # Green
        'Ford': '#FF5722',        # Deep orange
        'BMW': '#9C27B0',         # Purple
        'Mercedes': '#00BCD4',    # Cyan
        'Audi': '#F44336',        # Red
        'Other': '#757575'        # Gray
    }
    
    # Create color list based on the brands in your dataset
    brand_color_list = []
    for make in top_makes + ['Other']:
        if make in brand_colors:
            brand_color_list.append(brand_colors[make])
        else:
            brand_color_list.append(brand_colors['Other'])
    
    # Create scatter plot with custom brand colors
    fig = px.scatter(sample_df,
                x='hp',
                y='price',
                color='make_group',
                opacity=0.7,
                title="Price vs. Horsepower",
                labels={'hp': 'Horsepower', 'price': 'Price (€)', 'make_group': 'Make'},
                color_discrete_sequence=brand_color_list,  # Custom brand colors
                hover_data=['model', 'year', 'mileage'])
    
    # Increase marker size and add outlines for better visibility
    fig.update_traces(marker=dict(size=8, line=dict(width=1, color='DarkSlateGrey')))
    
    # Add trendline
    slope, intercept, r_value, p_value, std_err = stats.linregress(sample_df['hp'], sample_df['price'])
    r_squared = r_value**2
    
    x_range = np.linspace(sample_df['hp'].min(), sample_df['hp'].max(), 100)
    y_range = slope * x_range + intercept
    
    fig.add_scatter(x=x_range, y=y_range, mode='lines', name='Trend',
                line=dict(color='white', width=2, dash='dash'))
    
    # Update layout for dark theme
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(20,20,20,0.8)",
        paper_bgcolor="rgba(20,20,20,0.8)",
        font=dict(color="white"),
        height=600
    )
    
    # Add a unique key to the plotly_chart call
    st.plotly_chart(fig, use_container_width=True, key="price_vs_hp_chart")
    
    # Add insights
    avg_price_per_hp = slope
    
    st.write(f"**Performance insight:** On average, each additional horsepower adds approximately €{avg_price_per_hp:.2f} to a car's price.")
    st.write(f"The correlation between horsepower and price has an R² value of {r_squared:.2f}, showing that {(r_squared*100):.0f}% of price variation can be explained by differences in power.")
    st.write("Higher performance typically comes with a higher price tag, but some makes offer better value for money in terms of performance per euro.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_car_ages(df):
    """
    Render the Car Ages visualization.
    """
    st.markdown("### Car Age Distribution")
    
    # Age distribution
    age_counts = df['age_category'].value_counts().reset_index()
    age_counts.columns = ['Age', 'Count']
    
    # Sort by actual age
    age_order = ['New', '1-3', '3-5', '5-10', '10-15', '15-20', '20+']
    age_counts['Age'] = pd.Categorical(age_counts['Age'], categories=age_order, ordered=True)
    age_counts = age_counts.sort_values('Age')
    
    # Create bar chart with blue sand colors
    fig = px.bar(age_counts,
                x='Age',
                y='Count',
                color='Age',
                title="Car Age Distribution",
                labels={'Age': 'Car Age (years)', 'Count': 'Number of Vehicles'},
                color_discrete_sequence=blue_sequential)
    
    # Update layout for dark theme
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(20,20,20,0.8)",
        paper_bgcolor="rgba(20,20,20,0.8)",
        font=dict(color="white"),
        height=500,
        xaxis={'categoryorder': 'array', 'categoryarray': age_order}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Create a second chart with price by age using terracotta color
    avg_price_by_age = df.groupby('age_category')['price'].median().reset_index()
    avg_price_by_age.columns = ['Age', 'Median Price']
    
    # Sort by actual age
    avg_price_by_age['Age'] = pd.Categorical(avg_price_by_age['Age'], categories=age_order, ordered=True)
    avg_price_by_age = avg_price_by_age.sort_values('Age')
    
    # Create line chart with terracotta
    fig2 = px.line(avg_price_by_age,
                  x='Age',
                  y='Median Price',
                  markers=True,
                  title="Median Price by Car Age",
                  labels={'Age': 'Car Age (years)', 'Median Price': 'Median Price (€)'},
                  color_discrete_sequence=['#E27D60'])  # Terracotta
    
    # Update layout for dark theme
    fig2.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(20,20,20,0.8)",
        paper_bgcolor="rgba(20,20,20,0.8)",
        font=dict(color="white"),
        height=400,
        xaxis={'categoryorder': 'array', 'categoryarray': age_order}
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Calculate depreciation
    if 'New' in avg_price_by_age['Age'].values and '1-3' in avg_price_by_age['Age'].values:
        new_price = avg_price_by_age[avg_price_by_age['Age'] == 'New']['Median Price'].values[0]
        three_year_price = avg_price_by_age[avg_price_by_age['Age'] == '1-3']['Median Price'].values[0]
        
        depreciation_3yr = ((new_price - three_year_price) / new_price) * 100
        
        st.write(f"**Age insight:** Cars typically lose about {depreciation_3yr:.1f}% of their value in the first three years.")
        st.write("Understanding the age distribution and depreciation curve can help you determine the optimal age for a used car purchase, balancing initial cost with remaining useful life.")
    else:
        st.write("**Age insight:** The data shows how car prices depreciate over time.")
        st.write("Understanding this depreciation curve can help you determine the optimal age for a used car purchase, balancing initial cost with remaining useful life.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_transmission_types(df):
    """
    Render the Transmission Types visualization.
    """
    st.markdown("### Transmission Types Analysis")
    
    # Distribution of transmission types
    gear_counts = df['gear'].value_counts().reset_index()
    gear_counts.columns = ['Transmission', 'Count']
    
    # Percentage calculation
    gear_counts['Percentage'] = (gear_counts['Count'] / gear_counts['Count'].sum() * 100).round(1)
    
    # Create figure with subplots: pie chart and average price
    fig = make_subplots(rows=1, cols=2, 
                        specs=[[{"type": "pie"}, {"type": "bar"}]],
                        subplot_titles=("Transmission Type Distribution", 
                                      "Average Price by Transmission Type"))
    
    # Pie chart for distribution with sand colors
    fig.add_trace(
        go.Pie(
            labels=gear_counts['Transmission'],
            values=gear_counts['Count'],
            hole=0.4,
            textinfo='label+percent',
            marker_colors=sand_sequential  # Sand colors
        ),
        row=1, col=1
    )
    
    # Bar chart for average price by transmission with pastel blue
    avg_price = df.groupby('gear')['price'].mean().reset_index()
    avg_price.columns = ['Transmission', 'Average Price']
    
    fig.add_trace(
        go.Bar(
            x=avg_price['Transmission'],
            y=avg_price['Average Price'],
            marker_color=pastel_blue_sequential[0]  # Pastel blue color
        ),
        row=1, col=2
    )
    
    # Update layout for dark theme
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(20,20,20,0.8)",
        paper_bgcolor="rgba(20,20,20,0.8)",
        font=dict(color="white"),
        height=500,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add insights
    most_common = gear_counts.iloc[0]['Transmission']
    most_common_pct = gear_counts.iloc[0]['Percentage']
    
    highest_price_idx = avg_price['Average Price'].idxmax()
    highest_price_trans = avg_price.iloc[highest_price_idx]['Transmission']
    highest_price_value = avg_price.iloc[highest_price_idx]['Average Price']
    
    st.write(f"**Transmission insight:** {most_common} is the most common transmission type, representing {most_common_pct}% of all vehicles in the market.")
    st.write(f"Cars with {highest_price_trans} transmission have the highest average price at €{highest_price_value:,.0f}, which may indicate that this transmission type is more common in premium vehicles.")
    
    # Additional insight about manual vs automatic preferences
    if 'Manual' in gear_counts['Transmission'].values and 'Automatic' in gear_counts['Transmission'].values:
        manual_pct = gear_counts[gear_counts['Transmission'] == 'Manual']['Percentage'].values[0]
        auto_pct = gear_counts[gear_counts['Transmission'] == 'Automatic']['Percentage'].values[0]
        
        if manual_pct > auto_pct:
            st.write(f"Manual transmissions remain popular in the European market, making up {manual_pct}% of vehicles compared to {auto_pct}% for automatic transmissions.")
        else:
            st.write(f"Automatic transmissions are becoming increasingly popular, making up {auto_pct}% of vehicles compared to {manual_pct}% for manual transmissions.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_car_explorer():
    """
    Render the Car Explorer tab.
    """
    st.markdown('<div class="section-title animated-title">Explore Car Data</div>', unsafe_allow_html=True)
    
    # Add descriptive subtitle
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px; color: white;">
        Explore real market data to understand what's available and help inform your car choice.
    </div>
    """, unsafe_allow_html=True)
    
    # Load the car data
    df = load_car_data()
    
    # Create visualization selector
    viz_type = st.selectbox(
        "Select Visualization",
        ["Popular Car Makes", "Price by Make", "Price vs Performance", "Car Ages", "Transmission Types"]
    )
    
    # Render the selected visualization
    if viz_type == "Popular Car Makes":
        render_popular_car_makes(df)
    elif viz_type == "Price by Make":
        render_price_by_make(df)
    elif viz_type == "Price vs Performance":
        render_price_vs_performance(df)
    elif viz_type == "Car Ages":
        render_car_ages(df)
    elif viz_type == "Transmission Types":
        render_transmission_types(df)