"""Modulo donde se maneja los archivos"""

def leer_archivo(nombre_archivo: str, encoding: str = 'utf-8') -> str:
    """Lee el contenido de un archivo y lo retorna como una cadena de texto.

    Abre el archivo en modo lectura utilizando un manejador de contexto para garantizar
    su correcto cierre, independientemente de si ocurren errores durante la operación.

    Parámetros
    ----------
    nombre_archivo : str
        Ruta completa o relativa del archivo a leer.
    encoding : str, opcional
    Codificación utilizada para decodificar el archivo (por defecto: 'utf-8').

    Retorna
    -------
    str
        Contenido completo del archivo como cadena de texto.

    Excepciones
    -----------
    FileNotFoundError
        Si el archivo no existe en la ruta especificada.
    PermissionError
        Si no se tienen permisos suficientes para acceder al archivo.
    UnicodeDecodeError
        Si ocurre un error de decodificación con el encoding especificado.

    Ejemplos
    --------
    >>> leer_archivo('documento.txt')
    'Contenido del archivo...'

    >>> leer_archivo('datos.csv', encoding='latin-1')
    'Contenido,del,archivo...'
    """

    # Manejador de contexto asegura el cierre correcto del archivo
    with open(nombre_archivo, mode='r', encoding=encoding) as archivo:
        # Lee todo el contenido del archivo en una sola operación
        contenido = archivo.read()
    return contenido
