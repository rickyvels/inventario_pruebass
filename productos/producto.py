from abc import ABC

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
    