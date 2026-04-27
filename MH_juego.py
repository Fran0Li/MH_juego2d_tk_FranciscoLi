import tkinter as tk#importación de la librería tkinter y se nombra como tk
import pygame as py#importación de la librería pygame para el audio
import math#importación de la librería de mate para su uso posterior

#Constantes para la ventana
ANCHO_VP = 800 #ancho de la ventana principal
ALTO_VP = 600 #alto de la ventana prrincipal
GRAVEDAD = 0.8#valor de gravedad
POTENCIA_JUMP = -15 #potencia del salto, es negativo porque arriba es restar en Y
VELOCIDAD_MOV = 6 #velocidad de movimiento

#Game state

#info de hunter(jugador)
hunter = [100, 100, 0, False, None]
#i[0]: posición x
#i[1]: posición y
#i[2]: velocidad vertical (vy)
#i[3]: boolean sobre suelo 
#i[4]: identidad del dibuj en el Canvas (ID)

#interruptores de las teclas para un movimiento fluido 
teclas = {"Left": False, "Right": False, "Space": False}
#En orden respectivo de izquierda a derecha
#Estado de la flecha izquierda o a, estado de la flecha derecha o d, estado de la tecla espacio o W

#Funciones de movimiento, entradas
def izquier(event):
    teclas["Left"] = True #Activa interruptor para ir a la izquierda
def derecha(event):
    teclas["Right"] = True#Lo mismo que el de arriba pero para la derecha
def salto(event):
    teclas["Space"] = True#Lo mismo pero hacia arriba, el salto

def detener_key(event):#Funcion para detener el interruptor
    k = event.keysym #captura nombre de la tecla que el usuario dejó de presionar
    if k in ["Left", "a", "A"]: # si se deja de presionar
        teclas["Left"] = False # apaga el interruptor de izq
    elif k in ["Right", "d", "D"]:# si fue ir a la derecha 
        teclas["Right"] = False #apaga interruptor de derecha
    elif k in ["Space", "w", "W"]:# si fue salto, arriba
        teclas["Space"] = False # apaga interruptor de salto

#Lógica del mov!!

def mover_hunter():
    #Movimiento horizontal
    if  teclas["Left"]:#Si se presiona esta tecla
        hunter[0] -= VELOCIDAD_MOV# se mueve a la izq a la v de mov
    if teclas["Right"]:#Si se presiona esta teclas
        hunter[0] += VELOCIDAD_MOV# se mueve a la derecha a la v de mov
    
    #Lógica de salto
    if teclas["Space"] and hunter[3]:
        hunter[2] = POTENCIA_JUMP # Velocidad vertical hacia arriba
        hunter[3] = False #desactiva el estado de que está en el suelo

    #Aplicación de la Física!
    hunter[2] += GRAVEDAD # la gravedad jala hacia abajo sumando a la velocidad
    hunter[1] += hunter[2] # la posición Y cambia según la velocidad vertical que se acumule

    # Colisión con piso
    PISO_ALT = ALTO_VP - 20 #definición  de donde empieza el piso
    ALTO_HUNTER = 40 #Tamaño vertical del personaje

    # Si la parte baja de hunter pasa el límite del piso
    if hunter[1] + ALTO_HUNTER >= PISO_ALT:
        hunter[1] = PISO_ALT - ALTO_HUNTER # lo coloca encima del piso
        hunter[2] = 0 #devuelve la velocidad de caida a cero
        hunter[3] = True #marca que ahora está tocando el suelo

