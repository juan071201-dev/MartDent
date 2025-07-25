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

from .pacientes import (
    obtener_pacientes, agregar_paciente, eliminar_paciente,
    obtener_paciente_por_id, actualizar_paciente
)

@main.route("/pacientes", methods=["GET", "POST"])
@login_requerido
def lista_pacientes():
    filtro = request.form.get("filtro", "")
    pacientes = obtener_pacientes(filtro)
    return render_template("pacientes.html", pacientes=pacientes, filtro=filtro)

@main.route("/agregar_paciente", methods=["POST"])
@login_requerido
def nuevo_paciente():
    datos = {
        "tipo_documento": request.form["tipo_documento"],
        "nro_documento": request.form["nro_documento"],
        "sexo": request.form["sexo"],
        "apellido_paterno": request.form["apellido_paterno"],
        "apellido_materno": request.form["apellido_materno"],
        "nombres": request.form["nombres"],
        "fecha_nacimiento": request.form["fecha_nacimiento"],
        "celular": request.form["celular"],
        "departamento": request.form["departamento"],
        "direccion": request.form["direccion"],
        "acompaniante": request.form["acompaniante"],
        "alergias": request.form["alergias"],
        "enfermedades": request.form["enfermedades"],
    }
    agregar_paciente(datos)
    return redirect(url_for("main.lista_pacientes"))

@main.route("/eliminar_paciente/<int:paciente_id>")
@login_requerido
def eliminar_paciente_route(paciente_id):
    eliminar_paciente(paciente_id)
    return redirect(url_for("main.lista_pacientes"))

@main.route("/editar_paciente/<int:paciente_id>", methods=["GET", "POST"])
@login_requerido
def editar_paciente(paciente_id):
    if request.method == "POST":
        datos = {
            "tipo_documento": request.form["tipo_documento"],
            "nro_documento": request.form["nro_documento"],
            "sexo": request.form["sexo"],
            "apellido_paterno": request.form["apellido_paterno"],
            "apellido_materno": request.form["apellido_materno"],
            "nombres": request.form["nombres"],
            "fecha_nacimiento": request.form["fecha_nacimiento"],
            "celular": request.form["celular"],
            "departamento": request.form["departamento"],
            "direccion": request.form["direccion"],
            "acompaniante": request.form["acompaniante"],
            "alergias": request.form["alergias"],
            "enfermedades": request.form["enfermedades"],
        }
        actualizar_paciente(paciente_id, datos)
        return redirect(url_for("main.lista_pacientes"))
    else:
        paciente = obtener_paciente_por_id(paciente_id)
        return render_template("editar_paciente.html", paciente=paciente)


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
