##Key Features
Dynamic Filtering:

Focuses on the top 5 app categories, excluding those starting with A, C, G, or S.
Considers only countries with app installs exceeding 1 million.
Choropleth Map:

Displays global app installations, with color intensity proportional to the number of installs.
Interactive features include hover information (app category and install count).
Time-Based Display:

Ensures the map is displayed only between 6 PM and 8 PM IST.



import plotly.express as px
import pandas as pd
import googlemaps
import datetime
import pytz
import re

# Load your dataset containing app installs by country and category
df = pd.read_csv("/content/Playstore_final.csv")


# Filter for top 5 categories (excluding those starting with A, C, G, S)
top_categories = df['Category'].value_counts().head(5).index.tolist()
filtered_categories = [cat for cat in top_categories if cat[0] not in ['A', 'C', 'G', 'S']]
filtered_df = df[df['Category'].isin(filtered_categories)]

filtered_df.loc[:, 'Installs'] = pd.to_numeric(filtered_df['Installs'], errors='coerce')


# Filter countries with installs exceeding 1 million
filtered_df = filtered_df[filtered_df['Installs'] > 1000000]

filtered_df['Country'] = filtered_df['Developer Address'].str.extract(r'([A-Za-z]+)$')  # Extracts the last word (country) from address

gmaps = googlemaps.Client(key="AIzaSyD704oTDE6tMWEF6vyevKTOPXZdtmeAEDU")

# Function to get country code from address
def get_country_code(address):
    try:
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            for component in geocode_result[0]["address_components"]:
                if "country" in component["types"]:
                    return component["short_name"]
        return None
    except Exception as e:
        print(f"Error geocoding address '{address}': {e}")
        return None

# Apply the function to get country codes
filtered_df["Country"] = filtered_df["Developer Address"].apply(get_country_code)
filtered_df["Country"] = filtered_df["Developer Address"].str.extract(r"(\w+)$")
filtered_df["Country"] = filtered_df["Developer Address"].str.extract(r"([A-Za-z]+)(?:,\s*[A-Za-z]+(?:\s+\d{5})?)?$", expand=False)  # Extracts the country
filtered_df = filtered_df.dropna(subset=["Country"])

# Create the choropleth map

fig = px.choropleth(
    filtered_df,
    locations="Country",
    locationmode="country names",
    color="Installs",
    hover_name="Category", # Show category on hover
    hover_data=["Installs"],
    color_continuous_scale="Viridis",
    title="Global App Installs by Country (Top 5 Categories, Installs > 1 Million)",
    )
fig.update_layout(coloraxis_showscale=True)
fig.update_traces(marker_line_width=0)

# Function to check if current time is within the allowed range
def is_allowed_time():
    now = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))  # IST
    return now.hour >= 18 and now.hour < 20

# Display the map only if within the allowed time range
if is_allowed_time():
    fig.show()
else:
    print("The map is only available between 6 PM and 8 PM IST.")
