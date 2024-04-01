from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import MagicMock

from file_handling.views.file_chunk_upload import FileChunkView


class TestFileChunkView(APITestCase):

    def setUp(self):
        self.view = FileChunkView()
        self.valid_data = {
            "file_uuid": "abc123",
            "file": "path/to/file",
            "file_name": "test_file.csv",
            "chunk_qtd": 3,
            "chunk_idx": 2
        }
        self.invalid_data = {
            "file_uuid": "abc123",
            "file": "",  # Missing required field
            "file_name": "test_file.csv",
            "chunk_qtd": 3,
            "chunk_idx": 2
        }

    def test_post_valid_data(self):
        self.view.process_file.process_chunks = MagicMock(return_value='full_file_path')
        self.view.process_file.process_file_from_server = MagicMock()
        response = self.client.post('/files/upload', self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"message": "Chunk uploaded successfully."})
        self.view.process_file.process_chunks.assert_called_once_with('abc123')
        self.view.process_file.process_file_from_server.assert_called_once_with('full_file_path')

    def test_post_invalid_data(self):
        response = self.client.post('/files/upload', self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('file', response.data)  # Check if the 'file' field is in the response data

    def test_post_missing_data(self):
        response = self.client.post('/files/upload', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('file_uuid', response.data)  # Check if the 'file_uuid' field is in the response data
