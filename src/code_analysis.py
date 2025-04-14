import ast
import json
from typing import Any, Dict, List, Optional


def analizar_funciones(contenido: str, nombre_archivo: str = "codigo_fuente.py") -> Dict[str, List[Dict[str, Any]]]:
    """
    Analiza el contenido de un archivo de código fuente en Python y extrae los metadatos de las funciones definidas.
    
    Esta función procesa el código fuente utilizando el módulo `ast` para identificar las funciones declaradas
    y obtener la siguiente información para cada función:
      - Línea de inicio de la función (lineaInicio)
      - Línea final de la función (lineafinal)
      - Lista de parámetros con su anotación de tipo (lista_parametos)
      - Tipo de retorno anotado (TipoReturn)
    
    Args:
        contenido (str): Texto completo del archivo de código fuente a analizar.
        nombre_archivo (str, optional): Nombre del archivo analizado. Default: "codigo_fuente.py".
    
    Returns:
        Dict[str, List[Dict[str, Any]]]: Estructura JSON con los metadatos de las funciones, con el siguiente formato:
            {
                "NombreArchivo": [
                    {
                        "Nombre_funcion": {
                            "lineaInicio": "línea de inicio",
                            "lineafinal": "línea final",
                            "lista_parametos": [
                              "parametro(tipo de dato)"
                            ],
                            "TipoReturn": "Tipo de dato que retorna"
                        }
                    }
                ]
            }
    
    Raises:
        SyntaxError: Si el contenido no es un código Python válido.
    
    Ejemplo de uso:
        codigo = '''
        def ejemplo(param1: int, param2: str) -> bool:
            # Implementación
            return True
        '''
        
        resultado = analizar_funciones(codigo)
        print(json.dumps(resultado, indent=4, ensure_ascii=False))
    """

    def obtener_anotacion(anotacion: Optional[ast.expr]) -> str:
        """
        Convierte una anotación de tipo de AST a su representación en forma de cadena.
        
        Args:
            anotacion (ast.expr, opcional): Nodo de anotación en el árbol AST.
        
        Returns:
            str: Representación en cadena del tipo anotado o 'Any' si no existe.
        """
        if anotacion is None:
            return "Any"
        # Se utiliza ast.unparse (disponible desde Python 3.9) para convertir el nodo a cadena
        try:
            return ast.unparse(anotacion)
        except Exception:
            return "Any"

    # Parsear el contenido para obtener el árbol de sintaxis abstracta
    try:
        tree = ast.parse(contenido)
    except SyntaxError as e:
        raise SyntaxError("El contenido proporcionado no es un código Python válido.") from e

    funciones_info = []

    # Recorrer el árbol de sintaxis para encontrar declaraciones de funciones
    for nodo in ast.walk(tree):
        if isinstance(nodo, ast.FunctionDef):
            # Línea de inicio de la función
            linea_inicio = nodo.lineno

            # Línea final de la función.
            # Desde Python 3.8, se puede acceder a `end_lineno` si está disponible.
            linea_final = getattr(nodo, 'end_lineno', linea_inicio)

            # Procesar los parámetros
            lista_parametos = []
            for arg in nodo.args.args:
                # Obtener el nombre del parámetro
                nombre_param = arg.arg
                # Obtener la anotación si existe
                tipo_param = obtener_anotacion(arg.annotation)
                lista_parametos.append(f"{nombre_param}({tipo_param})")

            # Procesar el tipo de retorno
            tipo_retorno = obtener_anotacion(nodo.returns)

            # Construir el diccionario con la información de la función
            info_funcion = {
                nodo.name: {
                    "lineaInicio": linea_inicio,
                    "lineafinal": linea_final,
                    "lista_parametos": lista_parametos,
                    "TipoReturn": tipo_retorno
                }
            }

            funciones_info.append(info_funcion)

    # Construir la estructura final según el formato solicitado
    resultado = {nombre_archivo: funciones_info}

    return resultado

# Ejemplo de uso
# if __name__ == "__main__":
#     # Código de ejemplo para probar la función
#     codigo = '''
# def ejemplo(param1: int, param2: str) -> bool:
#     # Implementación
#     return True
#
# def sin_anotacion(param):
#     return param
# '''
#     resultado = analizar_funciones(codigo, "ejemplo.py")
#     print(json.dumps(resultado, indent=4, ensure_ascii=False))
#
