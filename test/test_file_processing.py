import os
import pytest
from unittest.mock import MagicMock, patch
from file_handling.model.file_models import Debt, ChunkedUpload
from file_handling.service.read_file_from_s3 import ReadFileFromS3
from file_handling.settings import CSV_FILES_ROOT
from file_handling.service.process_file import ProcessFile


@pytest.fixture
def process_file_instance():
    return ProcessFile()


@pytest.fixture
def mock_chunked_upload():
    with patch('file_handling.model.file_models.ChunkedUpload.objects') as mock_objects:
        mock_objects.filter.return_value = MagicMock()
        yield mock_objects


@pytest.fixture
def mock_debt():
    with patch('file_handling.model.file_models.Debt.objects') as mock_objects:
        mock_objects.bulk_create.return_value = MagicMock()
        yield mock_objects


def test_process_chunks(process_file_instance, mock_chunked_upload, tmpdir):
    file_uuid = "test_uuid"
    chunk = ChunkedUpload(file_uuid=file_uuid, chunk_idx=0, file_name='test.csv', file='test.csv')
    mock_chunked_upload.filter.return_value.count.return_value = 1
    mock_chunked_upload.filter.return_value.order_by.return_value = [chunk]
    output_file = process_file_instance.process_chunks(file_uuid)
    assert output_file == os.path.join(CSV_FILES_ROOT, file_uuid + 'test.csv')


def test_create_list_of_file_paths(process_file_instance, mock_chunked_upload):
    file_uuid = "test_uuid"
    chunk = ChunkedUpload(file_uuid=file_uuid, chunk_idx=0, file_name='test.csv', file='test.csv')
    mock_chunked_upload.filter.return_value = [chunk]
    chunk_paths, output_file = process_file_instance.create_list_of_file_paths([chunk], file_uuid)
    assert len(chunk_paths) == 1
    assert output_file == os.path.join(CSV_FILES_ROOT, file_uuid + 'test.csv')


def test_process_file_from_server(process_file_instance, mock_debt, tmpdir):
    tmp_file = tmpdir.join("test.csv")
    tmp_file.write("header\nvalue1\nvalue2\n")
    process_file_instance.process_file_from_server(str(tmp_file))
    assert mock_debt.bulk_create.called


def test_process_file_from_s3(process_file_instance):
    bucket_name = "test_bucket"
    object_key = "test_key"
    with patch('file_handling.service.read_file_from_s3.ReadFileFromS3') as mock_reader:
        mock_reader_instance = mock_reader.return_value
        mock_reader_instance.read_chunk.side_effect = [b'chunk1', b'chunk2', b'']
        process_file_instance.process_file_from_s3(bucket_name, object_key)
        assert mock_reader_instance.open.called
        assert mock_reader_instance.close.called
        assert mock_reader_instance.read_chunk.call_count == 3
