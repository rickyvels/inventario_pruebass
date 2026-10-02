from datetime import datetime
import os

from productos.producto import Inventario

# En Vercel solo se puede escribir en /tmp; en tu PC se usa la carpeta del proyecto.
CARPETA_REPORTES = os.path.join("/tmp", "archivos_generados") if os.environ.get("VERCEL") else "archivos_generados"


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
