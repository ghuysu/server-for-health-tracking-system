import firebase_admin
from firebase_admin import credentials, db
import os

# Config Firebase
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
cred_path = os.path.join(base_dir, 'firebase-cert.json')
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://deviot-ed1d5-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

