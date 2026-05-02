# sin musica, sin efectos de sonido 🐍
import tkinter as tk
import random
import json
import os
from tkinter import messagebox

# Constantes
ANCHO = 720
ALTO = 720
TAMANO_CELDA = 20

# Crear ventana
ventana = tk.Tk()
ventana.title("Snake 🐍")
ventana.resizable(False, False)

canvas = tk.Canvas(ventana, width=ANCHO, height=ALTO, bg="black")
canvas.pack()

ARCHIVO_GUARDADO = "snake_save.json"

# Valores por defecto
serpiente = [(360, 360), (340, 360), (320, 360)]
direccion = (20, 0)
puntos = 0
pausado = False

def nueva_comida():
    x = random.randrange(0, ANCHO, TAMANO_CELDA)
    y = random.randrange(0, ALTO, TAMANO_CELDA)
    return (x, y)

comida = nueva_comida()

def guardar_juego():
    datos = {
        "serpiente": serpiente,
        "direccion": list(direccion),
        "comida": list(comida),
        "puntos": puntos
    }
    with open(ARCHIVO_GUARDADO, "w") as f:
        json.dump(datos, f)

def cargar_juego():
    global serpiente, direccion, comida, puntos
    if os.path.exists(ARCHIVO_GUARDADO):
        with open(ARCHIVO_GUARDADO, "r") as f:
            datos = json.load(f)
        serpiente = [tuple(s) for s in datos["serpiente"]]
        direccion = tuple(datos["direccion"])
        comida = tuple(datos["comida"])
        puntos = datos["puntos"]
        return True
    return False

if os.path.exists(ARCHIVO_GUARDADO):
    respuesta = messagebox.askyesno("Partida guardada", "¿Quieres continuar la partida guardada?")
    if respuesta:
        cargar_juego()

def dibujar_serpiente():
    canvas.delete("all")
    canvas.create_rectangle(
        comida[0], comida[1],
        comida[0] + TAMANO_CELDA, comida[1] + TAMANO_CELDA,
        fill="red", outline="black"
    )
    for i, (x, y) in enumerate(serpiente):
        color = "lime" if i == 0 else "green"
        canvas.create_rectangle(
            x, y,
            x + TAMANO_CELDA, y + TAMANO_CELDA,
            fill=color, outline="black"
        )

def reiniciar():
    global serpiente, direccion, comida, puntos, pausado
    serpiente = [(360, 360), (340, 360), (320, 360)]
    direccion = (20, 0)
    comida = nueva_comida()
    puntos = 0
    pausado = False
    mover()

def game_over():
    if os.path.exists(ARCHIVO_GUARDADO):
        os.remove(ARCHIVO_GUARDADO)
    canvas.delete("all")
    canvas.create_text(ANCHO//2, ALTO//2 - 30, text="GAME OVER", fill="red", font=("Arial", 40))
    boton = tk.Button(ventana, text="Volver a empezar", font=("Arial", 16), bg="white",
                      command=lambda: [boton.destroy(), reiniciar()])
    canvas.create_window(ANCHO//2, ALTO//2 + 40, window=boton)

def pausar(event):
    global pausado
    if not pausado:
        pausado = True
        canvas.create_text(ANCHO//2, ALTO//2, text="PAUSA", fill="white", font=("Arial", 40), tags="pausa")
        canvas.create_text(ANCHO//2, ALTO//2 + 50, text="G = Guardar y salir", fill="yellow", font=("Arial", 20), tags="pausa")
    else:
        pausado = False
        canvas.delete("pausa")
        mover()

def guardar_y_salir(event):
    if pausado:
        guardar_juego()
        ventana.destroy()

def mover():
    global comida
    if pausado:
        return
    x, y = serpiente[0]
    nueva_cabeza = (x + direccion[0], y + direccion[1])

    if nueva_cabeza[0] < 0 or nueva_cabeza[0] >= ANCHO or nueva_cabeza[1] < 0 or nueva_cabeza[1] >= ALTO:
        game_over()
        return

    if nueva_cabeza in serpiente:
        game_over()
        return

    serpiente.insert(0, nueva_cabeza)

    if nueva_cabeza == comida:
        comida = nueva_comida()
    else:
        serpiente.pop()

    dibujar_serpiente()
    ventana.after(150, mover)

def cambiar_direccion(event):
    global direccion
    if event.keysym == "Up" and direccion != (0, 20):
        direccion = (0, -20)
    elif event.keysym == "Down" and direccion != (0, -20):
        direccion = (0, 20)
    elif event.keysym == "Left" and direccion != (20, 0):
        direccion = (-20, 0)
    elif event.keysym == "Right" and direccion != (-20, 0):
        direccion = (20, 0)

ventana.bind("<Escape>", pausar)
ventana.bind("g", guardar_y_salir)
ventana.bind("<KeyPress>", cambiar_direccion)

mover()
ventana.mainloop()
