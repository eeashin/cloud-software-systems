import os
from google.cloud import storage
import functions_framework
# Add any imports that you may need, but make sure to update requirements.txt


@functions_framework.http
def create_text_file_http(request):
    bucket_name = os.environ.get("BUCKET_ENV_VAR")
    storage_client = storage.Client()

    request_json = request.get_json(silent=True)
    if request_json and 'fileName' in request_json:
        fileName = request_json['fileName']
    if request_json and 'fileContent' in request_json:
        fileContent = request_json['fileContent']

    bucket = storage_client.get_bucket(bucket_name)
    file = bucket.blob(fileName)
    file.upload_from_string(fileContent)

    res = {"fileName": fileName}
    return res, 200
