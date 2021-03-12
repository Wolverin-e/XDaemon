import os
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient
MY_CONNECTION_STRING = ""
MY_FILE_CONTAINER = ""
LOCAL_FILE_PATH = ""


class IStorage:

    def __init__(self):
        pass

    def set_creds(self, key):
        pass

    def upload(self, container, folder_path):
        pass


class AzureStorage(IStorage):

    def __init__(self):
        self.connection_string = ""
        self.container = ""
        self.blob_service_client = None

    def set_creds(self, connection_string, container):
        self.connection_string = connection_string
        self.container = container
        self.blob_service_client = BlobServiceClient.from_connection_string(
            connection_string)
        self.client = self.blob_service_client.get_container_client(
            self.container)

    def upload(self, folder_path):
        if(self.connection_string == ""):
            print("Creds not set")
            return
        file_names = [f for f in os.listdir(folder_path)
                      if os.path.isfile(os.path.join(folder_path, f)) and ".txt" in f]
        for file_name in file_names:
            blob_client = self.blob_service_client.get_blob_client(container=self.container,
                                                                   blob=file_name)
            upload_file_path = os.path.join(folder_path, file_name)
            file_content_setting = ContentSettings(content_type='txt')
            print(f"uploading file - {file_name}")
            with open(upload_file_path, "rb") as data:
                blob_client.upload_blob(
                    data, overwrite=True, content_settings=file_content_setting)

    def listblobs(self, path=''):
        blob_iter = self.client.list_blobs(name_starts_with=path)
        for blob in blob_iter:
            print(blob.name)

    def delete(self, files):
        for file in files:
            print(f'Deleting {file}')
            self.client.delete_blob(file)

A = AzureStorage()
A.set_creds(MY_CONNECTION_STRING, MY_FILE_CONTAINER)
# A.upload(LOCAL_FILE_PATH)
A.listblobs()
