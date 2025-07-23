import sqlite3

DB = "martdent.db"

def obtener_pacientes():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM pacientes")
    pacientes = cur.fetchall()
    conn.close()
    return pacientes

def agregar_paciente(nombre, apellido, dni, fecha_nacimiento, telefono, correo):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO pacientes (nombre, apellido, dni, fecha_nacimiento, telefono, correo)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nombre, apellido, dni, fecha_nacimiento, telefono, correo))
    conn.commit()
    conn.close()
