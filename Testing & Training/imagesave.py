import os
import datetime
from PIL import Image

PATH = os.path.join(os.getcwd(), '1.jpg')
print(PATH)
img = Image.open(PATH)

training_image_list = os.listdir('ObstacleData')
training_path = os.path.join(os.getcwd(), 'ObstacleData')
print(training_path)
training_path_data = ["ObstacleData/{0}".format(x) for x in training_image_list]
print(training_path_data)

if len(training_image_list) == 2:
    oldest_file = min(training_path_data, key=os.path.getctime)
    os.remove(oldest_file)
    curr_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]
    img.save(f"{training_path}\Pothole_{curr_datetime}.jpg")
    print(curr_datetime)
else:
    curr_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]
    img.save(f"{training_path}\Pothole_{curr_datetime}.jpg")