from django.forms import ModelForm
from django import forms
from ..model.file_models import ChunkedUpload


class UploadFileForm(ModelForm):
    file_uuid = forms.TextInput()
    file = forms.FileField()
    file_name = forms.TextInput()
    chunk_qtd = forms.IntegerField()
    chunk_idx = forms.IntegerField()

    class Meta:
        model = ChunkedUpload
        fields = ['file', 'file_uuid', 'file_name', 'chunk_qtd', 'chunk_idx']
