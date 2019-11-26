import cv2
import urllib.request
import numpy as np

f1 = 5
f2 = 5
tamCubo = 200

url = 'http://192.168.15.5:8080/shot.jpg'

def passa(x):
    pass
    
#Cria duas janelas para exibicao
cv2.namedWindow("Imagem Original")
cv2.namedWindow("Mascara")

#Loop de execucao
while(1):

    #Interrompe o programa ao se pressionar a tecla 'q'
    k = cv2.waitKey(1) & 0xFF
    if k == ord("q"):
        break
    
    #Obtém a imagem a partir da câmera do celular
    imgApp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgApp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNp, -1)    
    
    
    borrado = cv2.GaussianBlur(img, (f1, f2), 0)
    
    image = cv2.cvtColor(borrado, cv2.COLOR_BGR2GRAY)
    
    _ , th1 = cv2.threshold(image,65,255,cv2.THRESH_BINARY_INV)
    
    #cvuint8 = cv2.convertScaleAbs(image)
    
    contours, _ = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cont = 0
    pos = 0
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > tamCubo:
            ((x, y), radius) = cv2.minEnclosingCircle(cnt)
            center = (int(x), int(y))
            cv2.circle(img, center, int(radius), (0, 255, 255), 2)
            
            print(int(x), int(y), int(radius))
    
    
    #ret,thresh1 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)

    #kernel = np.ones((5, 5), np.uint8)
    #mascara = cv2.inRange(hsv, minimo, maximo)
    
    #mascara = cv2.erode(mascara, kernel)
    
    
    cv2.imshow('Mascara', th1)
             
    #Exibe a figura ajustada
    #cv2.imshow('Contornado',hsv)
    cv2.imshow('Imagem Original', img)
    
    

#Caso saia do loop, fecha as janelas
cv2.destroyAllWindows()
