import cv2
import urllib.request
import numpy as np

f1 = 5
f2 = 5
tamCubo = 800
minV = 0
maxV = 0
mtx = np.array([[676.58122219, 0, 308.98003766], [0, 675.28712062, 232.34446214], [0,0,1]])
dist = np.array([[0.07705304, 0.35945543, -0.00850226, -0.00701473, -1.84300351]])

    
def extraiMascara(img, minimo, maximo):

    
    
    borrado = cv2.GaussianBlur(img, (f1, f2), 0)
    
    hsv = cv2.cvtColor(borrado, cv2.COLOR_BGR2HSV)
    kernel = np.ones((5, 5), np.uint8)
    mascara = cv2.inRange(hsv, minimo, maximo)
    mascara = cv2.erode(mascara, kernel)

    #cv2.imshow('Mascara', mascara)
    
    contours, _ = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cont = 0
    pos = 0
    
    posicao = []
    
    minV = cv2.getTrackbarPos('x','Trackbars')
    maxV = cv2.getTrackbarPos('y','Trackbars')
    
    #cv2.imshow('Distorc', borrado)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > tamCubo:
            ((x1,y1),(wi,he),angle) = cv2.minAreaRect(cnt)
            #pos[cont+1] = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(((x1,y1),(wi,he),angle))
            box = np.int0(box)
            cv2.drawContours(img,[box],0,(0,0,255),2)
            cont = cont+1   
            
            posicao.append((int(x1), int(y1), np.around(angle, 2)))
            
            cv2.putText(img, 'u: '+str(int(x1))+' v: '+str(int(y1)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(img, 'angulo: '+str(np.abs(np.around(angle, 2))), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(img, 'x: '+str(int(x1*minV*0.014))+' y: '+str(int(y1*maxV*0.0111))+' mm', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
            
            cv2.circle(img, (int(x1), int(y1)), 2, (255, 0, 0), 3)
            
            print(int(x1), int(y1), angle)           
    return cont, posicao

def temAzul(img):
    minimo = (79, 72, 70)
    maximo = (117, 200, 160)
    contaCor, pos  = extraiMascara(img, minimo, maximo)
    if contaCor != 0:
        print(contaCor)
        return 1
    return 0

def temAmarelo(img):
    minimo = (19, 79, 137)
    maximo = (52, 232, 200)
    contaCor, pos  = extraiMascara(img, minimo, maximo)
    if contaCor != 0:
        print(contaCor)
        return 1
    return 0

def temLaranja(img):
    minimo = (0, 165, 106)
    maximo = (14, 255, 200)
    contaCor, pos  = extraiMascara(img, minimo, maximo)
    if contaCor != 0:
        print(contaCor)
        print(pos)
        return 1
    return 0

def temVerde(img):
    minimo = (47, 81, 51)
    maximo = (87, 200, 160)
    contaCor, pos  = extraiMascara(img, minimo, maximo)
    if contaCor != 0:
        print(contaCor)
        return 1
    return 0

def temMarrom(img):
    minimo = (0, 95, 0)
    maximo = (41, 183, 83)
    contaCor, pos  = extraiMascara(img, minimo, maximo)
    if contaCor != 0:
        print(contaCor)
        return 1
    return 0

def temRosa(img):
    minimo = (129, 97, 132)
    maximo = (180, 181, 227)
    contaCor, pos  = extraiMascara(img, minimo, maximo)
    if contaCor != 0:
        print(contaCor)
        return 1
    return 0

def passa(x):
    pass
     

url = 'http://192.168.15.5:8080/shot.jpg'


#Cria duas janelas para exibicao
cv2.namedWindow("Imagem Original")
cv2.namedWindow("Mascara")

cv2.namedWindow("Trackbars")
cv2.createTrackbar('x', 'Trackbars', 0, 100, passa)
cv2.createTrackbar('y', 'Trackbars', 0, 100, passa)

#img = cv2.imread("D:/OneDrive/TCC/TCC2/OpenCV/fotos/cubos/CUBOS3.png")

#Loop de execucao

#temLaranja(img)

while(1):

    #Interrompe o programa ao se pressionar a tecla 'q'
    k = cv2.waitKey(1) & 0xFF
    if k == ord("q"):
        break
        
    
    
    #Obtém a imagem a partir da câmera do celular
    imgApp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgApp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNp, -1)
    
    h,  w = img.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

    # undistort
    img = cv2.undistort(img, mtx, dist, None, newcameramtx)
    
    #temAzul(img) #corrigir
    #temAmarelo(img)
    #temVerde(img)
    #temMarrom(img) #corrigir
    
    temLaranja(img)
    
    #print(a)
    
    #Exibe a figura ajustada
    #cv2.imshow('Contornado',hsv)
    cv2.imshow('Imagem Original', img)

#Caso saia do loop, fecha as janelas
cv2.destroyAllWindows()
