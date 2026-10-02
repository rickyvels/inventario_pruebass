"""
Versión web del sistema (la que usa Vercel).
Reutiliza las mismas clases y funciones que main.py; solo cambia la interfaz (HTML en vez de consola).
"""
import os
import sys

from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file

# Permite importar productos/, utilidades/ y reportes/ desde la raíz del proyecto
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from productos.producto import Inventario, ProductoTecnologico, ProductoAccesorio
from utilidades.validaciones import (
    CATEGORIAS_PERMITIDAS,
    validar_texto_web,
    validar_numero_positivo_web,
    validar_categoria_web,
)
from utilidades.generadores import generador_codigos
from reportes.gestor_reportes import generar_reporte_txt

app = Flask(__name__, template_folder=os.path.join(RAIZ, "templates"))
app.secret_key = os.environ.get("SECRET_KEY", "cambia-esta-clave-en-vercel")


# ==========================================
# Guardar / cargar el inventario en la sesión del navegador
# (Vercel no conserva memoria entre peticiones)
# ==========================================
def producto_a_dict(prod) -> dict:
    datos = {
        "codigo": prod.codigo,
        "nombre": prod.nombre,
        "categoria": prod.categoria,
        "precio": prod.precio,
        "stock": prod.stock,
    }
    if isinstance(prod, ProductoTecnologico):
        datos["tipo"] = "tecnologico"
        datos["garantia_meses"] = prod.garantia_meses
    else:
        datos["tipo"] = "accesorio"
        datos["tipo_conexion"] = prod.tipo_conexion
    return datos


def dict_a_producto(d: dict):
    if d["tipo"] == "tecnologico":
        return ProductoTecnologico(d["codigo"], d["nombre"], d["categoria"], d["precio"], d["stock"], d["garantia_meses"])
    return ProductoAccesorio(d["codigo"], d["nombre"], d["categoria"], d["precio"], d["stock"], d["tipo_conexion"])


def cargar_inventario() -> Inventario:
    inventario = Inventario()
    for d in session.get("productos", []):
        inventario.agregar_producto(dict_a_producto(d))
    return inventario


def guardar_inventario(inventario: Inventario):
    session["productos"] = [producto_a_dict(p) for p in inventario.obtener_todos()]


# ==========================================
# Rutas
# ==========================================
@app.route("/")
def inicio():
    inventario = cargar_inventario()
    busqueda = request.args.get("codigo", "").strip()
    orden = request.args.get("orden", "")

    if busqueda:
        hallado = inventario.buscar_por_codigo(busqueda)
        productos = [hallado] if hallado else []
        if not hallado:
            flash(f"No se encontró ningún producto con el código '{busqueda}'.", "error")
    elif orden == "desc":
        productos = inventario.ordenar_por_precio(descendente=True)
    elif orden == "asc":
        productos = inventario.ordenar_por_precio(descendente=False)
    else:
        productos = inventario.obtener_todos()

    siguiente_codigo = next(generador_codigos("TEC", len(inventario.obtener_todos()) + 1))

    return render_template(
        "index.html",
        productos=productos,
        total_items=len(inventario.obtener_todos()),
        valor_total=inventario.calcular_valor_total(),
        precio_promedio=inventario.calcular_precio_promedio(),
        categorias=CATEGORIAS_PERMITIDAS,
        siguiente_codigo=siguiente_codigo,
        busqueda=busqueda,
        orden=orden,
        es_tecnologico=lambda p: isinstance(p, ProductoTecnologico),
    )


@app.route("/agregar", methods=["POST"])
def agregar():
    inventario = cargar_inventario()
    tipo = request.form.get("tipo", "tecnologico")
    try:
        nombre = validar_texto_web(request.form.get("nombre"), "Nombre")
        categoria = validar_categoria_web(request.form.get("categoria"))
        precio = validar_numero_positivo_web(request.form.get("precio"), "Precio", float)
        stock = validar_numero_positivo_web(request.form.get("stock"), "Stock inicial", int)

        codigo = next(generador_codigos("TEC", len(inventario.obtener_todos()) + 1))

        if tipo == "tecnologico":
            garantia = validar_numero_positivo_web(request.form.get("garantia"), "Garantía (meses)", int)
            prod = ProductoTecnologico(codigo, nombre, categoria, precio, stock, garantia)
        else:
            conexion = validar_texto_web(request.form.get("conexion"), "Tipo de conexión")
            prod = ProductoAccesorio(codigo, nombre, categoria, precio, stock, conexion)
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for("inicio"))

    inventario.agregar_producto(prod)
    guardar_inventario(inventario)
    flash(f"Producto {prod.codigo} agregado correctamente.", "ok")
    return redirect(url_for("inicio"))


@app.route("/reporte")
def reporte():
    ruta = generar_reporte_txt(cargar_inventario())
    return send_file(os.path.abspath(ruta), as_attachment=True, download_name=os.path.basename(ruta), mimetype="text/plain")


@app.route("/vaciar", methods=["POST"])
def vaciar():
    session.pop("productos", None)
    flash("Inventario vaciado.", "ok")
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    # Para probar en tu PC:  python api/index.py  ->  http://127.0.0.1:5000
    app.run(debug=True)
