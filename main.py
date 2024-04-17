from Maszt import Maszt
import cv2

analiza = Maszt()
print(analiza)
while True:
    analiza.start()

    if cv2.waitKey(1) == ord('q'):
        print("Closing program without errors.")
        break

analiza.close()
