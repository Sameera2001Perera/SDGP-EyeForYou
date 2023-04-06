import cv2
import numpy as np
from keras.models import load_model

modell=load_model('model_file.h5')

face_Detectt=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

labels_dict_c={0:'Angry',1:'Disgust', 2:'Fear', 3:'Happy',4:'Neutral',5:'Sad',6:'Surprise'}

# len(number_of_image), image_height, image_width, channel

framee=cv2.imread("faces-small.jpg")
gray_y=cv2.cvtColor(framee, cv2.COLOR_BGR2GRAY)
facess= face_Detectt.detectMultiScale(gray_y, 1.3, 3)
for x,y,w,h in facess:
    sub_face_img=gray_y[y:y+h, x:x+w]
    resized_d=cv2.resize(sub_face_img,(48,48))
    normalize_e=resized_d/255.0
    reshapedd=np.reshape(normalize_e, (1, 48, 48, 1))
    result_t=modell.predict(reshapedd)
    label=np.argmax(result_t, axis=1)[0]
    print(label)

    cv2.putText(framee, labels_dict_c[label], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(50,50,255),2)
        
cv2.imshow("Frame",framee)
cv2.waitKey(0)
cv2.destroyAllWindows()