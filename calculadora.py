from tkinter import *
from math import *

# Crear ventana
ventana = Tk()
ventana.title("CALCULADORA")
ventana.geometry("380x600")
ventana.configure(background="SkyBlue4")

# Variable que guarda lo que se escribe
valor_tecla = StringVar()

# Campo de salida
Salida = Entry(ventana, font=("arial", 20, "bold"), width=22, bd=20, insertwidth=4, bg="powder blue", justify="right", textvariable=valor_tecla)
Salida.place(x=8, y=60)

# Función que se llama al presionar un botón
def click_boton(valor):
    actual = valor_tecla.get()
    valor_tecla.set(actual + str(valor))

def limpiar():
    valor_tecla.set("")

def calcular():
    try:
        resultado = str(eval(valor_tecla.get()))
        valor_tecla.set(resultado)
    except:
        valor_tecla.set("ERROR")

# Diccionario de botones con sus posiciones
botones = [
    ("0", 10, 180), ("1", 100, 180), ("2", 190, 180), ("3", 280, 180),
    ("4", 10, 240), ("5", 100, 240), ("6", 190, 240), ("7", 280, 240),
    ("8", 10, 300), ("9", 100, 300), ("π", 190, 300), (",", 280, 300),
    ("+", 10, 360), ("-", 100, 360), ("*", 190, 360), ("/", 280, 360),
    ("√", 10, 420), ("C", 100, 420), ("EXP", 190, 420), ("=", 280, 420),
    ("(", 10, 480), (")", 100, 480), ("%", 190, 480), ("ln", 280, 480),
]

# Crear botones dinámicamente
for (texto, x, y) in botones:
    if texto == "C":
        comando = limpiar
    elif texto == "=":
        comando = calcular
    elif texto == "π":
        comando = lambda t=pi: click_boton(t)
    elif texto == "ln":
        comando = lambda: click_boton("log(")
    elif texto == "√":
        comando = lambda: click_boton("sqrt(")
    elif texto == "EXP":
        comando = lambda: click_boton("**")
    else:
        comando = lambda t=texto: click_boton(t)

    Button(ventana, text=texto, width=11, height=3, command=comando).place(x=x, y=y)

ventana.mainloop()
