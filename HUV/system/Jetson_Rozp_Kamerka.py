import cv2
import time


class Camera_Maszt():
    def __init__(self):
        self.dispW=640
        self.dispH=480
        self.flip=2
        self.flag = True
        self.show = False # Here change to False if in command line mode
        # Initialize the camera object
        try:
            self.gstreamer_str = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=120/1 ! nvvidconv flip-method='+str(self.flip)+' ! video/x-raw, width='+str(self.dispW)+', height='+str(self.dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
            self.cap = cv2.VideoCapture(self.gstreamer_str, cv2.CAP_GSTREAMER)
        except Exception as e:
            print(e)
    def Camera_Maszt_Akwizycja(self, Storage):
        """Run This Method in new Thread."""
        jest = 0
        start = time.time()
        frame_count = 0
        ### Petla Akwizycji obrazu i zapisu go w magazynie
        while True:
            
            ret, frame = self.cap.read() 
            Storage.setframe(frame)# Save Frame in Class Storage for other modules
            if self.show == True: # Show Image  on screen
                cv2.imshow("Widok z masztu", frame)
                jest == 1
            if self.show == False and jest == 1: # Close Window
                cv2.destroyAllWindows()
                jest == 0
            frame_count += 1
            if time.time() - start >= 1:
                print("{}fps kamera".format(frame_count))
                start = time.time()
                frame_count = 0
            # Wait Key added due to time allow for camera - 1, do not use 0 - it freez the screen

            if self.flag:  ### Close Procedure
                if self.show:
                    cv2.destroyAllWindows()
                    pass
                self.cap.release()
                print('Zatrzymano')
                break

# To sluzy do testow
if __name__ == "__main__":
    kamera = Camera_Maszt()
    magazyn = Magazyn()
    print(kamera.resolution)
    flag = False
    kamera.Camera_Maszt_Akwizycja(magazyn, lambda: flag)
