import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

f = open("counter.txt", "r")

i=int(f.read())
lat=0
lng=1

data={'Latitude':lat,'Longitude':lng,'Type':'Pothole'}
db.collection('Location').document(f'Pothole_{i}').set(data)

i=i+1
f = open("counter.txt", "w")
f.write(f"{i}")
f.close()





