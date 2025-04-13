"""Modulo donde se maneja los archivos"""


def read_file_range(file_path, start_line=None, end_line=None):
    """
    Lee un rango específico de líneas de un archivo y retorna su contenido como string.
    Args:
        file_path (str): Ruta completa del archivo a leer
        start_line (int, optional): Línea inicial (1-based). Default: primera línea
        end_line (int, optional): Línea final (1-based). Default: última línea
    Returns:
        str: Contenido concatenado del rango solicitado
    Raises:
        ValueError: Si los parámetros son inválidos
        FileNotFoundError: Si el archivo no existe
    """
    # Validación de parámetros
    if start_line and (not isinstance(start_line, int) or start_line < 1):
        raise ValueError("Línea inicial debe ser entero positivo")
    if end_line and (not isinstance(end_line, int) or end_line < 1):
        raise ValueError("Línea final debe ser entero positivo")
    if start_line and end_line and (start_line > end_line):
        raise ValueError("Línea inicial no puede ser mayor que final")
    # Lectura del archivo
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # Cálculo de índices (convertimos a base 0)
    start = start_line - 1 if start_line else 0
    end = end_line if end_line else len(lines)
    # Extracción y unión del contenido
    return ''.join(lines[start:end])

def modificar_archivo(path, contenido, inicio=None, fin=None):
    """
    Modifica un archivo de texto sobrescribiendo un rango específico de líneas con nuevo contenido.
    Si las líneas indicadas no existen, el contenido se inserta en la posición correspondiente.
    Parámetros:
        path (str): Ruta del archivo a modificar.
        inicio (int, opcional): Número de línea inicial (basado en 1) desde donde se sobrescribe. Por defecto es la primera línea.
        fin (int, opcional): Número de línea final (basado en 1) hasta donde se sobrescribe. Por defecto es la última línea.
        contenido (str): Texto a insertar en el rango especificado.
    Excepciones:
        ValueError: Si los valores de inicio o fin son inválidos.
        FileNotFoundError: Si el archivo especificado no existe.
    """
    # Validar parámetros de entrada
    if inicio is not None:
        if not isinstance(inicio, int):
            raise TypeError("inicio debe ser un entero")
        if inicio < 1:
            raise ValueError("inicio debe ser un número positivo mayor o igual a 1")
    if fin is not None:
        if not isinstance(fin, int):
            raise TypeError("fin debe ser un entero")
        if fin < 1:
            raise ValueError("fin debe ser un número positivo mayor o igual a 1")
    if inicio is not None and fin is not None and fin < inicio:
        raise ValueError("fin no puede ser menor que inicio")
    # Leer todas las líneas del archivo original
    try:
        with open(path, 'r', encoding="utf-8") as archivo:
            lineas_originales = archivo.readlines()
    except FileNotFoundError:
        raise
    # Calcular índices de inicio y fin (basados en 0)
    longitud_original = len(lineas_originales)
    # Determinar índice inicial
    if inicio is not None:
        indice_inicio = inicio - 1
        # Asegurar que no sea menor que 0
        if indice_inicio < 0:
            indice_inicio = 0
    else:
        indice_inicio = 0  # Por defecto: primera línea
    # Determinar índice final
    if fin is not None:
        indice_fin = fin - 1
    else:
        # Si no hay líneas, se establece 0
        indice_fin = longitud_original - 1 if longitud_original > 0 else 0

    # Asegurar que el índice final no sea menor que el inicial
    if indice_fin < indice_inicio:
        indice_fin = indice_inicio

    # Verificar si el índice inicial está fuera del rango actual del archivo
    if indice_inicio >= longitud_original:
        # Insertar el contenido al final del archivo
        lineas_nuevas = lineas_originales + contenido.splitlines(True)
    else:
        # Ajustar el índice final para que no exceda el límite del archivo
        indice_fin = min(indice_fin, longitud_original - 1)

        # Dividir las líneas en partes antes, contenido nuevo y después
        lineas_anteriores = lineas_originales[:indice_inicio]
        lineas_posteriores = lineas_originales[indice_fin + 1:]
        lineas_contenido = contenido.splitlines(True)

        # Combinar todas las partes para formar el nuevo contenido
        lineas_nuevas = lineas_anteriores + lineas_contenido + lineas_posteriores

    # Escribir las nuevas líneas al archivo
    with open(path, 'w') as archivo:
        archivo.writelines(lineas_nuevas)


def escribir_archivo(ruta: str, contenido: str) -> None:
    """
    Crea un archivo en la ubicación especificada y escribe el contenido proporcionado.

    Parámetros:
    ruta (str): Ruta donde se creará el archivo.
    contenido (str): Texto que se escribirá en el archivo.
    Esta función abre (o crea si no existe) el archivo en modo escritura y escribe el contenido.
    """
    try:
        # Abrir el archivo en modo escritura (se crea si no existe)
        with open(ruta, 'w', encoding='utf-8') as archivo:
            # Escribir el contenido en el archivo
            archivo.write(contenido)
        # Confirmación de que se escribió el archivo correctamente
        print(f"El archivo ha sido creado y se ha escrito en él: {ruta}")
    except Exception as error:
        # Manejo de errores en caso de que la escritura falle
        print(f"Ocurrió un error al escribir el archivo: {error}")
