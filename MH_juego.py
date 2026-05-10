import tkinter as tk#importación de la librería tkinter y se nombra como tk
import pygame as py#importación de la librería pygame para el audio

# Funciones de control de  ventanas
def ir_a_juego():
    juego_pausa[0] = False
    ventana_menu.withdraw()  # Oculta el menú
    #Musica de juego
    py.mixer.music.stop()
    py.mixer.music.load("MH_Theme.mp3") # Pon aquí el nombre de tu otra canción
    py.mixer.music.play(-1)
    abrir_ventana_juego()

def ir_a_juego_base():
    es_mapa_personalizado[0] = False#Para el editor por si es ese
    ir_a_juego()

def abrir_ventana_ajustes():
    ventana_ajustes = tk.Toplevel()
    ventana_ajustes.title("Ajustes")
    ventana_ajustes.geometry("300x200")
    ventana_ajustes.focus_set()#se queda al frente
    ventana_ajustes.grab_set()
    tk.Label(ventana_ajustes, text="PANEL DE CONTROL", font=("Arial", 14, "bold")).pack(pady=10)

    def alternar_musica():#Función para manejo de música en ajustes
        if py.mixer.music.get_busy():
            py.mixer.music.pause()
            btn_musica.config(text="Reanudar Música")
        else:
            py.mixer.music.unpause()
            btn_musica.config(text="Pausar Música")
    btn_musica = tk.Button(ventana_ajustes, text="Pausar/Reanudar Música", command=alternar_musica, width=20) #Botón para alternar música
    btn_musica.pack(pady=10)

    # Botón para cerrar solo los ajustes
    tk.Button(ventana_ajustes, text="Cerrar", command=ventana_ajustes.destroy).pack(pady=10)


def volver_al_menu_desde_juego():
    # Volver a música de menú
    py.mixer.music.stop()
    py.mixer.music.load("MH_menuTheme.mp3")
    py.mixer.music.play(-1)
    # Esta función se asegura de limpiar todo antes de volver
    global ventana
    ventana.destroy()        # Cierra la ventana del juego
    ventana_menu.deiconify() # Muestra el menú de nuevo


def ir_a_editor():#Funcion para llamar a la ventana del editor de mapas
    ventana_menu.withdraw()
    # Resetear el mapa del editor para empezar limpio
    mapa_personalizado[1] = {"plataformas": [], "escaleras": [], "enemigos": []}
    meta_personalizada[1] = [None]
    inicio_personalizado[1] = [100, 100]
    lanzar_ventana_editor()

#Sistemas para las puntuaciones
def guardar_puntajes (puntos_finales):
    # with open para abrir archivo y cerrarlo
    with open("scores.txt", "a") as f:# a es de append (añadir): va escribiendo sin borrar lo de antes
        f.write(f"Puntaje: {puntos_finales}\n") #Escribe el texto (/n: salto de linea)
def mostrar_puntos():#Para texto de records
    v_records = tk.Toplevel()
    v_records.title("Cazadores Leyenda")
    v_records.geometry("300x400")

    tk.Label(v_records, text="HISTORIAL DE PUNTOS", font=("Arial", 16, "bold")).pack(pady=10)
    
    try:
        with open("scores.txt", "r") as f:
            lineas = f.readlines()
        
        # Extrae solo los números de cada línea y los ordena de mayor a menor
        puntajes = []
        for linea in lineas:
            linea = linea.strip()
            if linea:
                numero = int(linea.replace("Puntaje: ", ""))
                puntajes.append(numero)
        
        puntajes.sort(reverse=True)  # mayor a menor
        
        if puntajes:
            contenido = "\n".join(f"Puntaje: {p}" for p in puntajes)
        else:
            contenido = "No hay puntajes registrados."

    except FileNotFoundError:
        contenido = "Aún no has jugado ninguna partida."
        
    text_area = tk.Text(v_records, height=15, width=30)
    text_area.insert(tk.END, contenido)
    text_area.config(state="disabled")
    text_area.pack(pady=10)
    
    tk.Button(v_records, text="Cerrar", command=v_records.destroy).pack()

#Lógica del Editor de mapas
def click_editor(event):
    # Ajuste a la cuadrícula de 20x20 para precisión
    x = (event.x // 20) * 20
    y = (event.y // 20) * 20
    p_act = pantalla_edicion[0]
    if tipo_seleccionado[0] == "plataforma":
        ancho, alto = 100, 20
    
        # Dibujam el bloque naranja en el editor para verlo
        canvas_editor.create_rectangle(x, y, x + ancho, y + alto, fill="orange", outline="white")

        # Guarda los datos en lista, en la pantalla correspondiente para poder usarlos en el juego
        mapa_personalizado[p_act]["plataformas"].append([x, y, ancho, alto, None, "orange"])   
    elif tipo_seleccionado[0] == "escalera":#Lo mismo pero con la escalera
        ancho, alto = 30, 100
        canvas_editor.create_rectangle(x, y, x + ancho, y + alto, fill="#7F611F", outline="white", stipple="gray50")
        mapa_personalizado[p_act]["escaleras"].append([x, y, ancho, alto, None, "#7F611F"])
    elif tipo_seleccionado[0] == "enemigo":
        # Se eleije imagen
        imagen_a_usar = img_enemigo_rojo if tipo_denemigo[0] == 1 else img_enemigo_sombra
        # Dibuja el sprite real en el editor para que sepa cuál puso
        canvas_editor.create_image(x, y, image=imagen_a_usar, anchor="nw")
    #Guarda[x, y, ancho, alto, tipo (1 o 2), ID_canvas, color/tag]
        mapa_personalizado[p_act]["enemigos"].append([x, y, 30, 30, tipo_denemigo[0], None, "enemigo"])
    elif tipo_seleccionado[0] == "meta":
        ancho, alto = 40, 40
        # Dibuja un círculo cian para representar la meta en el editor
        canvas_editor.create_oval(x, y, x + ancho, y + alto, fill="cyan", outline="yellow", width=2)
        # Guarda la posición en lista de metas
        meta_personalizada[p_act] = [x, y, ancho, alto, None]
    elif tipo_seleccionado[0] == "inicio":
        # Guarda la coordenada donde el usuario hizo clic
        inicio_personalizado[1] = [x, y]
        # Dibujo verde temporal para marcarlo
        canvas_editor.create_rectangle(x, y, x+30, y+40, outline="#2ecc71", dash=(4, 4), width=2)
        canvas_editor.create_text(x+15, y-10, text="INICIO", fill="#2ecc71", font=("Arial", 8, "bold"))
def lanzar_ventana_editor():
    global ventana_editor, canvas_editor
    ventana_editor = tk.Toplevel() 
    ventana_editor.title("Editor de Mapas - Murcian Hunter")
    ventana_editor.geometry(f"{ANCHO_VP}x{ALTO_VP + 120}") #Extra de espacio para los botones
    
    # Crea el Canvas
    canvas_editor = tk.Canvas(ventana_editor, width=ANCHO_VP, height=ALTO_VP)
    canvas_editor.pack()
    
    # Fondo igual juego 
    canvas_editor.create_image(0, 0, image=img_fondo, anchor="nw")
    
    # Instrucción visual
    canvas_editor.create_text(400, 20, text="MODO EDITOR: Haz clic para colocar plataformas", fill="white", font=("Arial", 12, "bold"))

    # Evento de clic
    canvas_editor.bind("<Button-1>", click_editor)

    #Panel de objetos y pantallas
    #Se usa frame para agrupar los botones
    #Se utiliza setitem en esta seccion para modificar elementos dentro de la lista con ayuda de lambda no se puede usar =, cambia indices
    frame_objetos = tk.Frame(ventana_editor, bg="#2c3e50", pady=5)
    frame_objetos.pack(fill="x")
    
    tk.Label(frame_objetos, text="CONSTRUCCIÓN:", fg="white", bg="#2c3e50", font=("Arial", 10, "bold")).pack(side="left", padx=10)
    
    # Cambia la variable 'tipo_seleccionado' para que el clic sepa qué dibujar
    tk.Button(frame_objetos, text="BLOQUE", width=12, command=lambda: tipo_seleccionado.__setitem__(0, "plataforma")).pack(side="left", padx=5)
    tk.Button(frame_objetos, text="ESCALERA", width=12, command=lambda: tipo_seleccionado.__setitem__(0, "escalera")).pack(side="left", padx=5)
    
    tk.Label(frame_objetos, text=" | EDITAR:", fg="white", bg="#2c3e50").pack(side="left", padx=5)
    
    #Boton para poner meta
    tk.Button(frame_objetos, text="META", width=12, bg="cyan", command=lambda: tipo_seleccionado.__setitem__(0, "meta")).pack(side="left", padx=5)
    # En el panel de objetos del editor
    tk.Button(frame_objetos, text="INICIO PERSONAJE", bg="#2ecc71", command=lambda: tipo_seleccionado.__setitem__(0, "inicio")).pack(side="left", padx=5)
    #Panel de enemigos
    frame_enemigos = tk.Frame(ventana_editor, bg="#34495e", pady=5)
    frame_enemigos.pack(fill="x")
    tk.Label(frame_enemigos, text="ENEMIGOS:", fg="white", bg="#34495e", font=("Arial", 10, "bold")).pack(side="left", padx=10)
    
    # Al elegir enemigo, se define el 'tipo_seleccionado' y el 'tipo_denemigo' (1:Rojo, 2:Sombra)
    tk.Button(frame_enemigos, text="BAT ROJO", bg="#e74c3c", fg="white", command=lambda: [tipo_seleccionado.__setitem__(0, "enemigo"), tipo_denemigo.__setitem__(0, 1)]).pack(side="left", padx=5)
    tk.Button(frame_enemigos, text="BAT SOMBRA", bg="#8e44ad", fg="white", command=lambda: [tipo_seleccionado.__setitem__(0, "enemigo"), tipo_denemigo.__setitem__(0, 2)]).pack(side="left", padx=5)

    # Funcion para jugar con el mapa
    def probar_mapa_pro():
        juego_pausa[0] = False
        es_mapa_personalizado[0] = True #activa el interruptor para cargar pantalla uando el del editor
        # Hunter inicia donde el usuario marcó en el editor
        coords = inicio_personalizado[1]
        hunter[0], hunter[1], hunter[2] = coords[0], coords[1], 0
        game_state["pantalla_actual"] = 1 #Resetea a la pantalla 1
        # carga de los datos del editor a las listas activas
        global plataformas, escaleras, enemigos
        plataformas = mapa_personalizado[1]["plataformas"]
        escaleras = mapa_personalizado[1]["escaleras"]
        enemigos = mapa_personalizado[1]["enemigos"]
        datos_meta = meta_personalizada.get(1, [None])
        if datos_meta[0] is not None:
            meta[0], meta[1], meta[2], meta[3] = datos_meta[0], datos_meta[1], datos_meta[2], datos_meta[3]
    
        # Cierra editor y lanza el juego con la música
        ventana_editor.destroy()
        ir_a_juego() # Esta función ya pone la música y abre el juego

    # Botones del editor
    btn_probar = tk.Button(ventana_editor, text="PROBAR NIVEL", bg="green", fg="white", command=probar_mapa_pro)
    canvas_editor.create_window(100, 50, window=btn_probar)

    btn_salir = tk.Button(ventana_editor, text="Guardar y Salir", command=lambda: [ventana_editor.destroy(), ventana_menu.deiconify()])
    canvas_editor.create_window(700, 50, window=btn_salir)



#Pantalla final Game over o Victoria
def mostrar_pantalla_final(mensaje, color, puntos_finales):
    guardar_puntajes(puntos_finales)
    global ventana
    # se detiene juego y música
    py.mixer.music.stop()
    
    #Oculta ventana de juego
    ventana.withdraw()

    # Ventana de resultado
    v_final = tk.Toplevel()
    v_final.title("Fin de la Partida")
    v_final.geometry("400x300")
    v_final.configure(bg=color)
    v_final.resizable(False, False)
    
    # Centra textos
    tk.Label(v_final, text=mensaje, font=("Impact", 35), bg=color, fg="white").pack(pady=30)
    tk.Label(v_final, text=f"Puntaje Obtenido: {puntos_finales}", font=("Arial", 16, "bold"), bg=color, fg="white").pack(pady=10)
    
    def cerrar_y_regresar():
        v_final.destroy()
        if 'ventana' in globals() and ventana.winfo_exists():#Cierra el juego
            ventana.destroy()
        # Reinicio de valores para la próxima partida
        puntos[0] = 0
        vidas[0] = 3
        game_state["pantalla_actual"] = 1
        ventana_menu.deiconify() # Muestra el menú
        # Reinicia música del menúddwadd
        py.mixer.music.load("MH_menuTheme.mp3")
        py.mixer.music.play(-1)

    tk.Button(v_final, text="Volver al Menú", font=("Arial", 12, "bold"), command=cerrar_y_regresar).pack(pady=30)
    
    # Bloquear el juego de fondo
    v_final.grab_set()

#Constantes para la ventana
ANCHO_VP = 800 #ancho de la ventana principal
ALTO_VP = 600 #alto de la ventana prrincipal
GRAVEDAD = 0.8#valor de gravedad
POTENCIA_JUMP = -15 #potencia del salto, es negativo porque arriba es restar en Y
VELOCIDAD_MOV = 5 #velocidad de movimiento
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

#Lista de datos de mapa
#cada lista tiene: [x, y, ancho, alto, ID, color]
#plataformas = [[0, 580, 300, 20, None, "brown"], [500, 580, 300, 20, None, "brown"], [300, 450, 200, 20, None, "orange"], [85, 350, 150, 20, None, "orange"], [550, 300, 150, 20, None, "orange"]]
#La primera lista es el suelo pt1 
# La segunda es la otra parte del suelo para crea#77581r un hueco 
#La tercera, plataforma 1...
#Lista de escaleras: [x, y, ancho, alto, ID, color]
#escaleras = [[300, 350, 40, 230, None, "#7F611F"]]
pantallas = {
    1: {
        "plataformas": [# plataformas de la primer pantalla
            [0, 580, 300, 20, None, "brown"], 
            [500, 580, 300, 20, None, "brown"], 
            [300, 450, 200, 20, None, "#2b1d0e"]
        ],
        "escaleras": [ # lista de escaleras de la primer pantalla
            [350, 350, 30, 230, None, "#7F611F"] # Escalera del nivel 1
        ]
    },
    2: {
        "plataformas": [ #Plataformas de la segunda pantalla
            [0, 580, 800, 20, None, "green"], 
            [200, 300, 400, 20, None, "blue"]
        ],
        "escaleras": [ # lista de las escaleras de la segunda pantalla
            [100, 200, 30, 380, None, "#7F611F"], # Escalera diferente para nivel 2
            [600, 200, 30, 380, None, "#7F611F"]  
            ]}}

#Para el inicio
game_state = {"pantalla_actual": 1}
# se accede primero al numero de pantalla y despues a los datos de la misma
plataformas = pantallas[game_state["pantalla_actual"]]["plataformas"]#se extrae la lista segun pantalla actual
escaleras = pantallas[game_state["pantalla_actual"]]["escaleras"]#Lo mismo pero con la lista de escaleras
#info de la meta
#en la lista se tiene: [ x, y, ancho, alto, id]
meta = [650, 250, 30, 30, None]

# Matriz de muerciélagos [ID, x, y]
murcielagos = []
puntos = [0] #Lista mutable
contador_frames = [0] #para simular azar

#Matriz de enemigos
#Tipos: enemigo normal, enemigo roba puntos
enemigos =[ [400, 540, 30, 30, 1, None, "red"], [200, 250, 30, 30, 2, None, "purple"]]
vidas = [3]#Lista mutable para vidas

#Variables para el editor
# Guarda [x, y] de donde empezará Hunter en el mapa del editor
inicio_personalizado = {1: [100, 100]} # Por defecto empieza en 100, 100
juego_pausa = [False]
bloques_creados_editor = [] #Aquí se guardan los bloques
# Donde se  guardará la estructura del mapa creado por el usuario
mapa_personalizado = { 1: {"plataformas": [], "escaleras": [], "enemigos": []}}
es_mapa_personalizado = [False]  # Interruptor para saber qué lógica de niveles usar
pantalla_edicion = [1]           # Indica si esta editando la pantalla 1 
tipo_seleccionado = ["plataforma"] # Lo que el usuario está colocando actualmente
tipo_denemigo = [1] #1 el rojo, 2 la sombra
meta_personalizada = {1: [None]} # Para guardar la meta de cada pantalla


#interruptores de las teclas para un movimiento fluido 
teclas = {"Left": False, "Right": False, "space": False, "Down": False}
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

#Función para cargar mas pantallas en el nivel predeterminado
def cargar_npantalla(num):
    global plataformas, escaleras, enemigos, meta

    #Limpiar canvas
    for p in plataformas:
        canvas.delete(p[4])
    for e in escaleras:
        canvas.delete(e[4])
    for en in enemigos: canvas.delete(en[5])
    if meta[4]: canvas.delete(meta[4]) # Borra meta vieja

    #Condicion para determinar si es el predeterminado o nivel del editor
    #Si  entra por iniciar partida sera Flase y se usa nivel predeterminado
    if es_mapa_personalizado[0]:
        fuente = mapa_personalizado
        datos_meta = meta_personalizada.get(1, [None]) #Usa meta del editor
    else:
        fuente = pantallas
        #En el nivel predeterminado, meta solo en pantalla 2
        datos_meta = [650, 250, 30, 30, None] if num == 2 else [None]

    #nuevos datos
    plataformas  = fuente[num]["plataformas"]
    escaleras = fuente[num]["escaleras"]
    #.get en caso de que no haya enemigos definidos
    enemigos = fuente[num].get("enemigos", [])
    #se dibujan las nuevas plataformas y escaleras con ciclos
    for p in plataformas:
        p[4] = canvas.create_rectangle(p[0], p[1], p[0]+p[2], p[1]+p[3], fill=p[5], outline="white")
    for e in escaleras:
        e[4] = canvas.create_rectangle(e[0], e[1], e[0]+e[2], e[1]+e[3], fill=e[5], outline="white", stipple="gray50")
    for en in enemigos:
        # Se asigna (Rojo o Sombra) basado en el tipo (en[4])
        img_a_dibujar = img_enemigo_rojo if en[4] == 1 else img_enemigo_sombra
        en[5] = canvas.create_image(en[0], en[1], image=img_a_dibujar, anchor="nw")
   
    #dibuja meta si existe en la pantalla
    if datos_meta[0] is not None:
        meta[0], meta[1], meta[2], meta[3] = datos_meta[0], datos_meta[1], datos_meta[2], datos_meta[3]
        meta[4] = canvas.create_oval(meta[0], meta[1], meta[0]+meta[2], meta[1]+meta[3], fill="cyan", outline="yellow")
    

#Lógica del mov!! y colisiones

#Lógica y colisiones de objetos que caen
def lluvia_murcielagos(canvas, lista_m, contador, h_x):
    contador[0] += 1 #aumenta contador de cuadros
    
    if contador[0] % 60 == 0:# Cada 60 cuadros se genera un murciélago
        #"Azar"
        mx = (h_x * 7 + contador[0]) % (ANCHO_VP - 100) + 50 #Usa posición del jugador(h_x) y el tiempo para que parezca al azar la aparición
        m_id = canvas.create_image(mx, -20, image = img_moneda, anchor = "nw")#Dibujo en el canvas

        lista_m.append([m_id, mx, -20])#Nueva fila en matriz

# Colisiones de murcielagos
def actualizar_murcielagos(canvas, lista_m, puntos, h_pos, text_id):
    #Se recorre la matriz de muerciélagos
    for i in range(len(lista_m) - 1, -1, -1):
        m = lista_m [i] #Extrae datos
        m[2] += 4 #Actualiza la columna 2 (y) para caída

        canvas.coords(m[0], m[1], m[2]) #para mover el dibujo(imagenes solo ocupan x, y)

        #Detección de colisiones
        #h_pos es la lista de hunter
        if (hunter[0] < m[1] + 20 and h_pos[0] + ANCHO_HUNTER > m[1] and
            h_pos[1] < m[2] + 20 and h_pos[1] + ALT_HUNTER > m[2]): #cuando colisionan

            canvas.delete(m[0]) # se elimina el dibujo
            lista_m.pop(i)      #Elimina fila de la matriz
            puntos[0] += 10 # aumenta el valor en puntaje_lista
            canvas.itemconfig(text_id, text=f"Puntos: {puntos[0]}")#actualiza nuevo puntaje

        elif m[2] > ALTO_VP: # si el murcielago pasa el alto de la ventana 
            canvas.delete(m[0])#se borra
            lista_m.pop(i) #Borra de la matriz

#Colisiones y gestión de enemigos y vida
def coli_enemigos(canvas, lista_e, h_pos, vidas_l, puntos_l, txt_puntos, txt_vidas):
    #h_pos = lista de hunter
    for en in lista_e:
        if (h_pos[0] < en[0] + en[2] and h_pos[0] + 30 > en[0] and h_pos[1] < en[1] + en[3] and h_pos[1] + 40 > en[1]): #colision de hunter con los enemigos
            #Penalización
            vidas_l[0] -= 1
            if en[4] == 2:# Si es del segundo tipo, roba puntos
                puntos_l[0] = max(0, puntos_l[0] - 20)
            #Actualización para visualizar
            canvas.itemconfig(txt_vidas, text=f"Vidas: {vidas_l[0]}")#Muestra vidas
            canvas.itemconfig(txt_puntos, text=f"Puntos: {puntos_l[0]}")#Muestra puntos
            #Reset de posiciónn de hunter por el golpe
            h_pos[0], h_pos[1], h_pos[2] = 100, 100, 0

            if vidas_l[0] <= 0:#Si la vida llega a cero
                juego_pausa[0] = True#Para el juego
                # Llama a la pantalla roja de Game Over
                mostrar_pantalla_final("GAME OVER", "#5E0000", puntos_l[0])
                return # Detiene la ejecución de la colisión




#Movimiento y colisiones del jugador
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
    if en_laescalera:
        hunter[2] = 0 # Detiene gravedad para que no se caiga
        # salto lateral: espacio + direccion
        if teclas["space"] and (teclas["Left"] or teclas["Right"]):
            hunter[2] = POTENCIA_JUMP # potencia de salto
            hunter[3] = False # ya no esta en suelo
            en_laescalera = False # apaga modo escalera para volar
            
        # salto hacia arriba: si ya llego al tope de la escalera (e[1])
        elif teclas["space"] and hunter[1] <= e[1] + 10: 
            hunter[2] = POTENCIA_JUMP # potencia de salto
            hunter[1] -= 10 # empujon extra para despegarse del borde
            hunter[3] = False # ya no esta en suelo
            en_laescalera = False # apaga modo escalera

        # para trepar: solo si no esta saltando
        elif teclas["space"]: 
            hunter[1] -= VELOCIDAD_MOV # sube por la escalera

        # para bajar: con la flecha hacia abajo
        if teclas["Down"]: 
            hunter[1] += VELOCIDAD_MOV # baja por la escalera
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
    #Lógica de cambio de zona paara un mapa extendido 
    if hunter[0] > ANCHO_VP: #Siguiente pantalla derecha
        hunter[0] = 10# teletransporta a huntee al inicio de la siguient pantalla
        # Se aumenta el contador de pantalla para pasar a la segunda
        game_state["pantalla_actual"] += 1
        
        if game_state["pantalla_actual"] in [1, 2]:# si la pantalla existe, se carga
            cargar_npantalla(game_state["pantalla_actual"])
            canvas.configure(bg="#000000")
            print(f"Cambio de zona: {game_state['pantalla_actual']}")

    elif hunter [0] < 0:#  Izquierda, pantalla anterior
        if game_state["pantalla_actual"] > 1: #Si no es la primera
            game_state["pantalla_actual"] -= 1
            hunter[0] = ANCHO_VP - 40 #Aparece en pantalla anterior
            cargar_npantalla(game_state["pantalla_actual"])
            print(f"Regresando a zona: {game_state['pantalla_actual']}")
        else:
            hunter[0] = 0#frena 

    #Lógica reset por caídaa (por si se implementan huecos)
    # Lógica reset por caída (dentro de mover_hunter)
    if hunter[1] > ALTO_VP:
        vidas[0] -= 1 # Resta una vida al contador
        canvas.itemconfig(texto_vidas, text=f"Vidas: {vidas[0]}") # Actualiza el texto en pantalla
        
        # Si se queda sin vidas, lanza la pantalla de Game Over
        if vidas[0] <= 0:
            juego_pausa[0] = True #Para juego
            mostrar_pantalla_final("GAME OVER", "#5E0000", puntos[0])
            return

        # Reseteo de posición y física del personaje en una sola línea
        hunter[0], hunter[1], hunter[2] = 100, 100, 0 # X inicial, Y inicial, Vy a cero
        hunter[3] = False # Empieza en el aire (no está en el suelo)
    #Colisión con meta
    if (hunter [0] < meta[0] + meta[2] and hunter[0] + 30 > meta[0] and
        hunter [1] < meta[1] + meta[3]  and hunter[1] + 40 > meta[1]):# Revisa si el rectangulo de hunter y la meta se tocan
        if not juego_pausa[0]: #Si el juego no esta pausado ya
            juego_pausa[0] =  True#Para el juego       
            print("NIVEL COMPLETADOO:)")# aparece en la consola
        # Llama a la pantalla verde de Victoria
        mostrar_pantalla_final("¡VICTORIA!", "#1B4D3E", puntos[0])
        # Resetea posicion por si acaso



#Animacion en ventana

def animove():
    if juego_pausa [0] or not ventana.winfo_exists():# Si se acaban las vidas deja de ejecutar el bucle del juego o si se cierra ventana
        return
    mover_hunter() # Ejecuta la lógica de movimiento y salto
    # Lógica de Cambio imagen de Hunter según dirección
    if not hunter[3]: # Si no está en el suelo
        if teclas["Left"]:
            canvas.itemconfig(hunter[4], image=img_hunter_jump_izq)
        else: # Si va a la derecha o cae recto
            canvas.itemconfig(hunter[4], image=img_hunter_jump_der)
    
    else: # Si está caminando o en el sueloI
        if teclas["Left"]:
            canvas.itemconfig(hunter[4], image=img_hunter_izq)
        elif teclas["Right"]:
            canvas.itemconfig(hunter[4], image=img_hunter_der)


    #Ejecución de las funciones de los murcielagos, pasando las listas como argumentos
    lluvia_murcielagos(canvas, murcielagos, contador_frames, hunter[0])
    actualizar_murcielagos(canvas, murcielagos, puntos, hunter, texto_puntos)

    #Gestion de enemigos
    coli_enemigos(canvas, enemigos, hunter, vidas, puntos, texto_puntos, texto_vidas)

    #Actualiza el dibujo del personaje usando las coordenadas de  la lista de hunter
    #canva.coords usa: (ID, x, y) por se img
    canvas.coords(hunter[4], hunter[0], hunter[1])
    #los valores respectivamente son, el ID, esquina superior derecha, esquina inferior derecha (x+ancho, y+alto)
    ventana.after(20, animove)#Le dice a la ventana que vuelva a correr esta función en 20 ms

def abrir_ventana_juego():
    global ventana, canvas, texto_puntos, texto_vidas
    #Ventana juego config
    ventana = tk.Toplevel()#crea base
    ventana.title("Murcian Hunter") #Título
    ventana.resizable(False,False)#Para que el usuario no pueda alterar el tamaño de ventana
    ventana.protocol("WM_DELETE_WINDOW", volver_al_menu_desde_juego)# si cierra la ventana con x llama a la funcion de volver al menu

    # Area donde se dibujarán los rectángulos
    canvas = tk.Canvas(ventana, width=ANCHO_VP, height=ALTO_VP, bg="#2B122C")#Dimensiones y color
    canvas.pack()#Coloca el canvas dentro de la ventana
    #Dibujo del fondo (img) atras del todo
    canvas.create_image(0, 0, image = img_fondo, anchor="nw")

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

    # Dibujar Enemigos con imagen
    for en in enemigos:
        if en[4] == 1: # Tipo Rojo
            en[5] = canvas.create_image(en[0], en[1], image=img_enemigo_rojo, anchor="nw")#nw toma la esquina superior y la pone en las coords
        else:          # Tipo Sombra
            en[5] = canvas.create_image(en[0], en[1], image=img_enemigo_sombra, anchor="nw")

    #Dibujar a hunter(jugador)  
    hunter[4] = canvas.create_image(hunter[0], hunter[1], image = img_hunter_der, anchor = "nw")#Dibujo img hunter

    #Dibujar la meta
    if es_mapa_personalizado[0]:
        # En el editor siempre se muestra si fue colocada
        meta[4] = canvas.create_oval(meta[0], meta[1], meta[0] + meta[2], meta[1] + meta[3], fill="cyan", outline="yellow")
    else:
        # En el predeterminado, la meta solo va en pantalla 2, así que al inicio va oculta
        # cargar_npantalla la dibujará cuando el jugador llegue a pantalla 2a
        meta[4] = None
        

    btn_config = tk.Button(ventana, text="⚙️", font=("Arial", 12), command=abrir_ventana_ajustes)#Botón de ajustes
    canvas.create_window(780, 30, window=btn_config)

    #Binds, son la vinculacion de eventos conecta las teclas fisicas con las funciones del programa
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
    def resetear_teclas(event):#Resetea oor el foco
        teclas["Left"] = False
        teclas["Right"] = False
        teclas["space"] = False
        teclas["Down"] = False
    ventana.bind("<FocusOut>", resetear_teclas)
    #Dibuja marcador de puntos en esquina
    texto_puntos = canvas.create_text(650, 30, text="Puntos:  0", fill="white", font=("Arial", 16, "bold"))
    texto_vidas = canvas.create_text(100, 30, text="Vidas: 3", fill="red", font=("Arial", 18, "bold"))
    # Botón de "Volver" dentro del juego (opcional si ya usas la X de la ventana)
    btn_regresar = tk.Button(ventana, text="Volver al Menú", command=volver_al_menu_desde_juego)
    canvas.create_window(760, 590, window=btn_regresar, width= "90", height= "20") # Lo pone en la esquina inferior derecha
    #Fix para quitar el click antes de empezar
    ventana.focus_set()          # Reclama el foco para la ventana
    ventana.grab_set()           # Bloquea eventos en otras ventanas hasta que esta se cierre
    ventana.attributes("-topmost", True) # Asegura que esté por encima de todo
    canvas.focus_set() #Para no tener q dar click
    animove()

#Ventana del Main menu
ventana_menu = tk.Tk()
ventana_menu.title("Murcial Hunter - menu")
ventana_menu.geometry("400x500")
ventana_menu.resizable(False,False)

#Carga de imagenes (sprites)
img_hunter_der = tk.PhotoImage(file="Hunter_right1.png") #Imagen de personaje viendo a la der
img_hunter_izq = tk.PhotoImage(file="Hunter_left.png")# viendo a la izq
img_hunter_jump_der = tk.PhotoImage(file="Hunter_up_right1.png")
img_hunter_jump_izq = tk.PhotoImage(file="Hunter_up_left.png")
img_fondo = tk.PhotoImage(file="game_background.png")# fondo de nivel
img_moneda = tk.PhotoImage(file="Bat_coin.png")# img de bat_coins
img_enemigo_rojo = tk.PhotoImage(file="Red_bat_enemy1.png")# Enemigo 1
img_enemigo_sombra = tk.PhotoImage(file="Shadow_enemy2.png")# enemigo 2

#Cargar música 
py.mixer.init()
py.mixer.music.load("MH_menuTheme.mp3")
py.mixer.music.play(-1)#suena hasta que se apague


# Elementos del Menú
title = tk.Label(ventana_menu, text="MURCIAN HUNTER", font=("Impact", 28))
title.pack(pady=40)



# El botón "INICIAR PARTIDA" llama a ir_a_juego para ocultar el menú
btn_play = tk.Button(ventana_menu, text="INICIAR PARTIDA", width=25, height=2, font=("Arial", 12, "bold"), bg="#911C75", fg="white", command=ir_a_juego_base)
btn_play.pack(pady=10)

#Botón para ir a ajustes
btn_ajustes_menu = tk.Button(ventana_menu, text="AJUSTES", width=20, command=abrir_ventana_ajustes)
btn_ajustes_menu.pack(pady=5)

# El botón del Editor (luego haremos su función)
btn_editor = tk.Button(ventana_menu, text="EDITOR DE MAPAS", width=25, height=2, font=("Arial", 10), command=ir_a_editor)
btn_editor.pack(pady=10)

#Botón de los records de puntos
btn_scores = tk.Button(ventana_menu, text="VER PUNTUACIONES", width=25, command=mostrar_puntos)
btn_scores.pack(pady=10)

ventana_menu.mainloop()