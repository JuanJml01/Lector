"""Modulo donde se maneja los archivos"""
import json


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


import json

import json
import os


def actualizar_archivo_json(path, nuevos_datos):
    """
    Actualiza o inserta definiciones de funciones en un archivo JSON que organiza la información
    por archivos (por ejemplo, "llm_api.py") y, para cada archivo, una lista de definiciones de funciones.

    La función procede de la siguiente forma:
      - Si el archivo JSON ya existe, se carga su contenido; de lo contrario se parte de un diccionario vacío.
      - Para cada clave en 'nuevos_datos':
          - Si la clave existe en el JSON, se recorre la lista de funciones existente y se actualiza cada
            definición que coincida con la función nueva (basada en el nombre de la función). Si la función
            no existe, se agrega a la lista.
          - Si la clave no existe, se añade al JSON con el valor proporcionado.
      - Se escribe el archivo actualizando el contenido con formato legible (indentado).

    Args:
        path (str): Ruta completa del archivo JSON a modificar.
        nuevos_datos (dict): Diccionario con la nueva información a agregar o actualizar.
            Formato esperado:
            {
                "nombre_archivo": [
                    { "nombre_funcion": { ... detalles ... } },
                    ...
                ],
                ...
            }

    Returns:
        None

    Raises:
        ValueError: Si 'nuevos_datos' no es un diccionario.
        Exception: Para errores en la lectura o escritura del archivo.
    """
    if not isinstance(nuevos_datos, dict):
        raise ValueError("El parámetro 'nuevos_datos' debe ser un diccionario.")

    # Cargar el contenido existente del archivo JSON, o iniciar con un diccionario vacío.
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf8") as archivo:
                contenido_existente = json.load(archivo)
        except Exception as e:
            raise Exception(f"Error al leer el archivo JSON existente: {e}")
    else:
        contenido_existente = {}

    # Recorrer cada clave (nombre de archivo) en los nuevos datos.
    for archivo_key, definiciones_nuevas in nuevos_datos.items():
        if not isinstance(definiciones_nuevas, list):
            raise Exception(f"El valor para la clave '{archivo_key}' debe ser una lista de definiciones.")

        # Si la clave ya existe, actualizar la lista de definiciones.
        if archivo_key in contenido_existente:
            definiciones_existentes = contenido_existente[archivo_key]
            # Validar que la estructura existente sea una lista.
            if not isinstance(definiciones_existentes, list):
                raise Exception(f"El valor asociado a la clave '{archivo_key}' no es una lista.")
            # Para cada definición nueva, actualizar o agregar en la lista existente.
            for nueva_def in definiciones_nuevas:
                if not isinstance(nueva_def, dict) or len(nueva_def) != 1:
                    raise Exception("Cada definición de función debe ser un diccionario con un único par clave-valor.")
                nombre_funcion = list(nueva_def.keys())[0]
                actualizada = False
                # Buscar si la función ya existe en la lista.
                for idx, def_existente in enumerate(definiciones_existentes):
                    if isinstance(def_existente, dict) and nombre_funcion in def_existente:
                        # Actualizar los detalles de la función existente.
                        definiciones_existentes[idx][nombre_funcion] = nueva_def[nombre_funcion]
                        actualizada = True
                        break
                # Si no se encontró, agregar la nueva definición.
                if not actualizada:
                    definiciones_existentes.append(nueva_def)
            contenido_existente[archivo_key] = definiciones_existentes
        else:
            # Si la clave no existe, agregarla completamente.
            contenido_existente[archivo_key] = definiciones_nuevas

    # Escribir el contenido actualizado de nuevo en el archivo JSON.
    try:
        with open(path, "w", encoding="utf8") as archivo:
            json.dump(contenido_existente, archivo, ensure_ascii=False, indent=4)
    except Exception as e:
        raise Exception(f"Error al escribir el archivo JSON actualizado: {e}")


# Ejemplos de uso (para pruebas o demostración)
# if __name__ == "__main__":
#     # Ejemplo 1: Actualización completa
#     try:
#         contenido_completo = {"nombre": "Juan", "edad": 30, "ocupacion": "Ingeniero"}
#         actualizar_archivo_json("datos.txt", contenido_completo)
#         print("Archivo actualizado completamente.")
#     except Exception as error:
#         print(f"Error actualizando archivo completo: {error}")
#
#     # Ejemplo 2: Modificación de un rango específico
#     try:
#         contenido_rango = {"titulo": "Actualización", "mensaje": "Este es un mensaje modificado."}
#         actualizar_archivo_json("log.txt", contenido_rango, inicio=2, fin=4)
#         print("Archivo modificado en el rango de líneas especificado.")
#     except Exception as error:
#         print(f"Error modificando el rango de líneas: {error}")
#
#     # Ejemplo 3: Caso límite con diccionario vacío
#     try:
#         actualizar_archivo_json("config.txt", {}, inicio=1, fin=2)
#         print("Archivo actualizado con diccionario vacío en el rango especificado.")
#     except Exception as error:
#         print(f"Error en caso de diccionario vacío: {error}")



def borrar_contenido_archivo_json(ruta_archivo: str) -> None:
    """
    Borra el contenido de un archivo JSON, dejando el archivo vacío.

    Parámetros:
        ruta_archivo (str): Ruta del archivo JSON a modificar.

    Notas:
        - Se sobreescribe el archivo dejando una cadena vacía.
        - Si el archivo no existe, se lanzará una excepción.
    """
    try:
        # Se abre el archivo en modo escritura, lo que borra su contenido previamente existente
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write("")
        print(f"Contenido del archivo '{ruta_archivo}' borrado exitosamente.")
    except FileNotFoundError as e:
        print(f"Error: El archivo no existe: {e}")
    except Exception as error:
        print(f"Ocurrió un error al borrar el contenido del archivo: {error}")
