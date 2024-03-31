
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from file_handling.model.file_models import ChunkedUploadSerializer, ChunkedUpload
from file_handling.service.process_file import ProcessFile


class FileChunkView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.process_file = ProcessFile()


    def post(self, request, *args, **kwargs):
        form = ChunkedUploadSerializer(data=request.data)
        if form.is_valid():
            form.save()
            if form.validated_data["chunk_idx"] == form.validated_data["chunk_qtd"]:
                full_file_path = self.process_file.process_chunks(form.validated_data["file_uuid"])
                self.process_file.process_file_from_server(full_file_path)
            return Response({"message": "Chunk uploaded successfully."},  status=status.HTTP_201_CREATED)

        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        chunked_uploads = ChunkedUpload.objects.all()
        serializer = ChunkedUploadSerializer(chunked_uploads, many=True)
        return Response(serializer.data)

