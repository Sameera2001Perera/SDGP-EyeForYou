from guiFrames.loginGui import LoginApp
from guiFrames.loginGui import MainApplicationFrame

import os
import mongodb

if __name__ == "__main__":
    try:
        database = mongodb.Database()
    except Exception as e:
        raise Exception("Database Connection Failed! (Possible : network error!)")
        exit()

    app = LoginApp(database)

    dirPath = "imageRes"

    if (not os.path.exists(dirPath)):
        os.makedirs(dirPath)
        print("The new directory imageRes is created")

    pngs = os.listdir(dirPath)

    if len(pngs) > 1:
        raise Exception("More than 1 ref image found in the app folder")
    elif len(pngs) == 1:
        username = pngs[0].split(".")[0]
        print("username from files - - "+username)
        app.accountFrame.destroy()
        app.placeFrame(MainApplicationFrame(master=app, db=database, userName=username, width=620, height=550, corner_radius=15))
        app.mainloop()
    else:
        app.mainloop()
