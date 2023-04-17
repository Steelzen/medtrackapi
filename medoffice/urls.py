from django.urls import path
from . import views

urlpatterns = [
    path('get_document_all/<str:collection_name>/', views.get_document_all, name='get_document_all'),
    path('get_document/<str:collection_name>/<str:document_id>/', views.get_document, name='get_document'),
    path('add_document/<str:collection_name>/<str:document_id>/<str:content1>/<str:content2>/', views.add_document, name='add_document'),
    path('add_medistaff/<str:collection_name>/<str:document_id>/<str:user_id>/<str:license_number>/', views.add_medistaff, name='add_medistaff'),
    path('openai/', views.call_openai, name='call_openai'),
]