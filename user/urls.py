from django.urls import path
from .views import  update_profile,upload_document


urlpatterns=[
    path('info/',update_profile,name="update-profile"),
    path('upload-document/', upload_document,name="upload-document"),

]