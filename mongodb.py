from pymongo import MongoClient
from PIL import Image
import io
from datetime import datetime



cluster = None
db = None
collection = None
date = None#date and time of the session
currentSession = None#current sesion
def init():
    print("initializing database connection...")
    global cluster
    cluster = MongoClient("mongodb+srv://Pasindu:Pasindu123@eyeforyoudatabase.ds8dliv.mongodb.net/?retryWrites=true&w=majority")
    global db
    db = cluster["EyeForYou"]
    global collection
    collection = db["user"]

def sesionInit(username):
    print("initializing new session in database...")
    global cluster
    cluster = MongoClient("mongodb+srv://Pasindu:Pasindu123@eyeforyoudatabase.ds8dliv.mongodb.net/?retryWrites=true&w=majority")
    global db
    db = cluster["EyeForYou"]
    global collection
    collection = db["user"]
    global date
    date = datetime.now()
    postSession(username=username)

def postAccount(username, password):
    print("posting - " + username + "," + password)

    post = {"userName": username,
            "password": password,
            "refImage": None,
            "lowDistanceWarnings": 0,
            "sessions":[]}

    collection.insert_one(post)


def postRefImage(username):
    imageFileName = username + ".png"
    print("posting image - " + imageFileName)
    result = collection.find_one({"userName": username})
    if (result != None):
        print("username found")
        im = Image.open("imageRes/" + username + ".png")
        image_bytes = io.BytesIO()
        im.save(image_bytes, format='PNG')
        image = {
            'refImage': image_bytes.getvalue()
        }
        collection.update_one({"userName": username},
                                   {"$set": image})
        print("updated image : ", image)
    else:
        print("Error!: username not found")


def postSession(username):
    global date
    filter = {"userName": username}
    update = {
        "$push": {
            "sessions": {
                "start_time": date,
                "blinkWarnings": 0,
                "distanceWarnings": 0
            }
        }
    }

    result = collection.update_one(filter, update)

    print(result.modified_count)  # Check the number of documents modified

def postEyeBlinkWarning(username):
    global date
    filter = {"userName": username, "sessions.start_time": date}
    update = {"$inc": {"sessions.$.blinkWarnings": 1}}  # Update the duration to 5400 seconds (1.5 hours)

    result = collection.update_one(filter, update)

    print(result.modified_count)  # Check the number of documents modified
def postEyeDistanceWarning(username):
    global date
    filter = {"userName": username, "sessions.start_time": date}
    update = {"$inc": {"sessions.$.distanceWarnings": 1}}  # Update the duration to 5400 seconds (1.5 hours)

    result = collection.update_one(filter, update)

    print(result.modified_count)  # Check the number of documents modified
def isAvailable(username):
    result = collection.find_one({"userName": username})
    if (result == None):
        return False
    else:
        return True


def getImage(username):
    print("getting image from the database and saving to local folder")
    result = collection.find_one({"userName": username})
    if result["refImage"] == None:
        raise Exception("No image file saved in the database for user - " + username)
    else:
        pil_img = Image.open(io.BytesIO(result["refImage"]))
        pil_img.save("imageRes" + "\\" + username + ".png")


def hasRefImage(username):
    result = collection.find_one({"userName": username})
    if result["refImage"] == None:
        return False
    else:
        return True


def getPassword(username):
    result = collection.find_one({"userName": username})
    return result["password"]
