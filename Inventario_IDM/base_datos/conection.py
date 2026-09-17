import sqlite3

def conectar():

    conexion = sqlite3.connect("inventario.db")

    conexion.execute("PRAGMA foreign_keys = ON")
    
    return conexion