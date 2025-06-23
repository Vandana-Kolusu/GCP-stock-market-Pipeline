import pandas as pd
import requests
import json
from google.cloud import storage
from datetime import datetime

# Function to list all files in the specified folder (to_process)
def list_files_in_gcs(bucket_name, folder_name):
    print(f"Listing files in folder: {folder_name}")  # Log folder being processed
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    # List all files in the folder (prefix matches 'to_process')
    blobs = storage_client.list_blobs(bucket_name, prefix=folder_name)
    file_names = [blob.name for blob in blobs if blob.name.endswith('.json')]  # Only pick JSON files
    print(f"Found files: {file_names}")  # Log the list of files found
    return file_names

# Function to fetch raw data from Google Cloud Storage (GCS)
def fetch_raw_data_from_gcs(bucket_name, source_blob_name):
    print(f"Fetching raw data from: {source_blob_name}")  # Log the file being processed
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    
    # Load the raw data from the file
    raw_data = json.loads(blob.download_as_text())  
    print(f"Raw data fetched from {source_blob_name}")  # Log after fetching the data
    return raw_data

# Function to transform the raw data
def transform_data(raw_data):
    """
    Transforms the raw stock data from Alpha Vantage into a DataFrame, performs calculations,
    and returns the transformed data.
    """
    print("Transforming raw data...")  # Log transformation start
    # Extract the time series data (daily stock data)
    time_series = raw_data.get('Time Series (Daily)', {})

    # Convert the time series data to a pandas DataFrame
    df = pd.DataFrame.from_dict(time_series, orient='index')
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    
    # Convert the index to datetime
    df.index = pd.to_datetime(df.index)
    
    # Sort the data by date (ascending)
    df = df.sort_index(ascending=True)
    
    # Example transformation: Calculate the moving average of the 'Close' price over the last 5 days
    df['5_day_avg'] = df['Close'].rolling(window=5).mean()
    
    # Filter out rows where the 'Close' price is missing (optional)
    df = df.dropna(subset=['Close'])

    print("Transformation complete.")  # Log after transformation
    return df

# Function to upload transformed data to Google Cloud Storage (GCS)
def upload_transformed_to_gcs(df, bucket_name, destination_blob_name):
    print(f"Uploading transformed data to GCS: {destination_blob_name}")  # Log the upload path
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    # Convert the DataFrame to CSV string
    csv_data = df.to_csv(index=True)
    
    # Create a blob (file) in GCS
    blob = bucket.blob(destination_blob_name)
    
    # Upload the CSV data to the blob in GCS
    blob.upload_from_string(csv_data, content_type='text/csv')
    print(f"Transformed data uploaded to GCS: gs://{bucket_name}/{destination_blob_name}")  # Log successful upload

# Function to move raw data from `to_process` to `processed` folder
def move_raw_data(bucket_name, source_blob_name, destination_blob_name):
    print(f"Attempting to move raw data from {source_blob_name} to {destination_blob_name}")  # Log movement start
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    # Get the source blob (raw data file)
    source_blob = bucket.blob(source_blob_name)
    
    # Check if the source blob exists
    if not source_blob.exists():
        print(f"Source file does not exist: gs://{bucket_name}/{source_blob_name}")
        return
    
    # Copy the file to the 'processed' folder
    source_blob.copy_to(bucket.blob(destination_blob_name))
    print(f"Raw data moved to: gs://{bucket_name}/{destination_blob_name}")  # Log successful move
    
    # Delete the original file from the 'to_process' folder
    source_blob.delete()
    print(f"Raw data deleted from: gs://{bucket_name}/{source_blob_name}")  # Log deletion


# Function to delete an empty folder (prefix) in GCS
def delete_empty_folder(bucket_name, folder_name):
    print(f"Checking if folder {folder_name} is empty")  # Log check for empty folder
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # List files in the folder (prefix matches 'to_process')
    blobs = storage_client.list_blobs(bucket_name, prefix=folder_name)
    
    # If no files are found, the folder is empty, and we can delete the "folder"
    if not any([blob.name.startswith(folder_name) for blob in blobs]):
        print(f"Deleting folder {folder_name} (empty folder) from GCS")  # Log folder deletion
        # Deleting an empty folder (by removing the prefix "to_process" if no files are there)
        return True
    else:
        print(f"The folder {folder_name} is not empty. Skipping deletion.")  # Log if folder is not empty
        return False

# Function to fetch raw data from the Alpha Vantage API
def fetch_raw_data():
    print("Fetching raw data from Alpha Vantage API...")  # Log the fetching process
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=your-api-key'
    response = requests.get(url)

    if response.status_code == 200:
        print("Raw data fetched successfully.")  # Log success
        return response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")  # Log failure
        return None

# Function to upload raw JSON data to Google Cloud Storage
def upload_raw_to_gcs(raw_data, bucket_name, destination_blob_name):
    print(f"Uploading raw data to GCS: {destination_blob_name}")  # Log the upload path
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    raw_data_string = json.dumps(raw_data)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(raw_data_string, content_type='application/json')
    print(f"Data uploaded to GCS: gs://{bucket_name}/{destination_blob_name}")  # Log successful upload

# Pub/Sub trigger entry point for Cloud Function (Ingest Raw Data)
def ingest_raw_data(event, context):
    """Triggered by a message on a Cloud Pub/Sub topic."""
    print("Function triggered")  # Log the function being triggered
    raw_data = fetch_raw_data()

    if raw_data:
        bucket_name = 'stock-market-bucket-kolusu'  # Replace with your GCS bucket name

        # Create a filename with the current timestamp (formatted to avoid invalid characters)
        filename = 'stock_raw_data_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.json'
        
        # Set the destination path in GCS (you can adjust the folder structure as needed)
        destination_blob_name = 'raw_data/to_process/' + filename  # GCS path for raw data

        # Upload the raw data to GCS
        upload_raw_to_gcs(raw_data, bucket_name, destination_blob_name)

    return 'Data ingestion complete!'

def transform_and_move_data(event, context):
    """Triggered by a message on a Cloud Pub/Sub topic."""
    print("Transform Function triggered")  # Log that the function was triggered.
    
    # GCS bucket and folder names
    bucket_name = event['bucket']  # Bucket name from event
    to_process_folder = 'raw_data/to_process/'  # Folder where raw data is stored
    processed_folder = 'raw_data/processed/'   # Folder where processed data will be moved
    
    # Get the file name from the event
    raw_data_file = event['name']  # File name from event
    print(f"Processing file: {raw_data_file}")  # Log the file being processed.
    
    # Fetch the raw data from GCS
    raw_data = fetch_raw_data_from_gcs(bucket_name, raw_data_file)

    if raw_data:
        print(f"Transforming data from {raw_data_file}")  # Log that data is being transformed.
        # Transform the raw data
        transformed_data = transform_data(raw_data)

        # Generate a filename with the current timestamp for the transformed data
        filename = 'stock_transformed_data_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.csv'
        
        # Set the destination path in GCS (new folder 'transformed_data')
        destination_blob_name = 'transformed_data/' + filename  # GCS path for transformed data

        # Upload the transformed data to GCS
        upload_transformed_to_gcs(transformed_data, bucket_name, destination_blob_name)

        # Move the raw data to the 'processed' folder
        destination_processed_blob_name = processed_folder + raw_data_file.split('/')[-1]  # Moving to 'processed' folder
        move_raw_data(bucket_name, raw_data_file, destination_processed_blob_name)

        print(f"Raw data moved to processed folder: {destination_processed_blob_name}")
    else:
        print(f"Failed to fetch raw data from {raw_data_file}")  # Log if failed to fetch data

    # After processing all files, check and delete the empty 'to_process' folder
    if delete_empty_folder(bucket_name, to_process_folder):
        print(f"Folder {to_process_folder} deleted successfully (if empty).")
    else:
        print(f"Folder {to_process_folder} not empty, skipping deletion.")

    return 'Data transformation, move, and folder cleanup complete!'

