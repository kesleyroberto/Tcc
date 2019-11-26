import cv2
import urllib.request
import numpy as np

f1 = 5
f2 = 5
tamCubo = 800
Ku = 66*0.014
Kv = 82*0.0111

mtx = np.array([[676.58122219, 0, 308.98003766], [0, 675.28712062, 232.34446214], [0,0,1]])
dist = np.array([[0.07705304, 0.35945543, -0.00850226, -0.00701473, -1.84300351]])


def extraiMascara(img, minimo, maximo):

    h,  w = img.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

    # undistort
    img = cv2.undistort(img, mtx, dist, None, newcameramtx)
    
    cv2.imshow('Imagem Original', img)
    
    borrado = cv2.GaussianBlur(img, (f1, f2), 0)
    hsv = cv2.cvtColor(borrado, cv2.COLOR_BGR2HSV)
    kernel = np.ones((5, 5), np.uint8)
    mascara = cv2.inRange(hsv, minimo, maximo)
    mascara = cv2.erode(mascara, kernel)
    
    contours, _ = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cont = 0    
    posicao = []
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > tamCubo:
            ((x1,y1),(wi,he),angle) = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(((x1,y1),(wi,he),angle))
            box = np.int0(box)
            cv2.drawContours(img,[box],0,(0,0,255),2)
            
            cont = cont+1
            img = cv2.circle(img, (int(x1), int(y1)), 2, (0, 0, 255) , 2) 
            
            cv2.putText(img, 'u: '+str(int(x1))+' v: '+str(int(y1)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(img, 'angulo: '+str(np.abs(np.around(angle, 2))), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(img, 'x: '+str(int(x1*Ku))+' y: '+str(int(y1*Kv))+' mm', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
            
            
            posicao.append((int(x1*Ku), int(y1*Kv), np.abs(np.around(angle, 2))))        
    return cont, posicao

def temAzul(img):
    minimo = (79, 128, 70)
    maximo = (117, 255, 160)
    contaCor, pos  = extraiMascara(img, minimo, maximo)
    return contaCor, pos

def temAmarelo(img):
    minimo = (19, 79, 137)
    maximo = (52, 232, 200)
    contaCor, pos  = extraiMascara(img, minimo, maximo)
    return contaCor, pos

def temLaranja(img):
    minimo = (0, 165, 106)
    maximo = (14, 255, 200)
    contaCor, pos  = extraiMascara(img, minimo, maximo)
    return contaCor, pos

def temVerde(img):
    minimo = (47, 81, 51)
    maximo = (87, 200, 160)
    contaCor, pos  = extraiMascara(img, minimo, maximo)
    return contaCor, pos

def temMarrom(img):
    minimo = (0, 95, 0)
    maximo = (41, 183, 83)
    contaCor, pos  = extraiMascara(img, minimo, maximo)
    return contaCor, pos

def temRosa(img):
    minimo = (129, 97, 132)
    maximo = (180, 181, 227)
    contaCor, pos  = extraiMascara(img, minimo, maximo)
    return contaCor, pos
    
def retornaCubos(img):
    pos = []
    
    cAzul, pAzul = temAzul(img)
    cAmarelo, pAmarelo = temAmarelo(img)
    cLaranja, pLaranja = temLaranja(img)
    cVerde, pVerde = temVerde(img)
    cMarrom, pMarrom = temMarrom(img)
    cRosa, pRosa = temRosa(img)
    
    contTotal = cAzul + cAmarelo + cLaranja + cVerde + cMarrom + cRosa
    
    if (contTotal) > 3:
        print('ERRO NA CONTAGEM DOS CUBOS!!!!!')
        return -1
    
    if cAzul > 0:
        for i in range(cAzul):
            pos.append(pAzul[i])
    
    if cAmarelo > 0:
        for i in range(cAmarelo):
            pos.append(pAmarelo[i])
            
    if cLaranja > 0:
        for i in range(cLaranja):
            pos.append(pLaranja[i])
            
    if cVerde > 0:
        for i in range(cVerde):
            pos.append(pVerde[i])

    if cMarrom > 0:
        for i in range(cMarrom):
            pos.append(pMarrom[i])
            
    if cRosa > 0:
        for i in range(cRosa):
            pos.append(pRosa[i])
            
    return contTotal, pos
    


url = 'http://192.168.15.5:8080/shot.jpg'


#Cria duas janelas para exibicao
cv2.namedWindow("Imagem Original")

img = cv2.imread("D:/OneDrive/TCC/TCC2/OpenCV/fotos/cubos/CUBOS3.png")

print(retornaCubos(img))


#Loop de execucao
while(1):

    #Interrompe o programa ao se pressionar a tecla 'q'
    k = cv2.waitKey(1) & 0xFF
    if k == ord("q"):
        break
    
    #Obtém a imagem a partir da câmera do celular
    #imgApp = urllib.request.urlopen(url)
    #imgNp = np.array(bytearray(imgApp.read()), dtype=np.uint8)
    #img = cv2.imdecode(imgNp, -1)
    
    

    



#Caso saia do loop, fecha as janelas
cv2.destroyAllWindows()
