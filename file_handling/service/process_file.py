import os
import pandas as pd

from file_handling.model.file_models import Debt, ChunkedUpload
from file_handling.service.file_thread_processing import FileProcessingThread
from file_handling.service.read_file_from_s3 import ReadFileFromS3
from file_handling.settings import CSV_FILES_ROOT


class ProcessFile:

    def __init__(self):
        self.chunk_size = os.environ.get("CHUNK_SIZE", 5000)

    def process_chunks(self, file_uuid):
        list_chunked_files = ChunkedUpload.objects.filter(file_uuid=file_uuid).order_by('chunk_idx')

        if list_chunked_files.count() > 0:
            chunk_paths, output_file = self.create_list_of_file_paths(list_chunked_files, file_uuid)
            with open(output_file, 'wb') as output_blob:
                for chunk in chunk_paths:
                    with open(chunk, 'rb') as input_blob:
                        output_blob.write(input_blob.read())
            return output_file

    def create_list_of_file_paths(self, list_chunked_files, file_uuid):
        chunk_paths = []
        for chunk in list_chunked_files:
            new_file_name = file_uuid + chunk.file_name
            output_file = os.path.join(CSV_FILES_ROOT, str(new_file_name))
            chunk_paths.append(os.path.join("", str(chunk.file)))

        return chunk_paths, output_file

    def multiprocess_file_from_server(self, file_path):
        processing_thread = FileProcessingThread(file_path, self.chunk_size)
        processing_thread.start()

    def process_file_from_s3(self, bucket_name, object_key):

        s3_reader = ReadFileFromS3(bucket_name, object_key, chunk_size=self.chunk_size)
        s3_reader.open()
        try:
            while True:
                chunk = s3_reader.read_chunk()
                if not chunk:
                    break
                # Process each chunk
                print(chunk)
        finally:
            s3_reader.close()
