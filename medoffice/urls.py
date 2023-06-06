from django.urls import path
from . import views

urlpatterns = [
    path('get_document_all/<str:collection_name>/', views.get_document_all, name='get_document_all'),
    path('get_document/<str:collection_name>/<str:document_id>/', views.get_document, name='get_document'),
    path('get_patient_list/<str:collection_name>/<str:document_id>/', views.get_patient_list, name='get_patient_list'),
    path('add_medistaff/<str:collection_name>/<str:document_id>/<str:user_id>/<str:license_number>/<str:position>/<str:first_name>/<str:last_name>/<str:date_of_birth>/<str:address>/<str:city>/<str:state>/<str:zip>/<str:phone>/<str:role>/<str:organisation>/', views.add_medistaff, name='add_medistaff'),
    path('add_patient/<str:collection_name>/<str:document_id>/<str:user_id>/<str:position>/<str:first_name>/<str:last_name>/<str:date_of_birth>/<str:address>/<str:city>/<str:state>/<str:zip>/<str:phone>/', views.add_patient, name='add_patient'),
    path('register_patient_list/<str:collection_name>/<str:document_id>/', views.register_patient_list, name='register_patient_list'),
    path('register_patient_list/<str:collection_name>/<str:document_id>/add_patient_on_list/<str:patient_id>/', views.add_patient_on_list, name='add_patient_on_list'),
    path('register_patient_list/<str:collection_name>/<str:document_id>/delete_patient_on_list/<str:patient_id>/', views.delete_patient_on_list, name='delete_patient_on_list'),
    path('openai/', views.call_openai, name='call_openai'),
]