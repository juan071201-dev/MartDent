import sqlite3

def obtener_historial(paciente_id):
    conn = sqlite3.connect("martdent.db")
    cur = conn.cursor()
    cur.execute("SELECT fecha, descripcion FROM historial WHERE paciente_id = ?", (paciente_id,))
    historial = cur.fetchall()
    conn.close()
    return historial

def agregar_historial(paciente_id, fecha, descripcion):
    conn = sqlite3.connect("martdent.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO historial (paciente_id, fecha, descripcion) VALUES (?, ?, ?)", 
                (paciente_id, fecha, descripcion))
    conn.commit()
    conn.close()
