import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

data={'Latitude':0,'Longitude':0,'Type':'Pothole','Observation':'Middle'}
db.collection('Location').document(f'Pothole_1').set(data)
