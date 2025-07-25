import sqlite3

DB = "martdent.db"

def obtener_pacientes(filtro=""):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    query = "SELECT * FROM pacientes"
    if filtro:
        query += " WHERE LOWER(nro_documento) LIKE LOWER(?) OR LOWER(nombres) LIKE LOWER(?)"
        cur.execute(query, (f"%{filtro}%", f"%{filtro}%"))
    else:
        cur.execute(query)
    pacientes = cur.fetchall()
    conn.close()
    return pacientes


def agregar_paciente(datos):
    """Inserta un nuevo paciente. Devuelve True si se inserta, False si hay error (ej: duplicado)."""
    try:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO pacientes (
                tipo_documento, nro_documento, sexo, apellido_paterno, apellido_materno,
                nombres, fecha_nacimiento, celular, departamento, direccion,
                acompaniante, alergias, enfermedades
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datos["tipo_documento"], datos["nro_documento"], datos["sexo"],
            datos["apellido_paterno"], datos["apellido_materno"], datos["nombres"],
            datos["fecha_nacimiento"], datos["celular"], datos["departamento"],
            datos["direccion"], datos["acompaniante"], datos["alergias"], datos["enfermedades"]
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        return False  # Documento duplicado
    finally:
        conn.close()
    return True


def eliminar_paciente(paciente_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
    conn.commit()
    conn.close()


def obtener_paciente_por_id(paciente_id):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM pacientes WHERE id = ?", (paciente_id,))
    paciente = cur.fetchone()
    conn.close()
    return paciente


def actualizar_paciente(paciente_id, datos):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('''
        UPDATE pacientes SET
            tipo_documento = ?, nro_documento = ?, sexo = ?, apellido_paterno = ?,
            apellido_materno = ?, nombres = ?, fecha_nacimiento = ?, celular = ?,
            departamento = ?, direccion = ?, acompaniante = ?, alergias = ?, enfermedades = ?
        WHERE id = ?
    ''', (
        datos["tipo_documento"], datos["nro_documento"], datos["sexo"],
        datos["apellido_paterno"], datos["apellido_materno"], datos["nombres"],
        datos["fecha_nacimiento"], datos["celular"], datos["departamento"],
        datos["direccion"], datos["acompaniante"], datos["alergias"], datos["enfermedades"],
        paciente_id
    ))
    conn.commit()
    conn.close()
