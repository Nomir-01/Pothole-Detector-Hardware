from flask import Flask, request, jsonify
import cv2
import numpy as np
import os
from tensorflow import keras
import datetime

model = keras.models.load_model('trained.h5')

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

PATH = os.path.join(os.getcwd(), 'ServerRoadData')
training_path = os.path.join(os.getcwd(), 'ServerObstacleData')
training_limit = 10
app = Flask(__name__)

@app.route('/process-image', methods=['POST'])
def process_image():
    i = 1
    print('send')
    #file = request.files['image']
    #img_bytes = file.read()
    #img_array = np.frombuffer(img_bytes, np.uint8)
    #img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    nparr = np.fromstring(request.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img_name = f"{PATH}\{i}.jpg"
    cv2.imwrite(img_name, img)
    img = keras.preprocessing.image.load_img(f"{PATH}\{i}.jpg", target_size=(150, 150))
    box2 = (0, 0, 75, 150)
    img2 = img.crop(box2)
    img2.save(f"{PATH}\{i}_a.jpg")

    box3 = (75, 0, 150, 150)
    img3 = img.crop(box3)
    img3.save(f"{PATH}\{i}_b.jpg")

    labels = {0: "Pothole", 1: "Road"}

    img2 = load_image(f"{PATH}\{i}_a.jpg")
    classes_index = (model.predict(img2) > 0.5).astype("int32")
    result1 = labels[classes_index[0][0]]

    img3 = load_image(f"{PATH}\{i}_b.jpg")
    classes_index1 = (model.predict(img3) > 0.5).astype("int32")
    result2 = labels[classes_index1[0][0]]

    if result1 == "Pothole" and result2 == "Pothole":
        print("Slow Down")
        result = {'message': 'Slow Down'}
        training_image_list = os.listdir('ServerObstacleData')
        training_path_data = ["ServerObstacleData/{0}".format(x) for x in training_image_list]
        if len(training_image_list) == training_limit:
            oldest_file = min(training_path_data, key=os.path.getctime)
            os.remove(oldest_file)
            curr_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]
            img.save(f"{training_path}\Pothole_{curr_datetime}.jpg")
            return jsonify(result)
        else:
            curr_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]
            img.save(f"{training_path}\Pothole_{curr_datetime}.jpg")
            return jsonify(result)

    elif result1 == "Pothole" and result2 == "Road":
        print("Pothole On Left")
        result = {'message': 'Pothole On Left'}
        training_image_list = os.listdir('ServerObstacleData')
        training_path_data = ["ServerObstacleData/{0}".format(x) for x in training_image_list]
        if len(training_image_list) == training_limit:
            oldest_file = min(training_path_data, key=os.path.getctime)
            os.remove(oldest_file)
            curr_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]
            img.save(f"{training_path}\Pothole_{curr_datetime}.jpg")
            return jsonify(result)
        else:
            curr_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]
            img.save(f"{training_path}\Pothole_{curr_datetime}.jpg")
            return jsonify(result)

    elif result1 == "Road" and result2 == "Pothole":
        print("Pothole On Right")
        result = {'message': 'Pothole On Right'}
        training_image_list = os.listdir('ServerObstacleData')
        training_path_data = ["ServerObstacleData/{0}".format(x) for x in training_image_list]
        if len(training_image_list) == training_limit:
            oldest_file = min(training_path_data, key=os.path.getctime)
            os.remove(oldest_file)
            curr_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]
            img.save(f"{training_path}\Pothole_{curr_datetime}.jpg")
            return jsonify(result)
        else:
            curr_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]
            img.save(f"{training_path}\Pothole_{curr_datetime}.jpg")
            return jsonify(result)
    else:
        print("Keep Going")
        result = {'message': 'Keep Going'}
        return jsonify(result)

    os.remove(f"{PATH}\{i}.jpg")
    os.remove(f"{PATH}\{i}_a.jpg")
    os.remove(f"{PATH}\{i}_b.jpg")
    i = i + 1

    #result = {'message': 'image processed successfully'}
    #return jsonify(result)


def load_image(img_path):
    img = keras.preprocessing.image.load_img(img_path, target_size=(150, 150))
    img_tensor = keras.preprocessing.image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.
    return img_tensor


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
