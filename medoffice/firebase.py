import os
import firebase_admin
from firebase_admin import credentials, firestore


# Set up Firebase credentials
current_file_path = os.path.abspath(__file__)
parent_of_parent_folder_path = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
json_file_path = os.path.join(parent_of_parent_folder_path, 'medtrack-b54f3-firebase-adminsdk-e28m3-98994087b8.json')

cred = credentials.Certificate(json_file_path)
firebase_admin.initialize_app(cred)


# GEt a firestore client
db = firestore.client()
