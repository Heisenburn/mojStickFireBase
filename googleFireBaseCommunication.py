import pyrebase


config = {
    "apiKey": "AIzaSyA6l04lL9R8hHRJc2Ri67kAnfDW697WezI",
    "authDomain": "mojstickpy.firebaseapp.com",
    "databaseURL": "https://mojstickpy.firebaseio.com",
    "projectId": "mojstickpy",
    "storageBucket": "mojstickpy.appspot.com",
    "messagingSenderId": "96104255538",
    "appId": "1:96104255538:web:e81dbd194df664d6b12c2b"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def updateStick(textToUpdate):

    db.set({"stick": textToUpdate})

def getStickValue():
    stickFromFireBase = list(db.child().get().val().items())[0][1]
    return stickFromFireBase


