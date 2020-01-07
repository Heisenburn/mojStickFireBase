import pyrebase

config = {
    "apiKey": "AIzaSyBSoaetl0Gd9xe8SGzT5YefiTFjoEDwyf4",
    "authDomain": "mojstick-72ecb.firebaseapp.com",
    "databaseURL": "https://mojstick-72ecb.firebaseio.com",
    "projectId": "mojstick-72ecb",
    "messagingSenderId": "912823611803",
    "storageBucket": "mojstick-72ecb.appspot.com",
    "serviceAccount": "mojstick-72ecb-firebase-adminsdk-qua8y-ee203791f7.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def updateStick(textToUpdate):
    db.child("notatki").child("-LvFs7_CBp-KcuASoIJA").set({"stick": textToUpdate})


def getStickValue():
    stickFromFireBase = db.child("notatki").child("-LvFs7_CBp-KcuASoIJA").get().val()['stick']
    return stickFromFireBase


