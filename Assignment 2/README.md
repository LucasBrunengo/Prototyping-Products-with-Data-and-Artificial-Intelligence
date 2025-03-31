# CarMatch AI

![CarMatch AI Logo](https://i.ibb.co/KzFPtdxx/CAR-2-Photoroom.png)

## Overview

CarMatch AI is a Streamlit application that uses Cohere's API to recommend cars based on user preferences through an interactive questionnaire. The app analyzes user inputs to understand their needs, budget, and lifestyle, then provides personalized car recommendations with detailed information.

## Features

- **Personalized Recommendations**: Get car suggestions tailored to your unique needs
- **Driver Profile**: See an analysis of your driving style and priorities
- **Detailed Car Information**: View specifications, features, and match scores
- **Explanations**: Understand why each car matches your preferences
- **Car Data Explorer**: Discover trends and insights about the car market

## Installation

### Prerequisites

- Python 3.9+
- Cohere API key (get one from [cohere.ai](https://cohere.ai))

### Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/carmatch-ai.git
   cd carmatch-ai
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   streamlit run app.py
   ```

4. Enter your Cohere API key when prompted in the app interface.

## Project Structure

```
CarMatch-AI/
├── app.py                   # Main entry point
├── requirements.txt         # Dependencies
├── README.md                # Documentation
├── static/                  # Static assets
│   └── style.css            # CSS styling
├── utils/                   # Utility modules
│   ├── __init__.py          # Makes utils a package
│   ├── config.py            # Configuration and initialization
│   ├── helpers.py           # Helper functions
│   └── cohere_api.py        # Cohere API functions
└── components/              # UI components
    ├── __init__.py          # Makes components a package
    ├── car_planner.py       # Car Planner tab
    ├── car_explorer.py      # Car Explorer tab
    └── about.py             # About tab
```

## How It Works

1. **Enter your preferences** - Tell us about what you're looking for in a car
2. **AI analysis** - Our AI analyzes your inputs to understand your needs
3. **Get recommendations** - Receive personalized car suggestions with detailed information
4. **Explore options** - View features, specifications, and why each car is a good match

## Data Sources

The app uses real market data from autoscout24-germany-dataset.csv, which contains information about various car makes, models, prices, and specifications.

## Privacy Notice

Your data is only used to generate recommendations within this application and is not stored or shared.

## Technologies Used

- **Streamlit**: For the web interface
- **Cohere API**: For AI-powered recommendations and analysis
- **Plotly**: For data visualization
- **Pandas & NumPy**: For data processing

## License

[MIT License](LICENSE)

## Acknowledgements

- Powered by [Cohere](https://cohere.ai/) AI technology
- Developed by CarMatch AI Team