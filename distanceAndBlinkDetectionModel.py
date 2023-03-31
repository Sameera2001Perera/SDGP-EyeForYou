import cv2
import os
from winotify import Notification, audio
import mongodb as db
import mediapipe as mp
import time
import math
import numpy as np


# Distance between the camera and the face when taking reference image (Inches)
refDistance = 24

# Green colors in BGR Format
green = (0, 255, 0)

# Selected font to display on the image
fonts = cv2.FONT_HERSHEY_COMPLEX



# Left eyes indices
leftEye = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]

# right eyes indices
rightEye = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]

# mediapipe face mesh
map_face_mesh = mp.solutions.face_mesh



def face_data(image):
    """
    The purpose of this function is detecting the face in real time and return the face width.
    :param image: This function takes an image or a video frame as an argument.
    :return: It returns the face width in the image.
    """

    # Load the required XML classifiers to detect face in a frame
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faceWidth = 0
    faces = face_cascade.detectMultiScale(grayImage, 1.3, 5)
    for (x, y, h, w) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), 1)
        faceWidth = w

    return faceWidth

def getRefImage():
    search_root_directory = os.getcwd()

    # Recursively construct list of files under root directory.
    all_files_recursive = sum(
        [[os.path.join(root, f) for f in files] for root, dirs, files in
         os.walk(search_root_directory + '\imageRes')], [])

    # Define function to tell if a given file is an image
    # Example: search for .png extension.
    def is_an_image(fpath):
        return os.path.splitext(fpath)[-1] in ('.png')

    # Take the first matching result. Note: throws StopIteration if not found
    first_image_file = next(filter(is_an_image, all_files_recursive))
    return first_image_file




# function : landmark detection

def landmarks_detection(image, results, draw=False):
    imgHeight, imgWidth = image.shape[:2]

    meshCoord = [(int(point.x * imgWidth), int(point.y * imgHeight)) for point in results.multi_face_landmarks[0].landmark]
    if draw:
        [cv.circle(image, p, 2, green, -1) for p in meshCoord]

    # return the tuple list for each landmark
    return meshCoord




# function : euclaidean distance

def euclaidean_distance(point, point1):
    x1, y1 = point
    x2, y2 = point1
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance



# function : Blink Ratio

def blink_ratio(landmarks, rightIndices, leftIndices):
    # right eye
    # horizontal line
    r_right = landmarks[rightIndices[0]]
    r_left = landmarks[rightIndices[8]]
    # vertical line
    r_top = landmarks[rightIndices[12]]
    r_bottom = landmarks[rightIndices[4]]

    # left eye
    # horizontal line
    l_right = landmarks[leftIndices[0]]
    l_left = landmarks[leftIndices[8]]

    # vertical line
    l_top = landmarks[leftIndices[12]]
    l_bottom = landmarks[leftIndices[4]]

    rHoriDistance = euclaidean_distance(r_right, r_left)
    rVertDistance = euclaidean_distance(r_top, r_bottom)

    lVertDistance = euclaidean_distance(l_top, l_bottom)
    lHoriDistance = euclaidean_distance(l_right, l_left)

    rEyeRatio = rHoriDistance / rVertDistance
    lEyeRatio = lHoriDistance / lVertDistance

    ratio = (rEyeRatio + lEyeRatio) / 2
    return ratio







def measureDistance(username):

    # initialize database
    db.init()

    cap = cv2.VideoCapture(0)

    def focal_length(refDistance, rf_imageWidth):
        """
        The purpose of this function is calculating the focal length. The distance between the camera lens and the CMOS sensor
        is called as focal length. Distance from object to the Camera while Capturing Reference image, Actual width of object
        and width of object in reference image. When the user moves closer to the screen and moves away from the screen,
        Actual width of object (face width) does not change. Therefore, this function does not consider Actual width of object.
        :param refDistance: Distance from object to the Camera while Capturing Reference image
        :param rf_imageWidth: width of object in reference image
        :return: It returns the focal length of camera
        """
        focal_length = (rf_imageWidth * refDistance)
        return focal_length

    def distance_measure(focalLength, frame_face_width):
        """
        The purpose of this function is measuring the distance between face and the camera.
        :param focalLength: Returned value of focal_length(refDistance, rf_imageWidth) function.
        :param frame_face_width: Width of the frame.(A video is considered as a set of frames)
        :return: It returns the distance between face and the camera.
        """
        distance = focalLength / frame_face_width
        return distance


    # Read reference image
    refImage = cv2.imread(getRefImage())

    # Getting the face width in reference image
    ref_faceWidth = face_data(refImage)

    # getting the focal length
    focalLengthFound = focal_length(refDistance, ref_faceWidth)

    print("Focal length , line 121 ")
    print(focalLengthFound)

    toast_lowDistance = Notification(app_id="EyeForYou", title="keep distance", msg="You are too close to the monitor!",
                         duration="short")
    toast_lowDistance.set_audio(audio.SMS, loop=False)

    toast_lowBlinkRate = Notification(app_id="EyeForYou", title="keep blink rate", msg="Low blink rate detected!",
                         duration="short")
    toast_lowBlinkRate.set_audio(audio.SMS, loop=False)



    frameCounter_1 = 0   #

    # Blink detection variables
    closeEyeFrameCounter = 0
    totalBlinks = 0
    closedEyeFrames = 3

    with map_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:

        # start time
        startTime = time.time()

        while True:

            frameCounter_1 += 1

            _, frame = cap.read()




            frameFaceWidth = face_data(frame)

            # grayImage = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            results = face_mesh.process(frame)




            if frameFaceWidth != 0:   # check whether if the face is detected or not

                # Eye blink detection process

                if results.multi_face_landmarks:
                    meshCoords = landmarks_detection(frame, results, False)
                    ratio = blink_ratio(meshCoords, rightEye, leftEye)
                    print(ratio)

                    if ratio > 4.0:
                        closeEyeFrameCounter += 1
                        cv2.putText(frame, 'Blink', (200, 50), fonts, 1.3, green, 2)

                    else:
                        if closeEyeFrameCounter > closedEyeFrames:
                            totalBlinks += 1
                            closeEyeFrameCounter = 0
                    cv2.putText(frame, f'Total Blinks: {totalBlinks}', (100, 150), fonts, 0.6, green, 2)

                # Distance estimation process

                distance = distance_measure(focalLengthFound, frameFaceWidth)


                cv2.putText(frame, f"Distance : {distance} Inches", (50, 50), fonts, 0.5, (green), 2)

                if (frameCounter_1 > 25): # Notification for low distance
                    if (distance < 17):
                        print("low distance")
                        toast_lowDistance.show()
                        db.postEyeBlinkWarning(username)
                    frameCounter_1 = 0



                if ((time.time() - startTime) > 40):   # Calculate blink rate
                    print(time.time() - startTime)
                    if (12 > totalBlinks):
                        print("Low blink rate")
                        toast_lowBlinkRate.show()
                    totalBlinks = 0
                    startTime = time.time()



            cv2.imshow('Camera', frame)

            if cv2.waitKey(1) == ord('q'):
                break


            time.sleep(0.2)


    cap.release()
    cv2.destroyAllWindows()
