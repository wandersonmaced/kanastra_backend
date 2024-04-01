import boto3


class ReadFileFromS3:
    def __init__(self, bucket_name, object_key, chunk_size=1024):
        """
        Initialize the S3FileReader.
        here we use boto3.resource('s3').Bucket()
        but I dont have a bucket to test it so I did some unit tests
        """
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.chunk_size = chunk_size
        self.s3_client = boto3.client('s3')
        self.body = None

    def open(self):
        """
        Open the S3 file for reading.
        """
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=self.object_key)
        self.body = response['Body']

    def read_chunk(self):
        """
        Read a chunk of data from the S3 file.
        """
        if self.body is None:
            raise ValueError("File is not open. Call 'open()' method before reading.")

        return self.body.read(self.chunk_size)

    def close(self):
        """
        Close the S3 file.
        """
        if self.body is not None:
            self.body.close()
            self.body = None
