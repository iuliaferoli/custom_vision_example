import os
import json

from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings

ENV_SETTINGS = json.load(open('./env_settings.json'))

blob = ENV_SETTINGS['BLOB_STORAGE']
blob_service = BlockBlobService(blob['ACCOUNT_NAME'], blob['ACCOUNT_KEY'])
content_settings = ContentSettings(content_type='image/png')

# List all image urls (from camera)
def all_images(camera_name=""):
    generator = blob_service.list_blobs(blob["CONTAINER_CLASSIFY"], prefix=camera_name, delimiter="")
    return [{
        'name': os.path.basename(example.name),
        'url': blob["BASE_URL"] + blob["CONTAINER_CLASSIFY"] + '/' + example.name} for example in generator]


# List all image urls of specific coil
def coil_images(coil_id):
    generator = blob_service.list_blobs(blob["CONTAINER_CLASSIFY"], delimiter="")
    return [{
        'name': os.path.basename(example.name),
        'url': blob["BASE_URL"] + blob["CONTAINER_CLASSIFY"] + '/' + example.name} for example in generator if coil_id in example.name]
