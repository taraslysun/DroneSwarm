from flask import Flask, request
from model_training.YOLOvX import YOLOvX
import cv2
import numpy as np
import json

app = Flask(__name__)
model = YOLOvX('model_training/yolov8n.onnx')


@app.route('/', methods=['POST'])
def ImageHandler():
    image = request.files['image']
    img = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)
    detections = model.predict(img)
    img = model.draw_boxes(img, detections)
    print("Image processed")
    return "File processed", 200


if __name__ == "__main__":
    app.run(host='192.168.1.53', port=7000)