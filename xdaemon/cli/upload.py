import os
from azure.storage.blob import BlobServiceClient, ContainerClient
from logging import getLogger
from pathlib import Path

logger = getLogger(__name__)


class IStorage:

    def __init__(self, creds):
        pass

    def upload(self, path):
        pass


class AzureStorage(IStorage):

    def __init__(self, creds):
        logger.debug(f"Creds: {creds}")
        self.container = ContainerClient
        self._set_creds(creds["connection_string"], creds["container"])

    def _set_creds(self, connection_string, container_name):

        if(not (connection_string and connection_string)):
            logger.error("AzureStorage: Credentials not supplied properly")
            return

        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        self.container = blob_service_client.get_container_client(
            container_name
        )

    def upload(self, path):

        logger.info(f"Uploading: {path}")

        path = Path(path).resolve()

        if not path.exists():
            logger.warning(f"uploading: {path} doesn't exist.")
            return

        if(path.is_file()):
            self._upload(path)
            return

        parent_dir = str(path.parent.resolve())+'/'

        for root, dirs, files in os.walk(path):

            relative_root = Path(root.replace(parent_dir, ''))

            for file in files:
                self._upload(Path(root)/file, str(relative_root/file))
                logger.debug(f"Uploading: {relative_root/file}")

    def _upload(self, path, blob_path=None):
        logger.debug(f"Uploading: {path}")
        with open(path, "rb") as data:
            self.container.upload_blob(
                name=blob_path or path.name,
                data=data,
                overwrite=True
            )

    def listblobs(self, path=''):
        blob_iter = self.client.list_blobs(name_starts_with=path)
        for blob in blob_iter:
            print(blob.name)

    def delete(self, files):
        for file in files:
            print(f'Deleting {file}')
            self.client.delete_blob(file)
