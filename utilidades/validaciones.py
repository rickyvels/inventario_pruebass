import os
import platform

CATEGORIAS_PERMITIDAS = ("LAPTOP", "ACCESORIO", "RED", "ALMACENAMIENTO")

def limpiar_pantalla():
    sistema = platform.system().lower()
    if "windows" in sistema:
        os.system("cls")
    else:
        os.system("clear")

def sanitizar_texto(mensaje: str) -> str:
    while True:
        entrada = input(mensaje).strip()
        if entrada:
            return entrada
        print(" Error: El campo no puede estar vacío. Intente de nuevo.")

def validar_numero_positivo(mensaje: str, tipo=float):
    while True:
        try:
            valor = tipo(input(mensaje).strip())
            if valor < 0:
                print(" Error: Debe ingresar un valor numérico mayor o igual a 0.")
                continue
            return valor
        except ValueError:
            print(f" Error de entrada: Ingrese un número válido ({tipo.__name__}).")

def validar_categoria(mensaje: str) -> str:
    while True:
        cat = input(mensaje).strip().upper()
        if cat in CATEGORIAS_PERMITIDAS:
            return cat
        print(f" Categoría no válida. Opciones permitidas: {', '.join(CATEGORIAS_PERMITIDAS)}")

# ==========================================
# Versiones sin input() para la interfaz web
# (misma regla que las de arriba, pero lanzan ValueError en vez de volver a preguntar)
# ==========================================
def validar_texto_web(valor: str, campo: str) -> str:
    entrada = (valor or "").strip()
    if not entrada:
        raise ValueError(f"El campo '{campo}' no puede estar vacío.")
    return entrada

def validar_numero_positivo_web(valor: str, campo: str, tipo=float):
    try:
        numero = tipo((valor or "").strip())
    except ValueError:
        raise ValueError(f"'{campo}' debe ser un número válido ({tipo.__name__}).")
    if numero < 0:
        raise ValueError(f"'{campo}' debe ser mayor o igual a 0.")
    return numero

def validar_categoria_web(valor: str) -> str:
    cat = (valor or "").strip().upper()
    if cat not in CATEGORIAS_PERMITIDAS:
        raise ValueError(f"Categoría no válida. Opciones permitidas: {', '.join(CATEGORIAS_PERMITIDAS)}")
    return cat
