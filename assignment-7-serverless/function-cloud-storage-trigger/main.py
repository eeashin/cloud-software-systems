import os
import io  # To read from saved file
from google.cloud import storage, vision
import functions_framework
# Add any imports that you may need, but make sure to update requirements.txt


@functions_framework.cloud_event
def image_to_text_storage(cloud_event):
    data = cloud_event.data
    init_bucket = data["bucket"]
    source_obj_name = data["name"]

    if not source_obj_name.endswith('.txt'):
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(init_bucket)
        blob = bucket.blob(source_obj_name)
        destination_file_name = "/tmp/"+source_obj_name
        blob.download_to_filename(destination_file_name)

        client = vision.ImageAnnotatorClient()

        with io.open(destination_file_name, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations

        filename = source_obj_name.replace('jpg', 'txt')
        file = bucket.blob(filename)
        file.upload_from_string(texts[0].description)
        res = {"OK"}
        return res, 200
