from django.shortcuts import render
from django.http import JsonResponse
from  .firebase import db

# Create your views here.
def get_document_all(request, collection_name):
    docs = db.collection(collection_name).get()
    return JsonResponse({'docs': [doc.to_dict() for doc in docs]})

def get_document(request, collection_name, document_id):
    document_ref = db.collection(collection_name).document(document_id)
    doc = document_ref.get()
    if doc.exists:
        return JsonResponse(doc.to_dict())
    else:
        return JsonResponse({'error': 'Document not found'}, status=404)
    
def add_document(request, collection_name, document_id, content1, content2):
    document_ref = db.collection(collection_name).document(document_id)
    doc = document_ref.get()
    if doc.exists:
        return JsonResponse({'error': 'Document already exists'}, status=400)
    else:
        document_ref.set({
            'content1':  content1,
            'content2': content2,
        })
        return JsonResponse({'message': 'Document added successfully'}, status=201)
    