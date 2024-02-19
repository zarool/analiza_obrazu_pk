import cv2

dispW=640
dispH=400
flip=2

gstreamer_str = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3840, height=2160, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

cap = cv2.VideoCapture(gstreamer_str, cv2.CAP_GSTREAMER)
count = 0
while True:    
    ret, frame = cap.read()    
    if ret:        
        cv2.imshow("Input via Gstreamer", frame)     
        if cv2.waitKey(1) == ord('l'):
            cv2.imwrite("fram3333e%d.jpg" % count, frame)
            print("Dupa", count)
            count += 1

        if cv2.waitKey(1) == ord('q'):  
            break
        


cap.release()
cv2.destroyAllWindows()
