import cv2 
import numpy as np
import matplotlib.pyplot as plt

def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj):
    # slika postane le izbrani kvadrat
    slika = slika[levo_zgoraj[1]:desno_spodaj[1], levo_zgoraj[0]:desno_spodaj[0]]

    spodnja_meja_koze = np.ndarray((1,3))
    zgornja_meja_koze = np.ndarray((1,3))

    # sliko razdeli na barvne kanale
    for barvni_kanal_slike_st in range(3):
        barvni_kanal_slike = slika[:,:,barvni_kanal_slike_st]

        # izracuna povprecje vsakega barvnega kanala
        povp = 0
        for i in barvni_kanal_slike:
            for j in i:
                povp = povp + j
        povp = (povp / len(barvni_kanal_slike)) / len(barvni_kanal_slike[0])

        # izracuna standardni odklon vsakega barvnega kanala
        std_odklon = 0
        for i in barvni_kanal_slike:
            std_odklon = std_odklon + np.std(i)
        std_odklon = std_odklon / len(barvni_kanal_slike)

        # nastavi min in max bgr vrednosti barve
        spodnja_meja_koze[0][barvni_kanal_slike_st] = int(povp - std_odklon)
        zgornja_meja_koze[0][barvni_kanal_slike_st] = int(povp + std_odklon)

    return (spodnja_meja_koze,zgornja_meja_koze)

def zmanjsaj_sliko(slika):
    # spremeni velikost slike
    return cv2.resize(slika, (340, 220))

def obdelaj_sliko(slika, okno_sirina_odstotek, okno_visina_odstotek, barva_koze_spodaj, barva_koze_zgoraj):
    # shrani sirino in visino slike in okna
    sirina = slika.shape[1]
    visina = slika.shape[0]
    okno_sirina = int(sirina * okno_sirina_odstotek / 100)
    okno_visina = int(visina * okno_visina_odstotek / 100)

    # premika okno cez celo sliko
    max = 0
    koordinataX = 0
    koordinataY = 0
    for i in range(0, sirina - okno_sirina, 5):
        for j in range(0, visina - okno_visina, 5):
            # poisce okno z najvec ujemajocimi piksli
            tmpSlika = slika[j:j + okno_visina, i:i + okno_sirina]
            tmp = prestej_piksle_z_barvo_koze(tmpSlika, barva_koze_spodaj, barva_koze_zgoraj)
            # shrani zacezni koordinati okna
            if tmp > max:
                max = tmp
                koordinataX = i
                koordinataY = j

    return (koordinataX, koordinataY, okno_sirina, okno_visina)

def prestej_piksle_z_barvo_koze(podslika, barva_koze_spodaj, barva_koze_zgoraj):
    # presteje st pikslov, ki so v dolocenem barvnem obmocju
    return cv2.countNonZero(cv2.inRange(podslika, barva_koze_spodaj, barva_koze_zgoraj))

barva_dolocena = False
# zacnemo z zajemanjem videa
video = cv2.VideoCapture(0)
if video.isOpened() == False:
    print("Ne morem odpreti kamere")
    
cv2.namedWindow("Kamera")
while True:
    ret, slika = video.read()
    if ret == True:
        # slika = cv2.flip(slika, 1)
        slika = cv2.flip(zmanjsaj_sliko(slika), 1)

        # zapremo aplikacijo
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        # nastavimo zeljeno barvo
        if cv2.waitKey(10) & 0xFF == ord('w'):
            cv2.destroyWindow("Kamera")
            # dobimo koordinate in velikost okna
            k_v_slike = cv2.selectROI("Izberi barvo koze", slika) 
            cv2.destroyWindow("Izberi barvo koze")
            # x in y koordinata levo zgoraj, x + širina in y + višina desno spodaj 
            barva_koze = doloci_barvo_koze(slika, [k_v_slike[0], k_v_slike[1]], [k_v_slike[0] + k_v_slike[2], k_v_slike[1] + k_v_slike[3]]) 
            barva_dolocena = True

        if barva_dolocena:
            # sledimo doloceni barvi (obrazu)
            tmp = obdelaj_sliko(slika, 20, 20, barva_koze[0], barva_koze[1])
            # levo zgoraj in desno spodaj koordinata, barva in sirina pravokotnika
            image = cv2.rectangle(slika, [tmp[0], tmp[1]], [tmp[0] + tmp[2], tmp[1] + tmp[3]], (255, 0, 0), 2)
        cv2.imshow("Kamera",slika)
    else:
        break

video.release()
cv2.destroyAllWindows()
