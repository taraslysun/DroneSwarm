# Ultralytics YOLO 🚀, AGPL-3.0 license

import argparse
import cv2
import numpy as np
import time

CLASSES = ['tree']
colors = [(0, 0, 255)]

class YOLOvX:
    def __init__(self, model_path, img_size=640):
        self.model = cv2.dnn.readNetFromONNX(model_path)
        self.img_size = img_size


    def predict(self, image):
        height, width, _ = image.shape
        length = max((height, width))
        result_img = np.zeros((length, length, 3), np.uint8)
        result_img[0:height, 0:width] = image
        scale = length / self.img_size

        blob = cv2.dnn.blobFromImage(result_img, scalefactor=1 / 255, size=(self.img_size, self.img_size), swapRB=True)
        self.model.setInput(blob)

        outputs = self.model.forward()

        outputs = np.array([cv2.transpose(outputs[0])])
        rows = outputs.shape[1]

        boxes = []
        scores = []
        class_ids = []
        maxClassIndex = 0
        for i in range(rows):
            # classes_scores = outputs[0][i][4:]
            # (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(classes_scores)
            maxScore = outputs[0][i][4]
            
            if maxScore >= 0.25:
                box = [
                    outputs[0][i][0] - (0.5 * outputs[0][i][2]),
                    outputs[0][i][1] - (0.5 * outputs[0][i][3]),
                    outputs[0][i][2],
                    outputs[0][i][3],
                ]
                boxes.append(box)
                scores.append(maxScore)
                class_ids.append(maxClassIndex)

        # Apply NMS (Non-maximum suppression)
        result_boxes = cv2.dnn.NMSBoxes(boxes, scores, 0.25, 0.45, 0.5)

        detections = []

        for i in range(len(result_boxes)):
            index = result_boxes[i]
            box = boxes[index]
            detection = {
                "class_id": class_ids[index],
                "class_name": CLASSES[class_ids[index]],
                "confidence": scores[index],
                "box": box,
                "scale": scale,
            }
            detections.append(detection)
            # label = f"{CLASSES[class_ids[index]]} ({scores[index]:.2f})"
            # color = colors[class_ids[index]]
            # cv2.rectangle(image, 
            #             (round(box[0] * scale), round(box[1] * scale)), 
            #             (round((box[0] + box[2]) * scale), round((box[1] + box[3]) * scale)), 
            #             color, 
            #             2)
            # cv2.putText(image, 
            #             label,
            #             (round(box[0] * scale) - 10, round(box[1] * scale) - 10), 
            #             cv2.FONT_HERSHEY_SIMPLEX, 
            #             0.5, color, 2)
        # return image, detections
        return detections
    
    def draw_boxes(self, image, detections):
        for detection in detections:
            box = detection["box"]
            scale = detection["scale"]
            label = f"{detection['class_name']} ({detection['confidence']:.2f})"
            color = colors[detection["class_id"]]
            cv2.rectangle(image, 
                        (round(box[0] * scale), round(box[1] * scale)), 
                        (round((box[0] + box[2]) * scale), round((box[1] + box[3]) * scale)), 
                        color, 
                        2)
            cv2.putText(image, 
                        label,
                        (round(box[0] * scale) - 10, round(box[1] * scale) - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.5, color, 2)
        return image

    def cap_and_process(self, input_src, gst_str, sleep_time=0.2):
        if not input_src:
            cap = cv2.VideoCapture(0)
        else:
            cap = cv2.VideoCapture(input_src, cv2.CAP_GSTREAMER)
        out = cv2.VideoWriter(gst_str, 0, 30, (640, 480))
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            img = self.predict(frame)
            time.sleep(sleep_time)
            out.write(img)
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="yolov8n.onnx", help="Input your ONNX model.")
    parser.add_argument("--img", default="bus.jpg", help="Path to input image.")
    parser.add_argument("--img_size", default=640, type=int, help="Image size for inference.")
    args = parser.parse_args()
    # img = apply_model(args.model, args.img, args.img_size)
    model = YOLOvX(args.model, args.img_size)
    host_ip = "192.168.1.55"
    port = "12345"

    gst_str = f"appsrc ! videoconvert ! video/x-raw,format=I420 ! jpegenc ! rtpjpegpay ! udpsink host={host_ip} port={port}"
    img = cv2.imread(args.img)
    print(img.shape)
    detections = model.predict(img)
    result = model.draw_boxes(img, detections)
    for detection in detections:
        print(detection)
    cv2.imwrite("result.jpg", result)

    # model.cap_and_process(0, gst_str, sleep_time=0.2)
