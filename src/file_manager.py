"""
Este módulo proporciona funcionalidades para la gestión de archivos,
incluyendo la creación, edición, lectura, escritura, borrado,
y manipulación general de archivos y directorios.
"""

import os
import io

class File:
    """
    Clase para representar y manipular archivos en un entorno profesional.

    Atributos:
        nombre (str): El nombre del archivo.
        path (str): La ruta absoluta del archivo.
        extension (str): La extensión del archivo.
        metadatos (dict, optional): Un diccionario para almacenar metadatos adicionales del archivo.
                                     Por defecto, un diccionario vacío.
        oculto (bool): Un indicador de si el archivo está oculto.
        contenido (str): Una cadena que representa el contenido actual del archivo,
                         cargado al instanciar la clase.
    """

    def __init__(self, path: str):
        """
        Constructor de la clase File.

        Args:
            path (str): La ruta al archivo.

        Raises:
            FileNotFoundError: Si el archivo no existe.
            IOError: Si ocurre un error al leer el archivo.
        """
        try:
            if not os.path.exists(path):
                raise FileNotFoundError(f"El archivo no se encuentra en la ruta: {path}")

            self.path = os.path.abspath(path)
            self.nombre = os.path.basename(path)
            self.extension = os.path.splitext(path)[1]
            self.metadatos = os.stat(path)
            self.oculto = self.nombre.startswith('.')

            with io.open(self.path, 'r', encoding='utf-8') as f:
                self.contenido = f.read()

        except FileNotFoundError as e:
            raise e
        except Exception as e:
            raise IOError(f"Error al leer el archivo: {e}")

    def borrar_contenido(self):
        """
        Borra el contenido del archivo tanto en el disco como en el atributo 'contenido'.

        Raises:
            IOError: Si ocurre un error al escribir en el archivo.
        """
        try:
            with io.open(self.path, 'w', encoding='utf-8') as f:
                f.write("")
            self.contenido = ""
        except Exception as e:
            raise IOError(f"Error al borrar el contenido del archivo: {e}")

    def actualizar_contenido(self, linea_inicial: int = None, linea_final: int = None):
        """
        Actualiza un rango específico de líneas dentro del archivo.

        Args:
            linea_inicial (int, optional): La línea inicial para actualizar (1-indexado).
                                            Si es None o <= 0, comienza desde la primera línea.
                                            Si excede el número total de líneas, el cursor se mueve a la última línea y se ignora linea_final.
            linea_final (int, optional): La línea final para actualizar (1-indexado).
                                          Si es None o excede el número total de líneas, se trata como la última línea.
                                          Si ambos son None, se actualiza todo el contenido.

        Raises:
            IOError: Si ocurre un error al escribir en el archivo.
        """
        try:
            lineas = self.contenido.splitlines()
            total_lineas = len(lineas)

            if linea_inicial is None or linea_inicial <= 0:
                linea_inicial = 1
            elif linea_inicial > total_lineas:
                linea_inicial = total_lineas
                linea_final = None  # Ignorar linea_final si linea_inicial está fuera de rango

            if linea_final is None or linea_final > total_lineas:
                linea_final = total_lineas
            elif linea_final < linea_inicial:
                raise ValueError("linea_final debe ser mayor o igual a linea_inicial")

            # Leer el contenido del archivo
            with io.open(self.path, 'r', encoding='utf-8') as f:
                contenido_archivo = f.read()

            # Dividir el contenido en líneas
            lineas_archivo = contenido_archivo.splitlines()

            # Solicitar al usuario que ingrese el nuevo contenido para el rango de líneas especificado
            nuevo_contenido_lista = []
            for i in range(linea_inicial - 1, linea_final):
                nuevo_contenido = input(f"Ingrese el nuevo contenido para la línea {i + 1}: ")
                nuevo_contenido_lista.append(nuevo_contenido)

            # Reemplazar las líneas en el rango especificado con el nuevo contenido
            lineas_archivo[linea_inicial - 1:linea_final] = nuevo_contenido_lista

            # Unir las líneas en un solo string
            nuevo_contenido_completo = '\n'.join(lineas_archivo)

            # Escribir el nuevo contenido en el archivo
            with io.open(self.path, 'w', encoding='utf-8') as f:
                f.write(nuevo_contenido_completo)

            # Actualizar el atributo de contenido
            self.contenido = nuevo_contenido_completo

        except ValueError as e:
            raise e
        except Exception as e:
            raise IOError(f"Error al actualizar el contenido del archivo: {e}")

    def reescribir_contenido(self, nuevo_contenido: str):
        """
        Reescribe el contenido completo del archivo tanto en el disco como en el atributo 'contenido'.

        Args:
            nuevo_contenido (str): El nuevo contenido para el archivo.

        Raises:
            IOError: Si ocurre un error al escribir en el archivo.
        """
        try:
            with io.open(self.path, 'w', encoding='utf-8') as f:
                f.write(nuevo_contenido)
            self.contenido = nuevo_contenido
        except Exception as e:
            raise IOError(f"Error al reescribir el contenido del archivo: {e}")
