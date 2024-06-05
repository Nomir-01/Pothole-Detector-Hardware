import requests
import json
import os
import cv2

PATH = os.path.join(os.getcwd(), 'RoadData')
num_data=len(os.listdir(PATH))
i=1
def client_run(j):
    ret, frame = cam.read()
    if not ret:
        print("Failed to grab frame")
        exit()
    cv2.imshow("Pothole Detector", frame)
    img_name = f"{PATH}\{j}.jpg"
    cv2.imwrite(img_name, frame)
    img = cv2.imread(f"{PATH}\{j}.jpg")
    _, img_encoded = cv2.imencode('.jpg', img)

    response = requests.post('http://localhost:5000/process-image',
                             data=img_encoded.tostring(),
                             headers={'Content-Type': 'image/jpeg'})

    result = json.loads(response.content)
    print(result['message'])
    os.remove(f"{PATH}\{j}.jpg")
    j = j + 1
    run(j)

def run(j):
    client_run(j)
    k=cv2.waitKey(1)
    if k%256 == 27:
        exit()

cam=cv2.VideoCapture(0)
run(i)
