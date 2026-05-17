# 🧩 Python for Data Engineering: Pipeline Playgrounds
# 1. File I/O for Data Wranglers
# Learn how to open, read, and write data files in various formats. Understand modes like 'r', 'w', and 'a', and how file paths matter.
# 💡 Exercise: Read a sample text file, count lines, and write results to a new file named summary.txt.

with open("/workspaces/de-101-notes/Code/sample.txt", "r", encoding="utf-8") as f:
    # Perform file operations here
    data = f.read()
print(data)

# 2. CSV Magic: From Spreadsheet to Pipeline
# Dive into the csv module and pandas.read_csv() to process tabular data. Learn how to handle delimiters, headers, and missing values.
# 💡 Exercise: Load a CSV of sales data, filter rows with missing entries, and export a cleaned version.

# To install pandas, you can use pip:
# pip install pandas
import pandas as pd

sales_df = pd.read_csv("/workspaces/de-101-notes/Code/sales_data.csv")
sales_df_cleaned = sales_df.dropna()
sales_df_cleaned.to_csv("/workspaces/de-101-notes/Code/sales_data_cleaned.csv", index=False)

# 3. JSON Juggling: Handling APIs and Nested Data
# Practice working with structured but nested data. Use json.loads() and json.dump() for readable storage and transformations.
# 💡 Exercise: Parse a JSON file with nested customer details and flatten it into a simple dictionary list.

import pandas as pd
import json

# Load your nested JSON file
with open("/workspaces/de-101-notes/Code/customers.json", "r") as f:
    data = json.load(f)

# Flatten the data
df = pd.json_normalize(data, sep='_')
print(df)

# Convert back to a list of simple dictionaries (here each dictionary represents a single row)
flattened_list = df.to_dict(orient='records')
print(flattened_list)

# Note: For nested dictionary keyed by the index
flattened_list2 = df.to_dict(orient='index')
print(flattened_list2)

# 4. APIs on Tap: Fetching Data from the Web
# Learn to use Python’s requests library to call REST APIs, handle responses, and extract payloads. Understand basic rate limiting and error statuses.
# 💡 Exercise: Call a weather API for Dallas and print tomorrow’s forecast neatly.

# To install requests and python-dotenv, you can use pip:
# pip install requests python-dotenv
import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load variables from .env into the script's environment
load_dotenv("/workspaces/de-101-notes/Code/.env")

# Get the key safely
API_KEY = os.getenv("WEATHER_API_KEY")
print(f"Loaded API Key: {'Yes' if API_KEY else 'No'}")  # Check if the key was loaded successfully

def get_dallas_weather():
    if not API_KEY:
        print("Missing API Key! Make sure your .env file is set up correctly.")
        return

# API configuration for Dallas
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": "Dallas,US",
        "appid": API_KEY,
        "units": "imperial"  # Use 'metric' for Celsius
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        # Identify tomorrow's date
        tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        print(f"--- Dallas Forecast for {tomorrow_date} ---")
        
        # Filter for tomorrow's midday data point
        found = False
        for entry in data['list']:
            if tomorrow_date in entry['dt_txt'] and "12:00:00" in entry['dt_txt']:
                temp = entry['main']['temp']
                desc = entry['weather'][0]['description']
                print(f"Midday Sky: {desc.capitalize()}")
                print(f"Expected Temp: {temp}°F")
                found = True
                break
        
        if not found:
            print("Could not find a specific midday forecast for tomorrow yet.")

    except requests.exceptions.RequestException as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    get_dallas_weather()

# 5. The Art of the Try: Error Handling in Data Flows
# Use try and except to catch common data pipeline errors—like bad connections or missing files—and recover gracefully.
# 💡 Exercise: Simulate a pipeline that retries if the file doesn’t exist or the API call fails.

# 6. Glue Code: Connecting Multiple Data Sources
# Blend data from multiple files or APIs into one consistent dataset using dictionaries and DataFrames.
# 💡 Exercise: Merge CSV of users with a JSON of transaction details based on user IDs.

# 7. Data Cleansing Gym: Validating and Normalizing Inputs
# Get your data in shape! Learn transformations such as trimming strings, converting types, and validating formats.
# 💡 Exercise: Take a CSV of phone numbers, remove spaces, and enforce a consistent format.

# 8. Batch It Up: Automating Data Tasks
# Simulate real pipeline behavior: automate multiple file reads, data transformations, and exports. Learn about loops and scheduling.
# 💡 Exercise: Loop through all CSVs in a folder and combine them into one master file.

# 9. Logging for Legends: Keeping an Eye on Pipelines
# Use the logging module to record events, errors, and timestamps. Logging helps with reproducibility and debugging in production.
# 💡 Exercise: Add a logger to your previous pipeline that writes success and error messages to a log file.

# 10. Tiny Transformations: Mini ETLs in Action
# Build small Extract-Transform-Load workflows. Learn modularization—keeping “Extract,” “Transform,” and “Load” steps separate for clarity.
# 💡 Exercise: Pull user data from an API, transform names to uppercase, and export to CSV.

# 11. Scaling the Stream: Working with Big Data Samples
# Learn memory-friendly methods like chunked iteration and generators. Practice with large but manageable datasets.
# 💡 Exercise: Read a huge CSV in chunks and compute an average column value efficiently.

# 12. The Finishing Touch: Save, Backup, and Document Pipelines
# Explore version control, backups, and documentation best practices using markdown and comments.
# 💡 Exercise: Write a README explaining all your pipeline steps and upload everything to GitHub.