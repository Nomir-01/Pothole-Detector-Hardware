from tensorflow import keras
import numpy as np
import os
from PIL import Image
import cv2
from gpiozero import LED
import serial
import pynmea2
import firebase_admin
from firebase_admin import credentials, firestore
import time
import urllib.request
import datetime

path='/home/nomir/Desktop/Project/'

ServerPATH ='/home/nomir/Desktop/Project/ServerRoadData'
training_path = '/home/nomir/Desktop/Project/ServerObstacleData'
training_limit = 100

model_path = os.path.join(path, 'Otrained.h5')

model = keras.models.load_model(model_path)

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

def load_image(img_path):
    img = keras.preprocessing.image.load_img(img_path, target_size=(150, 150))
    img_tensor = keras.preprocessing.image.img_to_array(img)                    # (height, width, channels)
    img_tensor = np.expand_dims(img_tensor, axis=0)         # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor /= 255.                                      # imshow expects values in the range [0, 1]
    return img_tensor

PATH = os.path.join(path, 'RoadData')
num_data=len(os.listdir(PATH))
i=1

def check_data(j):
    port="/dev/ttyAMA0"
    ser=serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    newdata=ser.readline().decode('unicode_escape')
    ret,frame=cam.read()
    if not ret:
        print("Failed to grab frame")
        exit()
    cv2.namedWindow("Pothole Detector", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Pothole Detector", 700, 800)
    cv2.imshow("Pothole Detector",frame)
    img_name=f"{PATH}/{j}.jpg"
    cv2.imwrite(img_name,frame)

    img = keras.preprocessing.image.load_img(f"{PATH}/{j}.jpg", target_size=(150, 150))
    box2 = (0, 0, 75, 150)
    img2 = img.crop(box2)
    img2.save(f"{PATH}/{j}_a.jpg")

    box3 = (75, 0, 150, 150)
    img3 = img.crop(box3)
    img3.save(f"{PATH}/{j}_b.jpg")

    labels = {0: "Pothole", 1: "Road"}

    img2 = load_image(f"{PATH}/{j}_a.jpg")
    classes_index = (model.predict(img2) > 0.5).astype("int32")
    result1 = labels[classes_index[0][0]]

    img3 = load_image(f"{PATH}/{j}_b.jpg")
    classes_index1 = (model.predict(img3) > 0.5).astype("int32")
    result2 = labels[classes_index1[0][0]]

    if result1 == "Pothole" and result2 == "Pothole":
        print("Slow Down")
        ledRight.off()
        ledLeft.off()
        ledMiddle.on()
        
        training_image_list = os.listdir('ServerObstacleData')
        training_path_data = ["ServerObstacleData/{0}".format(x) for x in training_image_list]
        if len(training_image_list) == training_limit:
            oldest_file = min(training_path_data, key=os.path.getctime)
            os.remove(oldest_file)
            curr_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]
            img.save(f"{training_path}/Pothole_{curr_datetime}.jpg")
        else:
            curr_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]
            img.save(f"{training_path}/Pothole_{curr_datetime}.jpg")
            
        if newdata[0:6] == "$GPRMC":
            newmsg=pynmea2.parse(newdata)
            latN=newmsg.latitude
            lngN=newmsg.longitude
            if latN == latO and lngN == lngO:
                print('No New Location')
            else:
                print(f'Latitude: {latN}')
                print(f'Longitude: {lngN}')
                f = open("counter.txt", "r")
                k=int(f.read())
                data={'Latitude':latN,'Longitude':lngN,'Type':'Pothole','Observation':'Middle'}
                db.collection('Pothole Location').document(f'Pothole_{k}').set(data)
                k=k+1
                f = open("counter.txt", "w")
                f.write(f"{k}")
                f.close()

    elif result1 == "Pothole" and result2 == "Road":
        print("Pothole On Left")
        ledMiddle.off()
        ledRight.off()
        ledLeft.on()
        
        training_image_list = os.listdir('ServerObstacleData')
        training_path_data = ["ServerObstacleData/{0}".format(x) for x in training_image_list]
        if len(training_image_list) == training_limit:
            oldest_file = min(training_path_data, key=os.path.getctime)
            os.remove(oldest_file)
            curr_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]
            img.save(f"{training_path}/Pothole_{curr_datetime}.jpg")
        else:
            curr_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]
            img.save(f"{training_path}/Pothole_{curr_datetime}.jpg")
            
        if newdata[0:6] == "$GPRMC":
            newmsg=pynmea2.parse(newdata)
            latN=newmsg.latitude
            lngN=newmsg.longitude
            if latN == latO and lngN == lngO:
                print('No New Location')
            else:
                f = open("counter.txt", "r")
                k=int(f.read())
                print(f'Latitude: {latN}')
                print(f'Longitude: {lngN}')
                data={'Latitude':latN,'Longitude':lngN,'Type':'Pothole','Observation':'Left'}
                db.collection('Pothole Location').document(f'Pothole_{k}').set(data)
                k=k+1
                f = open("counter.txt", "w")
                f.write(f"{k}")
                f.close()
                
    elif result1 == "Road" and result2 == "Pothole":
        print("Pothole On Right")
        ledLeft.off()
        ledMiddle.off()
        ledRight.on()
        
        training_image_list = os.listdir('ServerObstacleData')
        training_path_data = ["ServerObstacleData/{0}".format(x) for x in training_image_list]
        if len(training_image_list) == training_limit:
            oldest_file = min(training_path_data, key=os.path.getctime)
            os.remove(oldest_file)
            curr_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]
            img.save(f"{training_path}/Pothole_{curr_datetime}.jpg")
        else:
            curr_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]
            img.save(f"{training_path}/Pothole_{curr_datetime}.jpg")
            
        if newdata[0:6] == "$GPRMC":
            newmsg=pynmea2.parse(newdata)
            latN=newmsg.latitude
            lngN=newmsg.longitude
            if latN == latO and lngN == lngO:
                print('No New Location')
            else:
                f = open("counter.txt", "r")
                k=int(f.read())
                print(f'Latitude: {latN}')
                print(f'Longitude: {lngN}')
                data={'Latitude':latN,'Longitude':lngN,'Type':'Pothole','Observation':'Right'}
                db.collection('Pothole Location').document(f'Pothole_{k}').set(data)
                k=k+1
                f = open("counter.txt", "w")
                f.write(f"{k}")
                f.close()
                
    else:
        print("Keep Going")
        ledLeft.off()
        ledMiddle.off()
        ledRight.off()

    os.remove(f"{PATH}/{j}.jpg")
    os.remove(f"{PATH}/{j}_a.jpg")
    os.remove(f"{PATH}/{j}_b.jpg")
    j=j+1
    run(j)

def run(j):
    k=cv2.waitKey(1)
    if k%256 == 27:
        ledLeft.off()
        ledMiddle.off()
        ledRight.off()
        
        ledLeft.on()
        ledMiddle.on()
        ledRight.on()
        
        time.sleep(5)
        
        ledLeft.off()
        ledMiddle.off()
        ledRight.off()
        print('exit')
        exit()
    else:
        check_data(j)

ledLeft = LED(17)
ledMiddle = LED(27)
ledRight = LED(22)

ledLeft.off()
ledMiddle.off()
ledRight.off()

ledLeft.on()
ledRight.on()

time.sleep(5)

ledLeft.off()
ledRight.off()

host='http://google.com'
try:
    urllib.request.urlopen(host)
    status = "Connected"
except:
    status = "Not connected"
    print(status)
    ledLeft.on()
    ledMiddle.on()
    ledRight.on()

    time.sleep(5)

    ledLeft.off()
    ledMiddle.off()
    ledRight.off()
    
    exit()
    
    
print(status)
    

latO=0
lngO=0

cred_path= os.path.join(path, 'serviceAccountKey.json')
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

cam=cv2.VideoCapture(0)
run(i)
