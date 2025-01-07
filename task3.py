##Key Features
Data Cleaning and Transformation:

Preprocesses the Installs column by removing unwanted characters (commas and + signs) and converting to numeric format.
Handles the Last Updated column, converting it to a datetime format and extracting the Month-Year for time-based analysis.
Filtering:

Focuses on apps in the TOOLS category.
Filters apps whose names start with "D".
Considers only apps with more than 10,000 installs.
Grouping and Growth Calculation:

Groups data by Month-Year and calculates the total installs per month.
Computes the month-over-month growth rate for installs using the percentage change formula.
Visualization:

Creates an interactive time-series line chart with Plotly Express.
Highlights periods of significant growth (>20%) using shaded regions.
Time-Based Display:

Restricts chart display to the time window of 12 PM to 9 PM IST.






import plotly.express as px
import pandas as pd
import datetime
import pytz

# Load the dataset
df = pd.read_csv("./content/Playstore_final.csv")

# Clean and convert 'Installs'
df['Installs'] = df['Installs'].str.replace(',', '')  # Remove commas
df['Installs'] = df['Installs'].str.replace('+', '')  # Remove '+' signs
df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')

# Convert 'Released' to datetime before filtering

df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')

# Filter data based on conditions
filtered_df = df[
    (df['Category'] == 'TOOLS') &
    (df['App Name'].str.startswith('D')) &
    (df['Installs'] > 10000)
]

print(df)
# Convert 'Last Updated' to datetime and extract month-year (using .loc)
filtered_df.loc[:, 'Last Updated'] = pd.to_datetime(filtered_df['Last Updated'])
filtered_df.loc[:,'Month-Year'] = filtered_df['Last Updated'].dt.to_period('M')

# Group by month-year and category, sum installs
installs_by_month = filtered_df.groupby(['Month-Year', 'Category'])['Installs'].sum().reset_index()

# Calculate month-over-month growth
installs_by_month['Growth'] = installs_by_month.groupby('Category')['Installs'].pct_change()

# Convert 'Month-Year' to string (before plotting)
installs_by_month['Month-Year'] = installs_by_month['Month-Year'].dt.strftime('%Y-%m')

# Function to check if current time is within allowed range
def is_allowed_time():
    now = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    return now.hour >= 12 and now.hour < 21

# Create and display the chart if within allowed time
if is_allowed_time():
   # print(filtered_df['Last Updated'])
    fig = px.line(
        installs_by_month,
        x='Month-Year',
        y='Installs',
        color='Category',
        title='Total Installs Over Time by Category (Tools, App Name starts with D, Installs > 10k)'
    )

    # Highlight growth areas (add shaded regions)
    for category in installs_by_month['Category'].unique():
        growth_periods = installs_by_month[
            (installs_by_month['Category'] == category) & (installs_by_month['Growth'] > 0.2)
        ]
        for index, row in growth_periods.iterrows():
            fig.add_shape(
                type="rect",
                x0=row['Month-Year'],
                x1=installs_by_month.loc[index + 1, 'Month-Year'] if index + 1 < len(installs_by_month) else row['Month-Year'],
                y0=0,
                y1=row['Installs'],
                fillcolor="rgba(255, 0, 0, 0.2)",  # Red with 20% opacity
                line_width=0,
            )

    fig.show()
else:
    print("The graph is only available between 12 PM and 9 PM IST.")
