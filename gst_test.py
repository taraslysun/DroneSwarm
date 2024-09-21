import cv2

cap = cv2.VideoCapture(0)

host_ip = "192.168.1.53"

gst_str = f"appsrc ! videoconvert ! video/x-raw,format=I420 ! jpegenc ! rtpjpegpay ! udpsink host={host_ip} port=5001"

# receive with following command
# gst-launch-1.0 udpsrc port=5000 ! application/x-rtp,encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! videoconvert ! autovideosink

out = cv2.VideoWriter(gst_str, 0, 30, (640, 480))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    out.write(frame)

    # cv2.imshow("frame", frame)
    # if cv2.waitKey(1) & 0xFF == ord("q"):
    #     break