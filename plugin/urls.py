from django.urls import path
from . import views

urlpatterns = [
    path('size_recommendation/', views.size_recommendation,
         name='size_recommendation'),
    path('index/', views.index,
         name='index'),
    path('image_upload/', views.image_upload,
         name='image_upload'),
]

