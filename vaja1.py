import cv2 
import numpy as np
import matplotlib.pyplot as plt

def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj):
    print(str(levo_zgoraj[0]) + "\n" + str(levo_zgoraj[1]) + "\n" + str(desno_spodaj[0]) + "\n" + str(desno_spodaj[1]) + "\n")

    spodnja_meja_koze = np.ndarray((1,3))
    zgornja_meja_koze = np.ndarray((1,3))

    for c in range(3):
        tmp = slika[:,:,c]
        vsota = 0
        for i in tmp:
            for j in i:
                vsota = vsota + j
        vsota = (vsota / len(tmp)) / len(tmp[0])
        # print(vsota)

        std_odklon = 0
        for i in tmp:
            std_odklon = std_odklon + np.std(i, ddof=1)
        std_odklon = std_odklon / len(tmp)
        # print(std_odklon)

        spodnja_meja_koze[0][c] = int(vsota - std_odklon) # blue, green, red
        zgornja_meja_koze[0][c] = int(vsota + std_odklon)

    return (spodnja_meja_koze,zgornja_meja_koze)

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

            izbrano_obmocje = frame[r[1]:r[1]+r[3], r[0]:r[0]+r[2]]

            # x in y koordinata levo zgoraj, x + širina in y + višina desno spodaj 
            barva_koze = doloci_barvo_koze(izbrano_obmocje, [r[0], r[1]], [r[0] + r[2], r[1] + r[3]]) 

            print(barva_koze[0])
            print(barva_koze[1])

        cv2.imshow("Kamera",frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()