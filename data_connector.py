from azure.storage.blob import BlobServiceClient, BlobClient
import pandas as pd
from io import StringIO
import io  # Import the io module
from tqdm import tqdm
import functools
import constants

# Replace with your actual connection string
connection_string = ''
container_name = 'data-swollen'
master_file = constants.csv_file_path

# Function to download blob with progress
@functools.cache
def download_blob_with_progress(blob_client, total_size):
    stream = io.BytesIO()
    chunk_size = 1024 * 1024  # 1MB
    bytes_downloaded = 0

    with tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading') as pbar:
        downloader = blob_client.download_blob()
        for chunk in downloader.chunks():
            stream.write(chunk)
            bytes_downloaded += len(chunk)
            pbar.update(len(chunk))

    stream.seek(0)
    return stream

def get_data():
    try:
        # Initialize the BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Initialize the BlobClient
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=master_file)

        # Get blob size
        blob_properties = blob_client.get_blob_properties()
        total_size = blob_properties.size

        # Download the blob with progress
        blob_data = download_blob_with_progress(blob_client, total_size).getvalue()

        # Convert the blob's content to a StringIO object
        data = StringIO(blob_data.decode('utf-8'))

        # Read the data into a pandas DataFrame
        master_data = pd.read_csv(data, on_bad_lines='warn', encoding='utf-8')

        return master_data
    except Exception as data_ex:
        print(f'Ooops there was issue in get_data {data_ex}')
        return None
