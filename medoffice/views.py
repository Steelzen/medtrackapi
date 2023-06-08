from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
import json
import openai
import traceback
from requests import post
from firebase_admin import auth
from  .firebase import db, firestore
from medtrackapi.settings import OPENAI_API_KEY

# Create your views here.
def get_all_users(request):
    try:
        users = auth.list_users()
        user_list = [{'uid': user.uid, 'email': user.email} for user in users.iterate_all()]
        return JsonResponse(user_list, safe=False)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


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

def get_patient_list(request, collection_name, document_id):
    document_ref = db.collection(collection_name).document(document_id)
    doc = document_ref.get()
    
    if not doc.exists:
        return JsonResponse({'error': 'Document does not exist'}, status=404)
    
    patient_list = doc.to_dict().get('patient_list', [])
    return JsonResponse({'patient_list': patient_list}, status=200)

      

def add_medistaff(request, collection_name, document_id, user_id, license_number, position, first_name, last_name, date_of_birth, address, city, state, zip, phone, role, organisation):
    document_ref = db.collection(collection_name).document(document_id)
    doc = document_ref.get()
    if doc.exists:
        return JsonResponse({'error': 'Document already exists'}, status=400)
    else:
        document_ref.set({
            'user_id':  user_id,
            'license_number': license_number,
            'position': position,
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': date_of_birth,
            'address': address,
            'city': city,
            'state': state,
            'zip': zip,
            'phone': phone,
            'role': role,
            'organisation': organisation,
        })
        return JsonResponse({'message': 'Document added successfully'}, status=201)


def add_patient(request, collection_name, document_id, user_id, position, first_name, last_name, date_of_birth, address, city, state, zip, phone):
    document_ref = db.collection(collection_name).document(document_id)
    doc = document_ref.get()
    if doc.exists:
        return JsonResponse({'error': 'Document already exists'}, status=400)
    else:
        document_ref.set({
            'user_id':  user_id,
            'position': position,
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': date_of_birth,
            'address': address,
            'city': city,
            'state': state,
            'zip': zip,
            'phone': phone,
        })
        return JsonResponse({'message': 'Document added successfully'}, status=201)
    
def register_patient_list(request, collection_name, document_id):
    document_ref = db.collection(collection_name).document(document_id)
    doc = document_ref.get()
    if doc.exists:
        return JsonResponse({'error': 'Document already exists'}, status=400)
    else:
        document_ref.set({
            'patient_list': [],
        })
        return JsonResponse({'message': 'Document added successfully'}, status=201)
    

def add_patient_on_list(request, collection_name, document_id, patient_id):
    document_ref = db.collection(collection_name).document(document_id)
    doc = document_ref.get()
    if not doc.exists:
        return JsonResponse({'error': 'Document does not exist'}, status=404)
    
    document_ref.update({
        'patient_list': firestore.ArrayUnion([patient_id]),
    })
    
    return JsonResponse({'message': 'Patient added successfully'}, status=200)

def delete_patient_on_list(request, collection_name, document_id, patient_id):
    document_ref = db.collection(collection_name).document(document_id)
    doc = document_ref.get()
    if not doc.exists:
        return JsonResponse({'error': 'Document does not exist'}, status=404)
    
    document_ref.update({
        'patient_list': firestore.ArrayRemove([patient_id]),
    })
    
    return JsonResponse({'message': 'Patient deleted successfully'}, status=200)


      
@csrf_exempt
def call_openai(request):
    if request.method == 'POST':
        prompt = json.loads(request.body)['prompt']
        temperature = json.loads(request.body)['temperature']
        max_tokens = json.loads(request.body)['max_tokens']

        response = post(
            'https://api.openai.com/v1/completions',
            headers={'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            },
            json={
            'model':'text-davinci-002',
            'prompt':prompt,
                  'max_tokens': max_tokens,
                  'temperature': temperature,
                  },
        )

        if response.status_code == 200:
            return JsonResponse(response.json(), status=200)
        else:
            return JsonResponse({'error': response.text}, status=response.status_code)
        

    return JsonResponse({'error': 'Invalid request method'}, status=400)
