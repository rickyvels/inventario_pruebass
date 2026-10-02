def generador_codigos(prefijo: str = "TEC", inicio: int = 1):
    correlativo = inicio
    while True:
        yield f"{prefijo}{correlativo:03d}"
        correlativo += 1
