import cv2
import time
import os
import mediapipe as mp





class User:
    def __init__(self,name,image):
        self.name = name
        self.image = image




def captureRefImg():
    # Open the camera
    # Default number is zero for regular webcam

    capture = cv2.VideoCapture(0)

    # Checking that the camera is opened properly
    if not capture.isOpened():
        raise Exception("Could not open the camera !")


    while True:
        # Reading a frame from the camera
        ret, frame = capture.read()

        # Display the read frame
        cv2.imshow("WebCam", frame)

        # "q" is for quite
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # "c" is for capture the reference image
        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.imwrite("Ref_Image.png", frame, [cv2.IMWRITE_PNG_COMPRESSION, 9])
            print("Taken photo of the user saved as Ref_Image.png")

    # Release the camera
    capture.release()

    # Destroy all windows
    cv2.destroyAllWindows()



def measureDistance():
    # Distance between the camera and the face when taking reference image (Inches)
    refDistance = 24

    # Green colors in BGR Format
    Green = (0, 255, 0)

    # Selected font to display on the image
    fonts = cv2.FONT_HERSHEY_COMPLEX


    cap = cv2.VideoCapture(0)


    # Load the required XML classifiers to detect face in a frame
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


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


    def face_data(image):
        """
        The purpose of this function is detecting the face in real time and return the face width.
        :param image: This function takes an image or a video frame as an argument.
        :return: It returns the face width in the image.
        """
        faceWidth = 0
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(grayImage, 1.3, 5)
        for (x, y, h, w) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), 1)
            faceWidth = w
        return faceWidth


    # Read reference image
    refImage = cv2.imread("Ref_Image.png")

    # Getting the face width in reference image
    ref_faceWidth = face_data(refImage)

    # getting the focal length
    focalLengthFound = focal_length(refDistance, ref_faceWidth)

    print("Focal length , line 121 ")
    print(focalLengthFound)


    while True:

        _, frame = cap.read()

        frameFaceWidth = face_data(frame)

        if frameFaceWidth != 0:
            distance = distance_measure(focalLengthFound, frameFaceWidth)

            cv2.putText(frame, f"Distance : {distance} Inches", (50, 50), fonts, 0.5, (Green), 2)

        cv2.imshow('Camera', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


print("""1 - create account
2 - start
3 - pause
4 - start""")

option = int(input("Enter option : "))

if option==1:
    captureRefImg()
    print("func1")

    # func1()
elif option==2:
    measureDistance()
    print("func2")
    # func2()
elif option==3:
    print("func3")
    # func3()
elif option==4:
    print("func4")
    # func4()
else:
    print("Please enter a correct option number.")