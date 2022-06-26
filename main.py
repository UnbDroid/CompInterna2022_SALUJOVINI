#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
#from ev3dev.ev3 import *
from ev3dev2.sound import Sound
from ev3dev2.console import *
import sys

def vira_verde(valor_esq,valor_dir,verde):
    #motores.on_for_seconds(SpeedPercent(-20), SpeedPercent(-20), 1.2)
    global verde_esq
    valor_esq = sensorEsq.value()
    valor_dir = sensorDir.value()

    if (valor_esq < verde_esq): #esq ve verde
        Sound().beep()
        print("Verde esquerdo", file=sys.stderr)
        motores.on_for_seconds(SpeedPercent(-50),SpeedPercent(-50),0.3)
        motores.on_for_seconds(SpeedPercent(-10),SpeedPercent(-50),0.8) #vira esquerda
        valor_esq = sensorEsq.value()
        segue_linha(preto)
    
    elif (valor_dir < verde): #dir ve verde
        Sound().beep()
        print("Verde esquerdo", file=sys.stderr)
        motores.on_for_seconds(SpeedPercent(-50),SpeedPercent(-50),0.4)
        motores.on_for_seconds(SpeedPercent(-50),SpeedPercent(-10),0.8) #vira direita
        valor_dir = sensorDir.value()
        segue_linha(preto)
        #motores.on_for_seconds(SpeedPercent(-50),SpeedPercent(30),1) #dobra pra direita

def ambient_light_intensity(self):
        """
        A measurement of the ambient light intensity, as a percentage.
        """
        self._ensure_mode(self.MODE_AMBIENT)
        return self.value(0) * self._scale('AMBIENT')


def segue_linha(preto):
    #verde = 10 #12
    branco = 160 #dentro da sala
    valor_frontal = sensorFrontal.value()

    if valor_frontal <= 200: #<= 100 no modo ambiente // no claro, o valor é 250
        #obstaculos(preto)
        pass
        '''valor_frontal = sensorFrontal.value()'''
        
    valor_esq = sensorEsq.value()
    valor_dir = sensorDir.value() 
    valor_meio = sensorMeio.value()

    branco_meio = 600
    vmenor = 10 #42 #esses valores deixam a curv mais aberta, se a distância entre os valores for alta. O que é bom na curva do quadrado
    vmaior = -35

#valores: 35,-75 // 42 e -30

    #bom valor de agressividade = 60 e -60 // 70 e -70
    sensorMeio_valores.append(valor_meio)
    sensorDir_valores.append(valor_dir)
    sensorEsq_valores.append(valor_esq)

    #print(sensorEsq_valores, file=sys.stderr)
    #print(sensorDir_valores, file=sys.stderr)
    print(sensorMeio_valores, file=sys.stderr)
    
    global verde_esq 

    if (valor_dir < verde) or (valor_esq < (verde_esq)): #um ou outro ve verde
        vira_verde(valor_esq,valor_dir,verde)
    
    elif (valor_meio < branco_meio): #sensor do meio vendo preto
        kp = 0.1
        objetivo = 450
        if valor_dir > preto and valor_esq > preto: #somente o do meio vendo preto
            motores.on(SpeedPercent(((-kp*(objetivo-valor_meio)))-20),SpeedPercent(((kp*(objetivo-valor_meio)))-20))
        
        elif valor_esq < preto and valor_dir > preto: # esquerda e meio vendo preto 
            motores.on(SpeedPercent(vmenor),SpeedPercent(vmaior))
            while (valor_dir > preto): #enquanto o direito não ver preto
                valor_dir = sensorDir.value()

        elif valor_esq > preto and valor_dir < preto: # direita e meio vendo preto
            #Sound().beep()
            motores.on(SpeedPercent(vmaior),SpeedPercent(vmenor))
            while (valor_esq > preto): #enquanto o esquerdo não ver preto
                valor_esq = sensorDir.value()
        
        else: #encruzilhada / todos vendo preto
            motores.on_for_seconds(SpeedPercent(-15),(-15), 1.5)
    
    else: #sensor do meio vendo branco
        if (valor_esq < preto) and (valor_dir > preto): #esquerdo ve preto e direito ve branco
            motores.on(SpeedPercent(vmenor),SpeedPercent(vmaior))
            while (valor_meio > branco_meio): #enquanto o do meio não ver preto
                valor_meio = sensorMeio.value()

        elif (valor_esq > preto) and (valor_dir < preto): #esquerdo ve branco e direito ve preto
            motores.on(SpeedPercent(vmaior),SpeedPercent(vmenor))
            while (valor_meio > branco_meio):  #enquanto o do meio não ver preto
                valor_meio = sensorMeio.value()

        else: #todos veem branco
            motores.on(SpeedPercent(-20),SpeedPercent(-20))
        

        '''else: #Sensor do meio vendo preto
        if (valor_esq < (preto - 5)) and (valor_dir < (preto + 5)): #todos veem valor menor que preto
            motores.on_for_seconds(SpeedPercent(0), SpeedPercent(0),1)
            motores.on_for_seconds(SpeedPercent(-20),SpeedPercent(-20),1)

        elif (valor_esq < preto) and (valor_dir > preto): #esquerdo ve valor menor que preto -> dobra pra esquerda 
            motores.on(SpeedPercent(vmenor),SpeedPercent(vmaior)) 
            
        elif (valor_esq > preto) and (valor_dir < preto): #só direito ve valor menor que preto -> dobra pra direita
            motores.on(SpeedPercent(vmaior),SpeedPercent(vmenor))     

        else: #ambos veem valores maiores que preto (dois brancos)
            motores.on(SpeedPercent(-25),SpeedPercent(-25))'''

def obstaculos(preto):    
    valor_esq = sensorEsq.value()
    valor_dir = sensorDir.value()
    
    perto = 150

    motores.on_for_seconds(SpeedPercent(20),SpeedPercent(20), 1) # ré
    motores.on_for_seconds(SpeedPercent(30),SpeedPercent(-50),1.22) #dobra pra esquerda

    valor_ultrassom = ultrassom.value()
    
    if valor_ultrassom < perto:
        while valor_ultrassom < perto:
            motores.on(SpeedPercent(-50),SpeedPercent(-50))
            valor_ultrassom = ultrassom.value()
            Sound().beep()
    else:
        while valor_ultrassom >= perto:
            motores.on(SpeedPercent(-50),SpeedPercent(-50))
            valor_ultrassom = ultrassom.value()
            #print(valor_ultrassom, file=sys.stderr)

        while valor_ultrassom < perto:
            motores.on(SpeedPercent(-50),SpeedPercent(-50))
            valor_ultrassom = ultrassom.value()
            #print(valor_ultrassom, file=sys.stderr)

    motores.on_for_seconds(SpeedPercent(-50),SpeedPercent(10),1.6 ) #dobra pra direita

    valor_ultrassom = ultrassom.value()

    if valor_ultrassom < 100:
        while valor_ultrassom < 100:
            motores.on(SpeedPercent(-50),SpeedPercent(-50))
            valor_ultrassom = ultrassom.value()
            Sound().beep()
    else:
        while valor_ultrassom >= 100:
            motores.on(SpeedPercent(-50),SpeedPercent(-50))
            valor_ultrassom = ultrassom.value()
            #print(valor_ultrassom, file=sys.stderr)
        while valor_ultrassom < 100:
            motores.on(SpeedPercent(-50),SpeedPercent(-50))
            valor_ultrassom = ultrassom.value()
            #print(valor_ultrassom, file=sys.stderr)
    motores.on_for_seconds(SpeedPercent(-50),SpeedPercent(30),1.2) #dobra pra direita
    
    while valor_esq > preto and valor_dir > preto:
        motores.on(SpeedPercent(-20),SpeedPercent(-20)) #vai reto
        valor_esq = sensorEsq.value()
        valor_dir = sensorDir.value()

    motores.on_for_seconds(SpeedPercent(30),SpeedPercent(-50),1.2) #dobra pra esquerda'''
    
    valor_ultrassom = ultrassom.value()
    #print(valor_ultrassom)

    valor_frontal = sensorFrontal.value()
    segue_linha(preto)
    

def calibrate_white(self):
    (self.red_max, self.green_max, self.blue_max) = self.raw


def calibra_sensores():
    print('Comeco')
    time.sleep(10)
    #ambient_light_intensity(sensorFrontal)
    calibrate_white(sensorEsq)
    calibrate_white(sensorDir)
    
    
def abaixa_garra():
    garra.on_for_seconds(SpeedPercent(-15), 0.4)
    garra.on_for_seconds(SpeedPercent(-9), 0.7)
    garra.on_for_seconds(SpeedPercent(-10), 1) #0.8 // qunato tempo demora para abrir a garra
    time.sleep(2)

def levanta_garra():
    garra.on_for_seconds(SpeedPercent(15),1.2) #1.4
    #garra.on_for_seconds(SpeedPercent(9), 0.7)
    time.sleep(2)

def funcao_estoque():
    estoque.on_for_seconds(SpeedPercent(-10), 0.55) #sobe
    time.sleep(5)
    estoque.on_for_seconds(SpeedPercent(20), 0.35) #desce
    time.sleep(10)

def funcao_garra():
    abaixa_garra()
    motores.on_for_seconds(SpeedPercent(-40), SpeedPercent(-40),2)
    levanta_garra()

def leitor_cor():
    print("SensorEsquerdo = ", sensorEsq.value()) #valores esq: branco (59) // preto (10) // verde (4 - 9)
    print("SensorDireito = ", sensorDir.value()) # valores dir: branco (70) // preto (7) // verde (4) // verde é menor que 6

def valores_sCor(sensorEsq,sensorDir):
    i = 0
    
    while i < 5:
        motores.on(SpeedPercent(-50),SpeedPercent(-50))
        sensorDir_valores.append(sensorDir.value())
        sensorEsq_valores.append(sensorEsq.value())
        i += 1

    print(sensorDir_valores, file=sys.stderr)
    print(sensorEsq_valores, file=sys.stderr)

def inicio():
    #calibra_sensores()
    while True:   
        valor_frontal = sensorFrontal.value()     
        sensorFrontal_valores.append(valor_frontal)

        segue_linha(preto)
        #motores.follow_line(kp = 0.6 , ki =1 , kd =1 , speed=SpeedPercent(30), 500, True, 600)
        
        
motores = MoveTank(OUTPUT_A,OUTPUT_B)
garra = Motor(OUTPUT_C)
estoque = Motor(OUTPUT_D)

sensorEsq = ColorSensor(INPUT_3)
sensorDir = ColorSensor(INPUT_1)
sensorMeio = LightSensor(INPUT_4)
sensorFrontal = LightSensor(INPUT_2)
#sensorFrontal = Sensor(INPUT_2)
sensorEsq_valores = []
sensorDir_valores = []
sensorMeio_valores = []
sensorFrontal_valores = []
verde = 13
verde_esq = verde + 6 + 2

def feira_livro():
    while True:
        print(sensorFrontal.value(), file=sys.stderr)
        if sensorFrontal.value() < 20:
            funcao_garra()

preto = 45

inicio()

#le 45 por segundo no branco

#quadrado -> dominancia de sensor (Esq,Dir,Esq)
#Triangulo -> dominancia de sensor (Esq)
