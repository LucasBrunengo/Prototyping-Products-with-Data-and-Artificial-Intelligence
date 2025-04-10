# Netflix Marathon-Watch Planner - Submission Document

## Model Selection
I chose the Netflix titles dataset from a previous data analysis course, focusing on creating an interactive content recommendation tool.

## Utility of the Prototype
The Netflix Marathon-Watch Planner is an innovative solution for streaming content consumers, addressing the common challenge of deciding what to watch within a limited time frame. By allowing users to input their available viewing time, preferred genres, multiple moods, and content ratings, the app generates personalized watch plans that maximize entertainment value. The prototype goes beyond simple recommendations by optimizing content selection to precisely fit the user's available time, reducing decision fatigue and enhancing the streaming experience.

The application now includes social sharing capabilities so users can share their marathon plans with friends, accessibility features for improved usability, and personalization options that allow users to input their favorite shows for better recommendations.

## Main Difficulties Found
The most significant challenges encountered during the project spanned multiple technical and design domains. Handling diverse data types in the Netflix dataset proved particularly complex, with the need to manage different duration formats for movies and TV shows requiring sophisticated parsing strategies. Creating an algorithm to intelligently combine content while staying within the user's time constraints demanded intricate logic and multiple iterative refinements. 

A particularly challenging aspect was implementing the mood-based filtering with support for multiple mood selections. This required developing a complex filtering algorithm that could combine content suggestions based on different emotional states while avoiding duplicate recommendations and handling unhashable list types in the dataframe.

Error handling proved essential to application stability, especially when dealing with data type mismatches in the factorize array operations. Implementing robust error catching throughout the application ensured graceful degradation instead of application crashes, significantly improving the user experience.

The user interface design presented its own set of challenges, requiring careful widget placement and creative use of Streamlit's layout capabilities to balance comprehensive filtering options with visual appeal. Additionally, working with CSS posed significant obstacles due to a lack of prior knowledge in styling and layout design, necessitating extensive learning and experimentation to achieve the desired visual presentation. 

Performance optimization was another major challenge, requiring implementation of strategic caching and filter fingerprinting to avoid redundant calculations. Creating unique element IDs for dynamically generated widgets proved essential for eliminating duplication errors in Streamlit's rendering system.

These multifaceted challenges required continuous problem-solving, technical adaptability, and a persistent approach to overcoming design and implementation hurdles.
