from abc import ABC
from datetime import datetime
import os
import platform

# Intentar importar colorama si está instalada, de lo contrario usar fallbacks vacíos
try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
    COLOR_CYAN = Fore.CYAN + Style.BRIGHT
    COLOR_YELLOW = Fore.YELLOW
    COLOR_GREEN = Fore.GREEN
    COLOR_RED = Fore.RED
    COLOR_RESET = Style.RESET_ALL
except ImportError:
    COLOR_CYAN = ""
    COLOR_YELLOW = ""
    COLOR_GREEN = ""
    COLOR_RED = ""
    COLOR_RESET = ""

# ==========================================
# CONSTANTES Y CONFIGURACIÓN
# ==========================================
CATEGORIAS_PERMITIDAS = ("LAPTOP", "ACCESORIO", "RED", "ALMACENAMIENTO")
CARPETA_REPORTES = "archivos_generados"


# ==========================================
# UTILIDADES Y VALIDACIONES
# ==========================================
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
        print(f"{COLOR_RED} Error: El campo no puede estar vacío. Intente de nuevo.{COLOR_RESET}")

def validar_numero_positivo(mensaje: str, tipo=float):
    while True:
        try:
            valor = tipo(input(mensaje).strip())
            if valor < 0:
                print(f"{COLOR_RED} Error: Debe ingresar un valor numérico mayor o igual a 0.{COLOR_RESET}")
                continue
            return valor
        except ValueError:
            print(f"{COLOR_RED} Error de entrada: Ingrese un número válido ({tipo.__name__}).{COLOR_RESET}")

def validar_categoria(mensaje: str) -> str:
    while True:
        cat = input(mensaje).strip().upper()
        if cat in CATEGORIAS_PERMITIDAS:
            return cat
        print(f"{COLOR_RED} Categoría no válida. Opciones permitidas: {', '.join(CATEGORIAS_PERMITIDAS)}{COLOR_RESET}")

def generador_codigos(prefijo: str = "TEC", inicio: int = 1):
    correlativo = inicio
    while True:
        yield f"{prefijo}{correlativo:03d}"
        correlativo += 1


# ==========================================
# CLASES DE DOMINIO (POO)
# ==========================================
class Producto(ABC):
    def __init__(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int):
        self._codigo = codigo
        self._nombre = nombre.strip().title()
        self._categoria = categoria.strip().upper()
        self._precio = float(precio)
        self._stock = int(stock)

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def categoria(self) -> str:
        return self._categoria

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, nuevo_precio: float):
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = nuevo_precio

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, nuevo_stock: int):
        if nuevo_stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._stock = nuevo_stock

    def __str__(self) -> str:
        return f"[{self._codigo}] {self._nombre} | Cat: {self._categoria} | Precio: S/ {self._precio:.2f} | Stock: {self._stock}"


class ProductoTecnologico(Producto):
    def __init__(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int, garantia_meses: int):
        super().__init__(codigo, nombre, categoria, precio, stock)
        self._garantia_meses = int(garantia_meses)

    @property
    def garantia_meses(self) -> int:
        return self._garantia_meses

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | Garantía: {self._garantia_meses} meses"


class ProductoAccesorio(Producto):
    def __init__(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int, tipo_conexion: str):
        super().__init__(codigo, nombre, categoria, precio, stock)
        self._tipo_conexion = tipo_conexion.strip().capitalize()

    @property
    def tipo_conexion(self) -> str:
        return self._tipo_conexion

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | Conexión: {self._tipo_conexion}"


class Inventario:
    def __init__(self):
        self._productos = []

    def agregar_producto(self, producto: Producto):
        self._productos.append(producto)

    def buscar_por_codigo(self, codigo: str) -> Producto | None:
        codigo_clean = codigo.strip().upper()
        for prod in self._productos:
            if prod.codigo == codigo_clean:
                return prod
        return None

    def obtener_todos(self) -> list:
        return self._productos

    def ordenar_por_precio(self, descendente: bool = False) -> list:
        return sorted(self._productos, key=lambda p: p.precio, reverse=descendente)

    def calcular_valor_total(self) -> float:
        return sum(prod.precio * prod.stock for prod in self._productos)

    def calcular_precio_promedio(self) -> float:
        if not self._productos:
            return 0.0
        return sum(prod.precio for prod in self._productos) / len(self._productos)


# ==========================================
# GESTIÓN DE REPORTES
# ==========================================
def generar_reporte_txt(inventario: Inventario) -> str:
    os.makedirs(CARPETA_REPORTES, exist_ok=True)
    
    fecha_hora_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"reporte_inventario_{fecha_hora_str}.txt"
    ruta_completa = os.path.join(CARPETA_REPORTES, nombre_archivo)
    
    encabezado_fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    productos = inventario.obtener_todos()
    valor_total = inventario.calcular_valor_total()
    precio_promedio = inventario.calcular_precio_promedio()

    with open(ruta_completa, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("         SISTEMA DE GESTIÓN DE INVENTARIO - REPORTE\n")
        f.write(f" Emisión: {encabezado_fecha}\n")
        f.write("=" * 60 + "\n\n")

        if not productos:
            f.write("No hay productos registrados en el inventario.\n")
        else:
            f.write("DETALLE DE PRODUCTOS:\n")
            f.write("-" * 60 + "\n")
            for prod in productos:
                f.write(f"{str(prod)}\n")
            
            f.write("\n" + "-" * 60 + "\n")
            f.write("RESUMEN DE INVENTARIO:\n")
            f.write(f" - Total de ítems registrados : {len(productos)}\n")
            f.write(f" - Valor total del stock      : S/ {valor_total:.2f}\n")
            f.write(f" - Precio promedio por unidad : S/ {precio_promedio:.2f}\n")
            f.write("=" * 60 + "\n")

    return ruta_completa


# ==========================================
# MENÚ E INTERFAZ PRINCIPAL
# ==========================================
gen_codigos = generador_codigos("TEC", 1)

def mostrar_menu():
    print(f"{COLOR_CYAN}\n=== SISTEMA MODULAR DE INVENTARIO ==={COLOR_RESET}")
    print(f"{COLOR_YELLOW}1.{COLOR_RESET} Agregar Producto Tecnológico")
    print(f"{COLOR_YELLOW}2.{COLOR_RESET} Agregar Producto Accesorio")
    print(f"{COLOR_YELLOW}3.{COLOR_RESET} Listar Todos los Productos")
    print(f"{COLOR_YELLOW}4.{COLOR_RESET} Buscar Producto por Código")
    print(f"{COLOR_YELLOW}5.{COLOR_RESET} Listar Productos Ordenados por Precio")
    print(f"{COLOR_YELLOW}6.{COLOR_RESET} Ver Resumen de Inventario (Totales y Promedio)")
    print(f"{COLOR_YELLOW}7.{COLOR_RESET} Exportar Reporte a Archivo (.txt)")
    print(f"{COLOR_YELLOW}8.{COLOR_RESET} Salir")
    print(f"{COLOR_CYAN}======================================={COLOR_RESET}")

def main():
    inventario = Inventario()
    
    while True:
        mostrar_menu()
        opcion = input(f"{COLOR_GREEN}Seleccione una opción (1-8): {COLOR_RESET}").strip()
        
        if opcion == "1":
            limpiar_pantalla()
            print(f"{COLOR_CYAN}--- REGISTRO DE PRODUCTO TECNOLÓGICO ---{COLOR_RESET}")
            codigo = next(gen_codigos)
            print(f"Código asignado automáticamente: {COLOR_YELLOW}{codigo}{COLOR_RESET}")
            nombre = sanitizar_texto("Nombre del producto: ")
            categoria = validar_categoria("Categoría (LAPTOP/ACCESORIO/RED/ALMACENAMIENTO): ")
            precio = validar_numero_positivo("Precio: ", float)
            stock = validar_numero_positivo("Stock inicial: ", int)
            garantia = validar_numero_positivo("Garantía (meses): ", int)
            
            prod = ProductoTecnologico(codigo, nombre, categoria, precio, stock, garantia)
            inventario.agregar_producto(prod)
            print(f"{COLOR_GREEN}\n Producto tecnológico agregado correctamente.{COLOR_RESET}")

        elif opcion == "2":
            limpiar_pantalla()
            print(f"{COLOR_CYAN}--- REGISTRO DE PRODUCTO ACCESORIO ---{COLOR_RESET}")
            codigo = next(gen_codigos)
            print(f"Código asignado automáticamente: {COLOR_YELLOW}{codigo}{COLOR_RESET}")
            nombre = sanitizar_texto("Nombre del accesorio: ")
            categoria = validar_categoria("Categoría (LAPTOP/ACCESORIO/RED/ALMACENAMIENTO): ")
            precio = validar_numero_positivo("Precio: ", float)
            stock = validar_numero_positivo("Stock inicial: ", int)
            conexion = sanitizar_texto("Tipo de conexión (Inalámbrica/Cableada/USB-C): ")
            
            prod = ProductoAccesorio(codigo, nombre, categoria, precio, stock, conexion)
            inventario.agregar_producto(prod)
            print(f"{COLOR_GREEN}\n Producto accesorio agregado correctamente.{COLOR_RESET}")

        elif opcion == "3":
            limpiar_pantalla()
            print(f"{COLOR_CYAN}--- LISTADO GENERAL DE PRODUCTOS ---{COLOR_RESET}")
            productos = inventario.obtener_todos()
            if not productos:
                print(f"{COLOR_RED}El inventario está vacío.{COLOR_RESET}")
            else:
                for p in productos:
                    print(p)

        elif opcion == "4":
            limpiar_pantalla()
            print(f"{COLOR_CYAN}--- BÚSQUEDA DE PRODUCTO ---{COLOR_RESET}")
            cod_busqueda = input("Ingrese el código del producto (ej. TEC001): ")
            hallado = inventario.buscar_por_codigo(cod_busqueda)
            if hallado:
                print(f"{COLOR_GREEN}\nEncontrado: {hallado}{COLOR_RESET}")
            else:
                print(f"{COLOR_RED}\nNo se encontró ningún producto con el código '{cod_busqueda}'.{COLOR_RESET}")

        elif opcion == "5":
            limpiar_pantalla()
            print(f"{COLOR_CYAN}--- PRODUCTOS ORDENADOS POR PRECIO ---{COLOR_RESET}")
            productos_ordenados = inventario.ordenar_por_precio(descendente=True)
            if not productos_ordenados:
                print(f"{COLOR_RED}El inventario está vacío.{COLOR_RESET}")
            else:
                for p in productos_ordenados:
                    print(p)

        elif opcion == "6":
            limpiar_pantalla()
            print(f"{COLOR_CYAN}--- RESUMEN DE INVENTARIO ---{COLOR_RESET}")
            productos = inventario.obtener_todos()
            print(f"Total de ítems diferentes : {len(productos)}")
            print(f"Valor total acumulado     : S/ {inventario.calcular_valor_total():.2f}")
            print(f"Precio promedio por ítem  : S/ {inventario.calcular_precio_promedio():.2f}")

        elif opcion == "7":
            limpiar_pantalla()
            print(f"{COLOR_CYAN}--- GENERACIÓN DE REPORTE ---{COLOR_RESET}")
            ruta = generar_reporte_txt(inventario)
            print(f"{COLOR_GREEN} Reporte generado exitosamente en:\n {ruta}{COLOR_RESET}")

        elif opcion == "8":
            print(f"{COLOR_CYAN}\nSaliendo del sistema...{COLOR_RESET}")
            break

        else:
            print(f"{COLOR_RED}Opción inválida. Ingrese un número de 1 a 8.{COLOR_RESET}")

if __name__ == "__main__":
    main()