import json
import os

import pandas as pd

from src.config.setting import FOLDER_DATA


def write_to_csv(filename, data):
    """Save a list of dictionaries to a CSV file using Pandas."""
    if not data:
        print("No data to save.")
        return

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data)
    location = os.path.join(FOLDER_DATA, filename)
    if not os.path.exists(location):
        os.makedirs(location)

    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False, encoding='utf-8')

    print(f"Data saved to {filename}")


def write_json_to_file(file_name, data):
    location = os.path.join(FOLDER_DATA, file_name)
    json_file = open(location, 'w')
    try:
        json.dump(data, json_file, ensure_ascii=False)
        print(f"Data saved to {file_name}")
    except Exception as e:
        print(f"Error: {e}")
    json_file.close()


def read_file_to_json(file_name):
    location = os.path.join(FOLDER_DATA, file_name)
    with open(location, 'r', encoding='utf-8') as file:
        # Load the data from the file and convert it to a Python object
        return json.load(file)


def write_json_to_csv(file_name, data):
    """Save a list of objects to a CSV file."""
    # Flatten each object in the list
    for item in data:
        for key, value in item.items():
            if isinstance(value, dict):  # Check if the value is a dictionary
                item[key] = json.dumps(value)  # Convert to JSON string
    df = pd.DataFrame(data)
    location = os.path.join(FOLDER_DATA, file_name)
    os.makedirs(FOLDER_DATA, exist_ok=True)
    # Create a DataFrame and save to CSV
    df.to_csv(location, index=False, encoding='utf-8')
