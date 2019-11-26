import vrep
import numpy as np
import time

ip = '127.0.0.1'
porta = 19999
clientID = 0

def insereCubos(clientID, posCubos):
    _, mesa = vrep.simxGetObjectHandle(clientID, "FrameMesa", vrep.simx_opmode_blocking)
    for i in range(3):
        _, cubo = vrep.simxGetObjectHandle(clientID, 'Cubo'+str(i+1), vrep.simx_opmode_blocking)        
        vrep.simxSetObjectPosition(clientID, cubo, mesa, posCubos[i], vrep.simx_opmode_blocking)
    return 0

def moveRobo(clientID, angulos):
    junta = []
    for i in range(6):
        _, j = vrep.simxGetObjectHandle(clientID, 'eixo'+str(i+1), vrep.simx_opmode_blocking)
        junta.append(j)
    
    vrep.simxPauseCommunication(clientID,True)
    for i in range(6):
        vrep.simxSetJointTargetPosition(clientID, junta[i], angulos[i]*np.pi/180, vrep.simx_opmode_oneshot)
    vrep.simxPauseCommunication(clientID,False)
    time.sleep(2)
    return 0

def abreGarra(clientID, num):
    _, mesa = vrep.simxGetObjectHandle(clientID, 'mesa', vrep.simx_opmode_blocking)
    _, cubo = vrep.simxGetObjectHandle(clientID, 'Cubo'+str(num), vrep.simx_opmode_blocking)
    vrep.simxSetObjectParent(clientID, cubo, mesa, True, vrep.simx_opmode_blocking)
    
    _, j1 = vrep.simxGetObjectHandle(clientID, 'junta_m1', vrep.simx_opmode_blocking)
    _, j2 = vrep.simxGetObjectHandle(clientID, 'junta_m2', vrep.simx_opmode_blocking)
    vrep.simxPauseCommunication(clientID,True)
    vrep.simxSetJointTargetPosition(clientID, j1, 0, vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetPosition(clientID, j2, 0, vrep.simx_opmode_oneshot)
    vrep.simxPauseCommunication(clientID,False)
    time.sleep(0.5)
    return 0
    
def fechaGarra(clientID, num):
    _, j1 = vrep.simxGetObjectHandle(clientID, 'junta_m1', vrep.simx_opmode_blocking)
    _, j2 = vrep.simxGetObjectHandle(clientID, 'junta_m2', vrep.simx_opmode_blocking)
    vrep.simxPauseCommunication(clientID,True)
    vrep.simxSetJointTargetPosition(clientID, j1, 0.028, vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetPosition(clientID, j2, 0.028, vrep.simx_opmode_oneshot)
    vrep.simxPauseCommunication(clientID,False)
    _, s = vrep.simxGetObjectHandle(clientID, 'fixaGarra', vrep.simx_opmode_blocking)
    _, cubo = vrep.simxGetObjectHandle(clientID, 'Cubo'+str(num), vrep.simx_opmode_blocking)
    time.sleep(1)
    vrep.simxSetObjectParent(clientID, cubo, s, True, vrep.simx_opmode_blocking)
    
def cinematicaInversa(Xc, Yc, Zc, ang):
 
    teta1 = np.arctan(Yc/Xc)*180/np.pi
    
    l1 = 448*0.001
    l2 = 150*0.001
    l3 = 590*0.001
    l4 = 130*0.001
    l5 = 647*0.001
    d = 238*0.001
    
    Z = Zc + d #Restrição do problema
    
    r = np.sqrt(Xc*Xc+Yc*Yc)
    h1 = Z - l1
    b1 = r - l2
    w = np.sqrt(h1*h1+b1*b1)
    lx = np.sqrt(l4*l4+l5*l5)
    alpha = np.arctan(l5/l4)*180/np.pi
    beta = np.arctan(h1/b1)*180/np.pi
    
    cosphi = (l3*l3+lx*lx-w*w)/(2*l3*lx)
    phi = np.arccos(cosphi)*180/np.pi
    senomega = lx*np.sin(np.radians(phi))/w
    omega = np.arcsin(senomega)*180/np.pi
    
    teta2 = 90-omega-beta
    teta3 = 180-alpha-phi
    
    teta5 = 90-teta3-teta2
    
    teta6 = ang-teta1
    
    angulos = (float(teta1), float(teta2), (float(teta3))-90, 0, float(teta5), float(teta6))
    
    return angulos

def conectaVrep(ipv, portav):
    vrep.simxFinish(-1)
    id = vrep.simxStart(ipv, portav, True, True, 5000, 5)
    if id!=-1:
        print ('Connected to remote API server')
    return id

def pegaCubo(x, y, z, ang):
    angu = cinematicaInversa(x, y, z+0.1, ang)
    moveRobo(clientID, angu)

def colocaCubo(cont):
    return

def converteCoordenadas(x1, y1):
    x = 1.175 - y1
    y = 0.175 - x1
    return x, y

    
clientID = conectaVrep(ip, porta)

#Posiciona Robô em Home
home = (0, 0, -90, 0, 0, 0)
moveRobo(clientID, home)
abreGarra(clientID, 1)

#Pilha  = 0.8, 0.1, 0.55, 0
#Gira   = 0.77464, 0, 0.55, 0

#Cubo 1 = 1.0250, -0.15, 0.55, 0    45
#Cubo 2 = 0.85, -0.125, 0.55, 0     30
#Cubo 3 = 1.025, 0.075, 0.55, 0     15


#(113, 164, 16.26), (381, 199, 42.14), (231, 335, 70.46)
#1 = 0.113, 0.164, 0.55, 16.26
#2 = 0.381, 0.199, 0.55, 42.14
#3 = 0.231, 0.335, 0.55, 70.46

#mesa = 1.175, 0.175, 0.5      X = 1.175 - yFm          y = 0.175 - xFm

#Pega o primeiro cubo

x, y = converteCoordenadas(0.113, 0.164)
pegaCubo(x, y, 0.55, 16)
anguloss = cinematicaInversa(x, y, 0.55, 16)
moveRobo(clientID, anguloss)
fechaGarra(clientID, 3)
pegaCubo(x, y, 0.55, 0)
pegaCubo(0.8, 0.1, 0.55, 0)
anguloss = cinematicaInversa(0.8, 0.1, 0.55, 0)
moveRobo(clientID, anguloss)
abreGarra(clientID, 3)
pegaCubo(0.8, 0.1, 0.55, 0)


#Pega o segundo cubo
x, y = converteCoordenadas(0.381, 0.199)
pegaCubo(x, y, 0.55, 42)
anguloss = cinematicaInversa(x, y, 0.55, 42)
moveRobo(clientID, anguloss)
fechaGarra(clientID, 1)
pegaCubo(x, y, 0.55, 0)
pegaCubo(0.8, 0.1, 0.60, 0)
anguloss = cinematicaInversa(0.8, 0.1, 0.60, 0)
moveRobo(clientID, anguloss)
abreGarra(clientID, 1)
pegaCubo(0.8, 0.1, 0.60, 0)


#Pega o terceiro cubo
x, y = converteCoordenadas(0.231, 0.335)
pegaCubo(x, y, 0.55, 70)
anguloss = cinematicaInversa(x, y, 0.55, 70)
moveRobo(clientID, anguloss)
fechaGarra(clientID, 2)
pegaCubo(x, y, 0.55, 0)
pegaCubo(0.8, 0.1, 0.65, 0)
anguloss = cinematicaInversa(0.8, 0.1, 0.65, 0)
moveRobo(clientID, anguloss)
abreGarra(clientID, 2)
pegaCubo(0.8, 0.1, 0.65, 0)
moveRobo(clientID, home)


vrep.simxFinish(clientID)