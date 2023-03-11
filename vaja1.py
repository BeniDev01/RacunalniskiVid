import cv2 
import numpy as np
import matplotlib.pyplot as plt

def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj):
    print(str(levo_zgoraj[0]) + "\n" + str(levo_zgoraj[1]) + "\n" + str(desno_spodaj[0]) + "\n" + str(desno_spodaj[1]) + "\n")
    # return (spodnja_meja_koze,zgornja_meja_koze)

def zmanjsaj_sliko(slika):
    pass

def obdelaj_sliko(slika, okno_sirina, okno_visina,barva_koze_spodaj, barva_koze_zgoraj):
    pass

def prestej_piksle_z_barvo_koze(podslika, barva_koze_spodaj, barva_koze_zgoraj):
    pass


cap = cv2.VideoCapture(0)

if cap.isOpened() == False:
    print("Ne morem odpreti kamere")
    
cv2.namedWindow("Kamera")
while True:
    ret, frame = cap.read()
    if ret == True:
        frame = cv2.flip(frame,1)
        if cv2.waitKey(10) & 0xFF == ord('w'):
            cv2.destroyWindow("Kamera")
            r = cv2.selectROI("Izberi barvo koze", frame)
            cv2.destroyWindow("Izberi barvo koze")
            doloci_barvo_koze(frame, [r[0], r[1]], [r[0] + r[2], r[1] + r[3]]) # x in y koordinata levo zgoraj, x + širina in y + višina desno spodaj 
        cv2.imshow("Kamera",frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()