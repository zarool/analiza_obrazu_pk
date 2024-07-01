import jetson_inference
import jetson_utils
import cv2
from jetcam.csi_camera import CSICamera

net = jetson_inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

cam = CSICamera(width=600, height=400, framerate=30, flip=2)

while True:
    img = cam.read()

    imgCuda = jetson_utils.cudaFromNumpy(img)

    detections = net.Detect(imgCuda)

    img = jetson_utils.cudaToNumpy(imgCuda)

    cv2.imshow("Test", img)
    if cv2.waitKey(1) == ord('q'):
        print("Closing program without errors.")
        break

cam.cap.release()
cv2.destroyAllWindows()
