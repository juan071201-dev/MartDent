import sqlite3

def crear_base_datos():
    conn = sqlite3.connect('martdent.db')
    cur = conn.cursor()

    # Borrar tabla anterior si existe
    cur.execute("DROP TABLE IF EXISTS pacientes")

    # Crear nueva tabla de pacientes
    cur.execute('''
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_documento TEXT,
        nro_documento TEXT UNIQUE,
        sexo TEXT,
        apellido_paterno TEXT,
        apellido_materno TEXT,
        nombres TEXT,
        fecha_nacimiento TEXT,
        celular TEXT,
        departamento TEXT,
        direccion TEXT,
        acompaniante TEXT,
        alergias TEXT,
        enfermedades TEXT
    )
    ''')

    # Crear otras tablas si no existen
    cur.execute('''
    CREATE TABLE IF NOT EXISTS citas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        hora TEXT NOT NULL,
        motivo TEXT,
        FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS tratamientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio REAL NOT NULL
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS historial (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')

    cur.execute("SELECT * FROM usuarios WHERE username = 'admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", ('admin', 'admin123'))

    conn.commit()
    conn.close()
