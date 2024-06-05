from tensorflow import keras
import numpy as np
import os
from PIL import Image
import datetime

model = keras.models.load_model('Otrained.h5')

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
training_path = os.path.join(os.getcwd(), 'ObstacleData')
training_limit = 10
num_data=len(os.listdir(PATH))
i=1

def check_data(j):
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
        training_image_list = os.listdir('ObstacleData')
        training_path_data = ["ObstacleData/{0}".format(x) for x in training_image_list]
        if len(training_image_list) == training_limit:
            oldest_file = min(training_path_data, key=os.path.getctime)
            os.remove(oldest_file)
            curr_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]
            img.save(f"{training_path}\Pothole_{curr_datetime}.jpg")
        else:
            curr_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]
            img.save(f"{training_path}\Pothole_{curr_datetime}.jpg")
    elif result1 == "Pothole" and result2 == "Road":
        print("Pothole On Left")
        training_image_list = os.listdir('ObstacleData')
        training_path_data = ["ObstacleData/{0}".format(x) for x in training_image_list]
        if len(training_image_list) == training_limit:
            oldest_file = min(training_path_data, key=os.path.getctime)
            os.remove(oldest_file)
            curr_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]
            img.save(f"{training_path}\Pothole_{curr_datetime}.jpg")
        else:
            curr_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]
            img.save(f"{training_path}\Pothole_{curr_datetime}.jpg")
    elif result1 == "Road" and result2 == "Pothole":
        print("Pothole On Right")
        training_image_list = os.listdir('ObstacleData')
        training_path_data = ["ObstacleData/{0}".format(x) for x in training_image_list]
        if len(training_image_list) == training_limit:
            oldest_file = min(training_path_data, key=os.path.getctime)
            os.remove(oldest_file)
            curr_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]
            img.save(f"{training_path}\Pothole_{curr_datetime}.jpg")
        else:
            curr_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]
            img.save(f"{training_path}\Pothole_{curr_datetime}.jpg")
    else:
        print("Keep Going")

    os.remove(f"{PATH}\{j}.jpg")
    os.remove(f"{PATH}\{j}_a.jpg")
    os.remove(f"{PATH}\{j}_b.jpg")
    j=j+1
    run(j)

def run(j):
    if j!= num_data+1:
        check_data(j)
    else:
        exit()

run(i)
