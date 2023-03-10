import cv2 
import numpy as np
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(0) #lahko tudi link do posnetka

if cap.isOpened() == False:
    print("Ne morem odpreti kamere")
    
cv2.namedWindow("Kamera")
while True:
    ret, frame = cap.read()
    if ret == True:
        frame = cv2.flip(frame,1) #flipnemo sliko al hocmo ogledal al kamero
        cv2.imshow("Kamera",frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()