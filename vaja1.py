import cv2 
import numpy as np
import matplotlib.pyplot as plt

def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj):
    slika = slika[levo_zgoraj[1]:desno_spodaj[1], levo_zgoraj[0]:desno_spodaj[0]]

    spodnja_meja_koze = np.ndarray((1,3))
    zgornja_meja_koze = np.ndarray((1,3))

    for barvni_kanal_slike in range(3):
        podslika = slika[:,:,barvni_kanal_slike]
        vsota = 0
        for i in podslika:
            for j in i:
                vsota = vsota + j
        vsota = (vsota / len(podslika)) / len(podslika[0])

        std_odklon = 0
        for i in podslika:
            std_odklon = std_odklon + np.std(i, ddof=1)
        std_odklon = std_odklon / len(podslika)

        spodnja_meja_koze[0][barvni_kanal_slike] = int(vsota - std_odklon) # blue, green, red
        zgornja_meja_koze[0][barvni_kanal_slike] = int(vsota + std_odklon)

    return (spodnja_meja_koze,zgornja_meja_koze)

def zmanjsaj_sliko(slika):
    return cv2.resize(slika, (340, 220))

def obdelaj_sliko(slika, okno_sirina, okno_visina,barva_koze_spodaj, barva_koze_zgoraj):
    # print(barva_koze_spodaj)
    # print(barva_koze_zgoraj)
    x = prestej_piksle_z_barvo_koze(slika, barva_koze_spodaj, barva_koze_zgoraj) # TREBA SE IZBRATI PODSLIKO !!!!!!!!
    return (30, 40, int(slika.shape[1] * okno_sirina / 100), int(slika.shape[0] * okno_visina / 100))
    # print(x)

def prestej_piksle_z_barvo_koze(podslika, barva_koze_spodaj, barva_koze_zgoraj):
    return cv2.countNonZero(cv2.inRange(podslika, barva_koze_spodaj, barva_koze_zgoraj))

barva_dolocena = False

video = cv2.VideoCapture(0)

if video.isOpened() == False:
    print("Ne morem odpreti kamere")
    
cv2.namedWindow("Kamera")
while True:
    ret, slika = video.read()
    if ret == True:
        slika = cv2.flip(zmanjsaj_sliko(slika), 1)

        if cv2.waitKey(10) & 0xFF == ord('w'):
            cv2.destroyWindow("Kamera")
            k_v_slike = cv2.selectROI("Izberi barvo koze", slika) # dobimo koordinate in velikost
            cv2.destroyWindow("Izberi barvo koze")
            # x in y koordinata levo zgoraj, x + širina in y + višina desno spodaj 
            barva_koze = doloci_barvo_koze(slika, [k_v_slike[0], k_v_slike[1]], [k_v_slike[0] + k_v_slike[2], k_v_slike[1] + k_v_slike[3]]) 
            barva_dolocena = True

        if barva_dolocena:
            z = obdelaj_sliko(slika, 20, 20, barva_koze[0], barva_koze[1])
            image = cv2.rectangle(slika, (z[0], z[1]), (z[0] + z[2], z[1] + z[3]), (255, 0, 0), 2)
        cv2.imshow("Kamera",slika)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        


    else:
        break
video.release()
cv2.destroyAllWindows()
