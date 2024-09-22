from flask import Flask, request
import json
import os
import cv2
import numpy as np
from model_training.YOLOvX import YOLOvX
import time

app = Flask(__name__)
model = YOLOvX('python_impl/model_training/yolov8n.onnx')

# Folder to save images
SAVE_FOLDER = 'received_images'
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)


# Function to generate sequential file names
def next_file_name():
    base_name = "image"
    extension = ".jpg"
    i = 1
    while True:
        file_name = f"{base_name}{i:04d}{extension}"
        if not os.path.exists(os.path.join(SAVE_FOLDER, file_name)):
            return file_name
        i += 1



@app.route('/', methods=['POST'])
def receive_image():
    if 'file' not in request.files:
        return "No file in request", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    if file:
        image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        file_name = next_file_name()
        detections = model.predict(image)
        img = model.draw_boxes(image, detections)
        cv2.imwrite(os.path.join(SAVE_FOLDER, file_name), img)
        return "File saved", 200

    return "Error in saving file", 500

if __name__ == '__main__':
    app.run(host='192.168.1.53', port=7000)