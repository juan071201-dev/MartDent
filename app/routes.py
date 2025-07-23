from flask import session
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for
from .pacientes import obtener_pacientes, agregar_paciente
from .citas import obtener_citas, agregar_cita
from .tratamientos import obtener_tratamientos, agregar_tratamiento
from .historial import obtener_historial, agregar_historial

main = Blueprint("main", __name__)

def login_requerido(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorada

@main.route("/")
@login_requerido
def home():
    return render_template("base.html")

@main.route("/pacientes")
@login_requerido
def lista_pacientes():
    pacientes = obtener_pacientes()
    return render_template("pacientes.html", pacientes=pacientes)

@main.route("/agregar_paciente", methods=["POST"])
@login_requerido
def nuevo_paciente():
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    dni = request.form["dni"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    telefono = request.form["telefono"]
    correo = request.form["correo"]

    agregar_paciente(nombre, apellido, dni, fecha_nacimiento, telefono, correo)
    return redirect(url_for("main.lista_pacientes"))

@main.route("/citas")
@login_requerido
def lista_citas():
    citas = obtener_citas()
    pacientes = obtener_pacientes()
    return render_template("citas.html", citas=citas, pacientes=pacientes)

@main.route("/agregar_cita", methods=["POST"])
@login_requerido
def nueva_cita():
    paciente_id = request.form["paciente_id"]
    fecha = request.form["fecha"]
    hora = request.form["hora"]
    motivo = request.form["motivo"]
    agregar_cita(paciente_id, fecha, hora, motivo)
    return redirect(url_for("main.lista_citas"))

@main.route("/tratamientos")
@login_requerido
def lista_tratamientos():
    tratamientos = obtener_tratamientos()
    return render_template("tratamientos.html", tratamientos=tratamientos)

@main.route("/agregar_tratamiento", methods=["POST"])
@login_requerido
def nuevo_tratamiento():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = float(request.form["precio"])
    agregar_tratamiento(nombre, descripcion, precio)
    return redirect(url_for("main.lista_tratamientos"))

@main.route("/historial/<int:paciente_id>")
@login_requerido
def ver_historial(paciente_id):
    historial = obtener_historial(paciente_id)
    pacientes = obtener_pacientes()
    paciente = next((p for p in pacientes if p[0] == paciente_id), None)
    return render_template("historial.html", historial=historial, paciente=paciente)

@main.route("/agregar_historial/<int:paciente_id>", methods=["POST"])
@login_requerido
def nuevo_historial(paciente_id):
    fecha = request.form["fecha"]
    descripcion = request.form["descripcion"]
    agregar_historial(paciente_id, fecha, descripcion)
    return redirect(url_for("main.ver_historial", paciente_id=paciente_id))
