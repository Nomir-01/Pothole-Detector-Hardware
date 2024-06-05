from tensorflow import keras
import numpy as np
import os
from PIL import Image
import cv2

model = keras.models.load_model('trained.h5')

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

def load_image(img_path):
    img = keras.preprocessing.image.load_img(img_path, target_size=(150, 150))
    img_tensor = keras.preprocessing.image.img_to_array(img)                    # (height, width, channels)
    img_tensor = np.expand_dims(img_tensor, axis=0)         # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor /= 255.                                      # imshow expects values in the range [0, 1]
    return img_tensor

PATH = os.path.join(os.getcwd(), 'RoadData')
num_data=len(os.listdir(PATH))
i=1

def check_data(j):
    ret,frame=cam.read()
    if not ret:
        print("Failed to grab frame")
        exit()
    cv2.imshow("Pothole Detector",frame)
    img_name=f"{PATH}\{j}.jpg"
    cv2.imwrite(img_name,frame)

    img = keras.preprocessing.image.load_img(f"{PATH}\{j}.jpg", target_size=(150, 150))
    box2 = (0, 0, 75, 150)
    img2 = img.crop(box2)
    img2.save(f"{PATH}\{j}_a.jpg")

    box3 = (75, 0, 150, 150)
    img3 = img.crop(box3)
    img3.save(f"{PATH}\{j}_b.jpg")

    labels = {0: "Pothole", 1: "Road"}

    img2 = load_image(f"{PATH}\{j}_a.jpg")
    classes_index = (model.predict(img2) > 0.5).astype("int32")
    result1 = labels[classes_index[0][0]]

    img3 = load_image(f"{PATH}\{j}_b.jpg")
    classes_index1 = (model.predict(img3) > 0.5).astype("int32")
    result2 = labels[classes_index1[0][0]]

    if result1 == "Pothole" and result2 == "Pothole":
        print("Slow Down")
    elif result1 == "Pothole" and result2 == "Road":
        print("Pothole On Left")
    elif result1 == "Road" and result2 == "Pothole":
        print("Pothole On Right")
    else:
        print("Keep Going")

    #os.remove(f"{PATH}\{j}.jpg")
    #os.remove(f"{PATH}\{j}_a.jpg")
    #os.remove(f"{PATH}\{j}_b.jpg")
    j=j+1
    run(j)

def run(j):
    check_data(j)
    k=cv2.waitKey(1)
    if k%256 == 27:
        exit()

cam=cv2.VideoCapture(0)
run(i)
