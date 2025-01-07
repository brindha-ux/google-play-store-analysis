#Key Features
Filters the dataset to include only apps with over 1,000 reviews for more meaningful analysis.
Focuses on five specific app categories: Action, Photography, Sports, Tools, and Food.
Maps user ratings into sentiment categories (Positive, Neutral, Negative) and rating groups (e.g., 1-2 stars, 3-4 stars).
Aggregates review counts by category, sentiment, and rating group.
Visualizes the aggregated data using a customizable stacked bar chart.





  
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("/Playstore_final.csv", engine='python', on_bad_lines='skip')

# Filter out apps with more than 1,000 reviews
df_filtered = df[df['Reviews'] > 1000]

# Get the top 5 categories by total reviews_count
# Assuming you have a way to determine top categories, replace this with your logic
df_top_Categories = df_filtered[df_filtered['Category'].isin(['Action', 'Photography', 'Sports', 'Tools', 'Food'])]

# Define sentiment and rating group
def Rating(Rating):
    if pd.isnull(Rating):
        return 'Unknown', 'Unknown'
    elif Rating <= 2:
        return 'Negative', '1-2 stars'
    elif Rating == 3:
        return 'Neutral', '3-4 stars'
    elif Rating == 4:
        return 'Positive', '3-4 stars'
    else:  # Rating 5
        return 'Positive', '4-5 stars'

# Convert 'Rating' column to numeric
df_top_Categories['Rating'] = pd.to_numeric(df_top_Categories['Rating'], errors='coerce')

# Apply mapping
df_top_Categories[['Sentiment', 'Rating_Group']] = df_top_Categories['Rating'].apply(lambda x: pd.Series(Rating(x)))


# Group and aggregate
sentiment_counts = df_top_Categories.groupby(['Category', 'Rating_Group', 'Sentiment'])['Reviews'].sum().unstack(fill_value=0)

# Create stacked bar chart
plt.figure(figsize=(10, 6))  # Adjust figure size as needed
# Customize colors for sentiment categories
colors = {'Positive': 'green', 'Negative': 'red', 'Neutral': 'blue'}  # Adjust colors as desired

sentiment_counts.plot(kind='bar', stacked=True, color=[colors.get(sentiment, 'gray') for sentiment in sentiment_counts.columns])




plt.title('Sentiment Distribution of User Reviews by Rating Group and Category')
plt.xlabel('Category and Rating Group')
plt.ylabel('Number of Reviews (Greater than 1000)')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Sentiment', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


