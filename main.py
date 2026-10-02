from productos.producto import Inventario, ProductoTecnologico, ProductoAccesorio
from utilidades.validaciones import limpiar_pantalla, sanitizar_texto, validar_numero_positivo, validar_categoria
from utilidades.generadores import generador_codigos
from reportes.gestor_reportes import generar_reporte_txt

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