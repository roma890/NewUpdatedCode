from flask import Flask, render_template
import pandas as pd
import os
from kaggle.api.kaggle_api_extended import KaggleApi

app = Flask(__name__)

# Function that sets up the Kaggle API connection and authenticates
def connect_to_kaggle():
    api = KaggleApi()
    api.authenticate()
    return api

# Function that downloads dataset from Kaggle and returns a Pandas DataFrame
def get_csv_from_kaggle():
    # Establish and authenticate connection
    api = connect_to_kaggle()
    
    # Define the current directory and dataset path
    current_directory = os.getcwd()
    dataset_name = "epa/fuel-economy"
    savepath = os.path.join(current_directory, 'dataset-folder')
    
    # Create the dataset folder if it doesn't exist
    if not os.path.exists(savepath):
        os.makedirs(savepath)

    # Download dataset files
    api.dataset_download_files(dataset_name, path=savepath, unzip=True)
    
    # Assuming the file is named 'database.csv' and is located in the folder 'dataset-folder'
    filepath = os.path.join(savepath, 'database.csv')
    
    # Check if the file exists before reading
    if os.path.exists(filepath):
        data = pd.read_csv(filepath)
        return data
    else:
        print(f"File {filepath} not found. Check if the dataset contains 'database.csv'.")
        return None

@app.route('/')
def index():
    # Get the data
    fuel_data = get_csv_from_kaggle()
    
    # If the data is successfully retrieved, convert it to records for display
    if fuel_data is not None:
        data_records = fuel_data.to_dict(orient='records')
        return render_template('index.html', data=data_records)
    else:
        return render_template('error.html', message="Data could not be loaded.")

if __name__ == '__main__':
    app.run(debug=True)

