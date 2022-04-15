from google.cloud import vision, storage
import tempfile
import os

vision_client = vision.ImageAnnotatorClient()
storage_client = storage.Client()

def file_detection(data, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    file_name = data['name']
    bucket_name = data['bucket']

    print(f"bucket name: {bucket_name}.")
    print(f"file name: {file_name}.")
    
    blob = storage_client.bucket(bucket_name).get_blob(file_name)
    blob_uri = f"gs://{bucket_name}/{file_name}"
    blob_source = vision.Image(source=vision.ImageSource(gcs_image_uri=blob_uri))

    facesjson = vision_client.face_detection(image=blob_source, max_results=4).face_annotations
    print(facesjson)


    _, temp_local_filename = tempfile.mkstemp()
    f = open(temp_local_filename, "w")
    f.write(str(facesjson))
    f.close()

    face_bucket = storage_client.bucket("cs4843-out")
    uploadfilename =  file_name[:-5] + ".txt"
    new_blob = face_bucket.blob(uploadfilename)
    new_blob.upload_from_filename(temp_local_filename)

    print(f"Face Response uploaded to: gs://{face_bucket}/{uploadfilename}")

    # Delete the temporary file.
    os.remove(temp_local_filename)
