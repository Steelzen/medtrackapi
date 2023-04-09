from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from requests import post
from  .firebase import db
from medtrackapi.settings import OPENAI_API_KEY

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
    
@csrf_exempt
def call_openai(request):
    if request.method == 'POST':
        prompt = json.loads(request.body)['prompt']
        temperature = json.loads(request.body)['temperature']
        max_tokens = json.loads(request.body)['max_tokens']

        response = post(
            'https://api.openai.com/v1/engines/davinci/completions',
            headers={'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            },
            json={'prompt':prompt,
                  'max_tokens': max_tokens,
                  'temperature': temperature,
                  },
        )

        if response.status_code == 200:
            return JsonResponse(response.json(), status=200)
        else:
            return JsonResponse({'error': response.text}, status=response.status_code)
        

    return JsonResponse({'error': 'Invalid request method'}, status=400)    

    