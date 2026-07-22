from django import forms
from .models import UserImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = ('original_image',)
        widgets = {
            'original_image': forms.FileInput(attrs={'accept': 'image/*'}),
        }
        labels = {
            'original_image': 'Выберите изображение',
        }