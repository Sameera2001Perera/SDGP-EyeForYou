import math

def euclaidean_distance(point, point1):
    x1, y1 = point
    x2, y2 = point1
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance


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