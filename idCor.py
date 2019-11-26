import cv2
import imutils
import urllib.request
import numpy as np

f1 = 5
f2 = 5
tamCubo = 400

def passa(x):
    pass
    
def extraiMascara(img, minimo, maximo):
    borrado = cv2.GaussianBlur(img, (11, 11), 0)
    hsv = cv2.cvtColor(borrado, cv2.COLOR_BGR2HSV)
    kernel = np.ones((f1, f2), np.uint8)
    mascara = cv2.inRange(hsv, minimo, maximo)
    mascara = cv2.erode(mascara, kernel)
    cv2.imshow('Mascara', mascara)
    contours, _ = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cont = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > tamCubo:
            ((x1,y1),(x2,y2),angle) = cv2.minAreaRect(cnt)
            
            box = cv2.boxPoints(((x1,y1),(x2,y2),angle))
            box = np.int0(box)
            cv2.drawContours(img,[box],0,(0,0,255),2)
            
            print(int(x1+x2/2), int(y1+y2)/2, angle)
            #arc_len = cv2.arcLength(cnt, True)
            #approx = cv2.approxPolyDP(cnt, 0.1*arc_len, True)
            #if (len( approx ) == 4):
                
                #cv2.drawContours(hsv, [approx], -1, ( 255, 0, 0 ), 2 )
                #cont = cont+1
    return cont

def temVerde(img):
    minimo = (57, 95, 70)
    maximo = (130, 255, 154)
    contaCor = extraiMascara(img, minimo, maximo)
    
def temAmarelo(img):
    minimo = (0, 137, 95)
    maximo = (58, 255, 255)
    contaCor = extraiMascara(img, minimo, maximo)

def temLaranja(img):
    minimo = (0, 216, 135)
    maximo = (24, 255, 190)
    contaCor = extraiMascara(img, minimo, maximo)

def temRoxo(img):
    minimo = (122, 58, 28)
    maximo = (180, 183, 144)
    contaCor = extraiMascara(img, minimo, maximo)

def temAzul(img):
    minimo = (78, 35, 70)
    maximo = (129, 113, 188)
    contaCor = extraiMascara(img, minimo, maximo)

def temRosa(img):
    minimo = (130, 91, 121)
    maximo = (170, 188, 237)
    contaCor = extraiMascara(img, minimo, maximo)
    

url = 'http://192.168.15.5:8080/shot.jpg'


#Cria duas janelas para exibicao
cv2.namedWindow("Imagem Original")
cv2.namedWindow("Mascara")

#img = cv2.imread("D:\OneDrive\TCC\TCC2\OpenCV\fotos\cubos3.png")

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
    
    #Aplica a filtragem e conversão inicial
    
    temVerde(img)

    #Exibe a figura ajustada
    #cv2.imshow('Contornado',hsv)
    cv2.imshow('Imagem Original', img)

#Caso saia do loop, fecha as janelas
cv2.destroyAllWindows()
