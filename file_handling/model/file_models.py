import uuid
from django.db import models
from rest_framework import serializers


class Debt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField()
    email = models.EmailField(null=True, blank=True)
    amount = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    governmentId = models.CharField(null=True, blank=True )
    debtAmount = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    debtDueDate = models.CharField(null=True, blank=True )
    debtId = models.CharField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'file_handling'
        db_table = 'debt'

class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debt
        fields = ['id', 'name','email', 'amount', 'governmentId', 'debtAmount', 'debtDueDate', 'debtId', 'created_at']


class ChunkedUpload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    file_uuid = models.CharField(max_length=255)
    file = models.FileField(upload_to='csv_files/')
    file_name = models.CharField(max_length=255)
    chunk_qtd = models.IntegerField()
    chunk_idx = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'file_handling'
        db_table = 'chunked_upload'


class ChunkedUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChunkedUpload
        fields = ['id', 'file_uuid', 'file', 'file_name', 'chunk_qtd', 'chunk_idx', 'created_at']
