import sqlite3

def obtener_tratamientos():
    conn = sqlite3.connect('martdent.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM tratamientos')
    tratamientos = cur.fetchall()
    conn.close()
    return tratamientos

def agregar_tratamiento(nombre, descripcion, precio):
    conn = sqlite3.connect('martdent.db')
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO tratamientos (nombre, descripcion, precio)
        VALUES (?, ?, ?)
    ''', (nombre, descripcion, precio))
    conn.commit()
    conn.close()
