from pymongo import MongoClient
from PIL import Image
import io
class Database:
    def __init__(self):
        print("initializing database connection...")
        self.cluster = MongoClient("mongodb+srv://Pasindu:Pasindu123@eyeforyoudatabase.ds8dliv.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.cluster["EyeForYou"]
        self.collection=self.db["user"]
    def postAccount(self, username, password):
        print("posting - "+username+","+password)
        post = {"userName":username,"password":password,"refImage":None}
        self.collection.insert_one(post)

    def postRefImage(self, username):
        imageFileName = username+".png"
        print("posting image - "+imageFileName)
        result = self.collection.find_one({"userName":username})
        if(result!=None):
            print("username found")
            im = Image.open("imageRes/"+username+".png")
            image_bytes = io.BytesIO()
            im.save(image_bytes, format='PNG')
            image = {
                'refImage': image_bytes.getvalue()
            }
            self.collection.update_one({"userName": username},
                                         {"$set": image})
            print("updated image : ", image)
        else:
            print("Error!: username not found")

    def isAvailable(self, username):
        result = self.collection.find_one({"userName":username})
        if(result==None):
            return False
        else:
            return True

    def getImage(self, username):
        print("getting image from the database and saving to local folder")
        result = self.collection.find_one({"userName":username})
        if result["refImage"] == None:
            raise Exception("No image file saved in the database for user - "+username)
        else:
            pil_img = Image.open(io.BytesIO(result["refImage"]))
            pil_img.save("imageRes"+"\\"+username+".png")
    def hasRefImage(self, username):
        result = self.collection.find_one({"userName":username})
        if result["refImage"] == None:
            return False
        else:
            return True

    def getPassword(self, username):
        result = self.collection.find_one({"userName":username})
        return result["password"]

