from django.urls import path
from . import views

urlpatterns = [
    path('', views.ImageEditorView.as_view(), name='image_editor'),
]