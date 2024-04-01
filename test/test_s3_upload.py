import unittest
from unittest.mock import MagicMock, patch
from file_handling.service.read_file_from_s3 import ReadFileFromS3

class TestReadFileFromS3(unittest.TestCase):
    def setUp(self):
        self.bucket_name = "test-bucket"
        self.object_key = "test-file.txt"
        self.chunk_size = 1024

    @patch('boto3.client')
    def test_open_success(self, mock_client):
        mock_body = MagicMock()
        mock_body.read.return_value = b"Test data"
        mock_response = {'Body': mock_body}
        mock_client.return_value.get_object.return_value = mock_response

        reader = ReadFileFromS3(self.bucket_name, self.object_key)

        reader.open()

        mock_client.assert_called_once_with('s3')
        mock_client.return_value.get_object.assert_called_once_with(
            Bucket=self.bucket_name, Key=self.object_key)

        self.assertEqual(reader.body, mock_body)

    @patch('boto3.client')
    def test_read_chunk_success(self, mock_client):
        reader = ReadFileFromS3(self.bucket_name, self.object_key)

        mock_body = MagicMock()
        reader.body = mock_body

        result = reader.read_chunk()

        mock_body.read.assert_called_once_with(reader.chunk_size)

        self.assertEqual(result, mock_body.read.return_value)

    def test_read_chunk_without_opening_file(self):
        reader = ReadFileFromS3(self.bucket_name, self.object_key)

        with self.assertRaises(ValueError):
            reader.read_chunk()

if __name__ == '__main__':
    unittest.main()
