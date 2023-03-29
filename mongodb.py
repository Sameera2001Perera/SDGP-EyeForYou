from pymongo import MongoClient
from PIL import Image
import io


cluster = None
db = None
collection = None
def init():
    print("initializing database connection...")
    global cluster
    cluster = MongoClient("mongodb+srv://Pasindu:Pasindu123@eyeforyoudatabase.ds8dliv.mongodb.net/?retryWrites=true&w=majority")
    global db
    db = cluster["EyeForYou"]
    global collection
    collection = db["user"]

def postAccount(username, password):
    print("posting - " + username + "," + password)
    post = {"userName": username, "password": password, "refImage": None, "lowDistanceWarnings": 0}
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


def postEyeBlinkWarning(username):
    collection.update_one({
        'userName': username
    }, {
        '$inc': {
            'lowDistanceWarnings': 1
        }
    }, upsert=False)


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
