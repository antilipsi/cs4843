def detect_file(data, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    file_data = data
 

    file_name = file_data["name"]
    bucket_name = file_data["bucket"]

    print(f"Processing file: {file_name}.")
    print(f"Bucket: {bucket_name}.")
