import tkinter as tk#importación de la librería tkinter

def btn_play_press():#Función para probar el boton de empezar partida
    print("Play works! prueba de donde va a correr el juego")
def btn_editor_press():#Función para probar el boton que lleva al editor
    print("Editor works!! prueba de donde estará el editor")

ventana = tk.Tk()#Crea la ventana
ventana.title("Murcian Hunter")#Título de la ventana
ventana.geometry("400x500")#Dimensiones de la ventana

title = tk.Label(ventana, text="MURCIAN HUNTER", font=("Impact", 22))#Etiqueta con el título del juego
title.pack(pady=30)#Para centrar el título

btn_play = tk.Button(ventana, text="INICIAR PARTIDA", command= btn_play_press, width=20, height=2)#Botón para iniciar el juego
btn_play.pack(pady=10)#Centra el botón

btn_editor =  tk.Button(ventana, text="Editor de mapas!!", command= btn_editor_press, width=15, height=1)#Botón para abrir el editor de mapas
btn_editor.pack(pady=5)#Centra el botón y lo pone debajo del anterior

ventana.mainloop()


