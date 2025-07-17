from django.urls import path
from .views import  update_profile,upload_document,user_detail


urlpatterns=[
    path('info/',update_profile,name="update-profile"),
    path('upload-document/', upload_document,name="upload-document"),
    path('details/<int:user_id>/', user_detail, name='user-detail'),

]