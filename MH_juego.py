import tkinter as tk#importación de la librería tkinter y se nombra como tk
import pygame as py#importación de la librería pygame para el audio
import math#importación de la librería de mate para su uso posterior


#Constantes para la ventana
ANCHO_VP = 800 #ancho de la ventana principal
ALTO_VP = 600 #alto de la ventana prrincipal
GRAVEDAD = 0.8#valor de gravedad
POTENCIA_JUMP = -15 #potencia del salto, es negativo porque arriba es restar en Y
VELOCIDAD_MOV = 6 #velocidad de movimiento
#Dimensiones Hunter
ANCHO_HUNTER = 30 
ALT_HUNTER = 40

#Game state

#info de hunter(jugador)
hunter = [100, 100, 0, False, None]
#i[0]: posición x
#i[1]: posición y
#i[2]: velocidad vertical (vy)
#i[3]: boolean sobre suelo 
#i[4]: identidad del dibuj en el Canvas (ID)

#Lista de plataformas
#cada lista tiene: [x, y, ancho, alto, ID, color]
plataformas = [[0, 580, 300, 20, None, "brown"], [500, 580, 300, 20, None, "brown"], [300, 450, 200, 20, None, "orange"], [85, 350, 150, 20, None, "orange"], [550, 300, 150, 20, None, "orange"]]
#La primera lista es el suelo pt1 
# La segunda es la otra parte del suelo para crear un hueco 
#La tercera, plataforma 1
#La cuarta, plataforma 2
#La quinta, plataforma 3
#Lista de escaleras: [x, y, ancho, alto, ID, color]
escaleras = [[350, 350, 40, 230, None, "#7F611F"]]

#info de la meta
#en la lista se tiene: [ x, y, ancho, alto, id]
meta = [650, 250, 30, 30, None]

#interruptores de las teclas para un movimiento fluido 
teclas = {"Left": False, "Right": False, "space": False, "Down": False}
#En orden respectivo de izquierda a derecha
#Estado de la flecha izquierda o a, estado de la flecha derecha o d, estado de la tecla espacio o W

#Funciones de movimiento, entradas
def izquier(event):
    teclas["Left"] = True #Activa interruptor para ir a la izquierda
def derecha(event):
    teclas["Right"] = True#Lo mismo que el de arriba pero para la derecha
def salto(event):
    teclas["space"] = True#Lo mismo pero hacia arriba, el salto
def abajo(event):
    teclas["Down"] = True#Lo mismo pero para bajar

def detener_key(event):#Funcion para detener el interruptor
    k = event.keysym #captura nombre de la tecla que el usuario dejó de presionar
    if k in ["Left", "a", "A"]: # si se deja de presionar
        teclas["Left"] = False # apaga el interruptor de izq
    elif k in ["Right", "d", "D"]:# si fue ir a la derecha 
        teclas["Right"] = False #apaga interruptor de derecha
    elif k in ["space", "w", "W"]:# si fue salto, arriba
        teclas["space"] = False # apaga interruptor de salto
    elif k in ["Down", "s", "S"]:# si fue abajo, baja escalera
        teclas["Down"] = False# apaga interruptor de bajar

#Lógica del mov!! y colisiones

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
    #Lógica de Escaleras
    en_laescalera = False
    for e in escaleras:
         # Revisa si hunter está en la escalera
         if (hunter[0] + ANCHO_HUNTER > e[0] and hunter[0] < e[0] + e[2] and
            hunter[1] + ALT_HUNTER > e[1] and hunter[1] < e[1] + e[3]):
            en_laescalera = True
            break
         
    if en_laescalera:#Si está en la escalera
            hunter[2] = 0 # se pone la velocidad vertical en 0 para que no caiga
            if teclas["space"]: #Con W o Espacio sube
                hunter [1] -= VELOCIDAD_MOV
            if teclas["Down"]: #Con flecha hacia abajo o S
                hunter[1] += VELOCIDAD_MOV
    else:    
        #se ejecuta si no está en las escaleras
        hunter[2] += GRAVEDAD # la gravedad jala hacia abajo sumando a la velocidad
        hunter[1] += hunter[2] # la posición Y cambia según la velocidad vertical que se acumule

    # Colisiónes en plataformas y piso, cambio para que sea posible
    hunter[3] = False # Se asume que esta en el aire, que está cayendo
    # si toca una plataforma o suelo, cambiará a True dentro del ciclo

    #Se recorre la lista de plataformas una a la vez
    for p in plataformas:
        #Se extraen solo los primeros 4 datos de las plataformas, que son los que se utilizarán
        px = p[0] #posición x del bloque
        py = p[1] #posición y del blque, ahí empieza el tope
        p_ancho = p[2] #ancho del bloque
        p_alto = p[3] #alto del bloque
        #si hunter está bajando
        if hunter[2] >= 0: # evita que hunter se quede pegado al techo si salta
            #Si los pies de hunter están en la plataforma
            if hunter[1] + ALT_HUNTER >= py and hunter[1] + ALT_HUNTER <= py + p_alto: # Revisamos si y + alto, es mayor que el tope del bloque y menor que el fondo del mismo
                #Si hunter esta alineado horizontalmente
                if hunter[0] + ANCHO_HUNTER >= px and hunter[0] < px + p_ancho:
                    #Si se cumplen las anteriores hay colisión!!!
                    hunter[1] = py - ALT_HUNTER # Se transporta justo arriba del bloque para evitar problema de hundimiento
                    hunter[2] = 0 # se pone la velocidad vertical en 0 para que deje de caer
                    hunter[3] = True #activa interruptor de suelo para que se pueda saltar otra vez
    #Límites laterales para que no desaparezca al salirse
    if hunter[0] < 0:# si la x es menor a 0, se frena en el borde izquierdo
        hunter[0] = 0
    elif hunter[0] + ANCHO_HUNTER > ANCHO_VP:# si la x + el ancho de hunter superan el ancho de ventana
        hunter[0] = ANCHO_VP - ANCHO_HUNTER # se frena a la derecha
    #Lógica reset por caídaa (por si se implementan huecos)
    if hunter[1] > ALTO_VP:
        hunter[0] = 100 # De nuevo a la x inicial
        hunter[1] = 100 # De nuevo a la y inicial
        hunter[2] = 0 #Su velocidad de caída se vuelve a 0 para que no siga sumando la vel vertical
        hunter[3] = False # empieza en el aire
    #Colisión con meta
    if (hunter [0] < meta[0] + meta[2] and hunter[0] + 30 > meta[0] and
        hunter [1] < meta[1] + meta[3]  and hunter[1] + 40 > meta[1]):# Revisa si el rectangulo de hunter y la meta se tocan
        print("NIVEL COMPLETADOO:)")# aparece en la consola
        #Al ganar, hunter vuelve al inicio
        hunter[0] = 100#coordenada en x
        hunter[1] = 100#coordenada en y
        hunter[2] = 0#velocidad vertical se reinicia


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
canvas = tk.Canvas(ventana, width=ANCHO_VP, height=ALTO_VP, bg="#2B122C")#Dimensiones y color
canvas.pack()#Coloca el canvas dentro de la ventana
#Dibujar plataformas (incluye suelo)
for p in plataformas:
    #Se usa p[5] para el color fill
    #Dibujar cada una de las plataformas gracias al ciclo. se usan los datos de "Plataformas"
    # p[0] = x, p[1] = y, p[2] = ancho, p[3] = alto
    # se guarda el id en p[4]  para que el sistema de colisiones sepa que es cada dato
    p[4] = canvas.create_rectangle(p[0], p[1], p[0] + p[2], p[1] + p[3], fill= p[5], outline="White")#Asigna también colores
#Dibujar escaleras
for e in escaleras:
    # e[0]=x, e[1]=y, e[2]=ancho, e[3]=alto, e[5]=color
    e[4] = canvas.create_rectangle(e[0], e[1], e[0] + e[2], e[1] + e[3], fill=e[5], outline="white", stipple="gray50" )#stipple para dar el efecto de rejilla!

#Dibujar a hunter(jugador)
hunter[4] = canvas.create_rectangle(hunter[0], hunter[1], hunter[0] + ANCHO_HUNTER, hunter [1] + ALT_HUNTER, fill="purple", outline="white")#Asigna posición, tamaño y colores al dibujo

#Dibujar la meta
meta[4] = canvas.create_oval(meta[0], meta[1], meta[0] + meta[2], meta[1] + meta[3], fill="cyan", outline="yellow" )

#Binds, spn la vinculacion de eventos conecta las teclas fisicas con las funciones del programa
ventana.bind("<KeyPress-Left>", izquier)#Vincula flecha izq para que active función izquier
ventana.bind("<KeyPress-Right>", derecha)#Vincula flecha der para que active función derecha
ventana.bind("<KeyPress-space>", salto)#Vincula espacio para que active función salto
ventana.bind("<KeyPress-Down>", abajo)#Vincula la flecha hacia abajo para que active la función bajar
ventana.bind("<KeyPress-a>", izquier)#Vincula a para funcion izquier
ventana.bind("<KeyPress-d>", derecha)#Vincula d para funcion derecha
ventana.bind("<KeyPress-w>", salto)#Vincula w para funcion salto
ventana.bind("<KeyPress-s>", abajo)#Vincula s para funcion bajar
#KeyRelease es un evento, se activa cuando el usuario  levanta cualquier tecla
ventana.bind("<KeyRelease>", detener_key)#al activarse, la funcion detener_key revisa cual fue y apaga el interruptor

animove()

ventana.mainloop()
