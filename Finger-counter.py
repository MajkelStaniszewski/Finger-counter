import cv2
import numpy as np
import math

# Pobranie obrazu z kamerki internetowej
obraz = cv2.VideoCapture(0)

while (obraz.isOpened()):
    ret, frame = obraz.read()
    frame = cv2.flip(frame, 1)

# Domyślna wartość potrzebna do zliczcania palców
    ilosc = 0

# Z ramki badamy dłoń
    cv2.rectangle(frame, (100, 100), (300, 300), (0, 255, 5), 0) #cv2.rectangle(image, start_point, end_point, color, thickness)
    crop_image = frame[100:300, 100:300]

# Progowanie obrazu
    blur = cv2.GaussianBlur(crop_image, (5, 5), 0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((5, 5)) #5x5 matrix of ones (kernel for blurring)
    dilation = cv2.dilate(gray, kernel, iterations=1)
    erosion = cv2.erode(dilation, kernel, iterations=1)
    filtered = cv2.GaussianBlur(erosion, (3, 3), 0)
    ret, thresh = cv2.threshold(filtered, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)   #retval,thresholded image
# Wyświetlanie
    cv2.imshow("Sprogowane -Threshold image", thresh)
# Znajdowanie konturów
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# Wybiera kontur o największym polu, a arugmentem po którym wartość jest oceniania jest funkcja linowa
    contour = max(contours, key=lambda x: cv2.contourArea(x))
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(crop_image, (x, y), (x + w, y + h), (0, 0, 255), 0)

    hull = cv2.convexHull(contour)

    drawing = np.zeros(crop_image.shape, np.uint8)
    cv2.drawContours(drawing, [contour], -1, (0, 255, 0), 0)
    cv2.drawContours(drawing, [hull], -1, (0, 0, 255), 0)

    hull = cv2.convexHull(contour, returnPoints=False)
    defects = cv2.convexityDefects(contour, hull)

# Twierdzenie cosinusów
    for i in range(defects.shape[0]):
        p, l, m, n = defects[i, 0]

        far = tuple(contour[m][0])
        end = tuple(contour[l][0])
        start = tuple(contour[p][0])
# Znajdywanie długości wszystkich boków
        c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
        b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
        a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
# Kąt z tw.cosinusów
        kat = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14
#Sprawdzenie kąta pomiędzy palcami
        if kat <= 90:
            ilosc += 1
            cv2.circle(crop_image, far, 1, [0, 0, 255], -1)

        cv2.line(crop_image, start, end, [0, 255, 0], 2)

# Detekcja na postawie kątów ilości palców
    if ilosc == 0:
        cv2.putText(frame, "1 palec", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
    elif ilosc == 1:
        cv2.putText(frame, "2 palce", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
    elif ilosc == 2:
        cv2.putText(frame, "3 palce", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
    elif ilosc == 3:
        cv2.putText(frame, "4 palce", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
    elif ilosc == 4:
        cv2.putText(frame, "5 palcow", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
    else: pass
# Wyświetlanie
    cv2.imshow('łapsko', frame)
    if cv2.waitKey(1) == ord('q'):
        break

obraz.release()
cv2.destroyAllWindows()