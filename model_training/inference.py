# Ultralytics YOLO 🚀, AGPL-3.0 license

import argparse
import cv2
import numpy as np

CLASSES = ['tree']
colors = [(0, 123, 255)]


def main(onnx_model, input_image, img_size):
    model = cv2.dnn.readNetFromONNX(onnx_model)

    original_image = cv2.imread(input_image)
    height, width, _ = original_image.shape
    length = max((height, width))
    image = np.zeros((length, length, 3), np.uint8)
    image[0:height, 0:width] = original_image
    scale = length / img_size

    blob = cv2.dnn.blobFromImage(image, scalefactor=1 / 255, size=(img_size, img_size), swapRB=True)
    model.setInput(blob)

    outputs = model.forward()
    print(outputs.shape)

    # Prepare output array
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

    # Iterate through NMS results to draw bounding boxes and labels
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
        label = f"{CLASSES[class_ids[index]]} ({scores[index]:.2f})"
        color = colors[class_ids[index]]
        cv2.rectangle(original_image, 
                      (round(box[0] * scale), round(box[1] * scale)), 
                      (round((box[0] + box[2]) * scale), round((box[1] + box[3]) * scale)), 
                       color, 
                       2)
        cv2.putText(original_image, 
                    label, 
                    (round(box[0] * scale) - 10, round(box[1] * scale) - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, 
                    color, 
                    2)

    # Display the image with bounding boxes
    # cv2.imshow("image", original_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imwrite("output.jpg", original_image)

    return detections


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="yolov8n.onnx", help="Input your ONNX model.")
    parser.add_argument("--img", default="bus.jpg", help="Path to input image.")
    parser.add_argument("--img", default="bus.jpg", help="Path to input image.")
    parser.add_argument("--img_size", default=640, type=int, help="Image size for inference.")
    args = parser.parse_args()
    main(args.model, args.img, args.img_size)