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
teclas = {"Left": False, "Right": False, "space": False}
#En orden respectivo de izquierda a derecha
#Estado de la flecha izquierda o a, estado de la flecha derecha o d, estado de la tecla espacio o W

#Funciones de movimiento, entradas
def izquier(event):
    teclas["Left"] = True #Activa interruptor para ir a la izquierda
def derecha(event):
    teclas["Right"] = True#Lo mismo que el de arriba pero para la derecha
def salto(event):
    teclas["space"] = True#Lo mismo pero hacia arriba, el salto

def detener_key(event):#Funcion para detener el interruptor
    k = event.keysym #captura nombre de la tecla que el usuario dejó de presionar
    if k in ["Left", "a", "A"]: # si se deja de presionar
        teclas["Left"] = False # apaga el interruptor de izq
    elif k in ["Right", "d", "D"]:# si fue ir a la derecha 
        teclas["Right"] = False #apaga interruptor de derecha
    elif k in ["space", "w", "W"]:# si fue salto, arriba
        teclas["space"] = False # apaga interruptor de salto

#Lógica del mov!!

def mover_hunter():
    #Movimiento horizontal
    if  teclas["Left"]:#Si se presiona esta tecla
        hunter[0] -= VELOCIDAD_MOV# se mueve a la izq a la v de mov
    if teclas["Right"]:#Si se presiona esta teclas
        hunter[0] += VELOCIDAD_MOV# se mueve a la derecha a la v de mov
    
    #Lógica de salto
    if teclas["space"] and hunter[3]:
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

#Animacion en ventana

def animove():
    mover_hunter() # Ejecuta la lógica de movimiento y salto

    #Actualiza el dibujo del personaje usando las coordenadas de  la lista de hunter
    #canva.coords usa: (ID, x1, y1, x2, y2)
    canvas.coords(hunter[4], hunter[0], hunter[1], hunter[0] + 30, hunter[1]+ 40)
    #los valores respectivamente son, el ID, esquina superior derecha, esquina inferior derecha (x+ancho, y+alto)
    ventana.after(20, animove)#Le dice a la ventana que vuelva a correr esta función en 20 ms

#Ventana interfazconfig
ventana = tk.Tk()#crea base
ventana.title("MH 2026_FranLi") #Título de la ventana
ventana.resizable(False,False)#Para que el usuario no pueda alterar el tamaño de ventana

# Area donde se dibujarán los rectángulos
canvas = tk.Canvas(ventana, width=ANCHO_VP, height=ALTO_VP, bg="#222222")#Dimensiones y color
canvas.pack()#Coloca el canvas dentro de la ventana
#Dibuja un rectángulo que representa el suelo
canvas.create_rectangle(0, ALTO_VP-20, ANCHO_VP, ALTO_VP, fill="green")
#Dibujar a hunter(jugador)
hunter[4] = canvas.create_rectangle(hunter[0], hunter[1], hunter[0] + 30, hunter [1] + 40, fill="purple", outline="white")#Asigna posición, tamaño y colores al dibujo

#Binds, spn la vinculacion de eventos conecta las teclas fisicas con las funciones del programa
ventana.bind("<KeyPress-Left>", izquier)#Vincula flecha izq para que active función izquier
ventana.bind("<KeyPress-Right>", derecha)#Vincula flecha der para que active función derecha
ventana.bind("<KeyPress-space>", salto)#Vincula espacio para que active función salto
ventana.bind("<KeyPress-a>", izquier)#Vincula a para funcion izquier
ventana.bind("<KeyPress-d>", derecha)#Vincula d para funcion derecha
ventana.bind("<KeyPress-w>", salto)#Vincula w para funcion salto
#KeyRelease es un evento, se activa cuando el usuario  levanta cualquier tecla
ventana.bind("<KeyRelease>", detener_key)#al activarse, la funcion detener_key revisa cual fue y apaga el interruptor

animove()

ventana.mainloop()
