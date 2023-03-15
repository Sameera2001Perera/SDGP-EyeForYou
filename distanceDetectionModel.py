import cv2
import os

def getRefImage():
    search_root_directory = os.getcwd()

    # Recursively construct list of files under root directory.
    all_files_recursive = sum(
        [[os.path.join(root, f) for f in files] for root, dirs, files in os.walk(search_root_directory+'\imageRes')], [])

    # Define function to tell if a given file is an image
    # Example: search for .png extension.
    def is_an_image(fpath):
        return os.path.splitext(fpath)[-1] in ('.png')

    # Take the first matching result. Note: throws StopIteration if not found
    first_image_file = next(filter(is_an_image, all_files_recursive))
    return first_image_file

def measureDistance():
    # Distance between the camera and the face when taking reference image (Inches)
    refDistance = 24

    # mainFrame = mainFrame[0][0]

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
    refImage = cv2.imread(getRefImage())

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

            # mainFrame.setDis(f"Distance : {distance} Inches")

        cv2.imshow('Camera', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
