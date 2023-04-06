# EyeForYou: Real-time Emotion Detection and Eye Blinking System

EyeForYou is a real-time emotion detection and eye blinking system that uses computer vision and machine learning techniques to detect user emotions and eye blinks. The system is built using Python programming language and Tkinter graphical user interface (GUI) library. OpenCV is used for face detection in real-time, while facial landmarks are captured in real-time using the Mediapipe library. Convolutional Neural Network (CNN) is used for facial emotion recognition in real-time. MongoDB Atlas cloud database service is used as a database to save user login information and usage data, which is connected with the front end using the pymongo python library.

## Technologies Used
- Python
- Tkinter
- OpenCV
- Mediapipe
- Convolutional Neural Network (CNN)
- Google Collab
- MongoDB Atlas
- PyMongo

## Getting Started
To run the EyeForYou system, you need to follow these steps:

1. Clone the EyeForYou repository
2. Install all required dependencies using `pip install -r requirements.txt`
3. Open the terminal and navigate to the directory where the cloned repository is saved
4. Run `python main.py` to start the system

## Usage
The EyeForYou system has a simple and user-friendly interface. Once the system is started, the user needs to create an account or login if they already have an account. After successful login, the system will start detecting the user's face and eyes. The user's emotions will be displayed in real-time on the screen, and the system will also alert the user if they are not blinking enough. The user can also view their usage statistics, including the time spent using the system and the number of times they blinked their eyes.

## Future Work
In the future, we plan to improve the accuracy of emotion detection by using more advanced machine learning techniques. We also plan to add more features, such as user-specific settings and personalized recommendations for reducing eye strain.



