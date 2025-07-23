import sqlite3

DB = "martdent.db"

def obtener_citas():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('''
        SELECT c.id, c.fecha, c.hora, c.motivo, p.nombre, p.apellido
        FROM citas c
        JOIN pacientes p ON c.paciente_id = p.id
    ''')
    citas = cur.fetchall()
    conn.close()
    return citas

def agregar_cita(paciente_id, fecha, hora, motivo):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO citas (paciente_id, fecha, hora, motivo)
        VALUES (?, ?, ?, ?)
    ''', (paciente_id, fecha, hora, motivo))
    conn.commit()
    conn.close()
