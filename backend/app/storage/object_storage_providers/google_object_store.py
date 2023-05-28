from google.cloud import storage

# Load the service account key and create a storage client
client = storage.Client.from_service_account_json(
    "backend\mr-know-all-387618-f2bc1e5e3b0b.json"
)


def uploadFile(user_name: str, file_path: str):
    # Create a user-specific folder path within the bucket
    bucket_name = "mr-know-all"
    file_name = file_path.split("\\")[-1]

    # Upload the file to the user's folder in the bucket
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(f"{user_name}/{file_name}")
    blob.upload_from_filename(file_path)


def deleteFile(user_name: str, file_name: str):
    # Instantiate the client
    client = storage.Client()

    # Get the bucket
    bucket = client.get_bucket("mr-know-all")

    # Specify the file path within the user's folder
    file_path = f"{user_name}/{file_name}"

    # Get the blob (file) within the bucket
    blob = bucket.blob(file_path)

    # Delete the blob
    blob.delete()
