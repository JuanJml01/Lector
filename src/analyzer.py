"""
Provides code analysis functionalities.
"""

import ast
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CodeAnalyzer:
    """
    Abstract base class for code analyzers.
    """

    def __init__(self):
        pass


class PythonAnalyzer(CodeAnalyzer):
    """
    Python code analyzer.

    This analyzer receives Python source code and extracts key information
    from each defined function, including:

    - lineaInicio: The line number where the function definition begins.
    - lineaFinal: The line number where the function definition ends.
    - lista_parametros: A list of text strings, where each string represents
      a function parameter in the format "parameter_name (data type)".
      If the function has no parameters, the list should be empty.
    - tipoReturn: A text string indicating the data type that the function returns.
      If a return type is not explicitly specified, it should be inferred or set
      to "None" by default.

    Args:
        source_code (str): The Python source code to analyze.

    Returns:
        dict: A dictionary with the specified structure, containing the
              information of the functions found.

    Raises:
        SyntaxError: If the source code contains syntax errors.
        Exception: If an unexpected error occurs during analysis.
    """

    def analyze(self, source_code: str) -> dict:
        try:
            module = ast.parse(source_code)
            functions_data = []

            for node in ast.walk(module):
                if isinstance(node, ast.FunctionDef):
                    function_name = node.name
                    start_line = node.lineno
                    end_line = node.end_lineno

                    params = []
                    for arg in node.args.args:
                        param_name = arg.arg
                        param_type = 'unknown'
                        if arg.annotation:
                            param_type = ast.unparse(arg.annotation)
                        else:
                            # Try to get type from docstring
                            docstring = ast.get_docstring(node)
                            if docstring:
                                param_pattern = re.compile(f":param {param_name}:\\s*([^\\s]+)")
                                match = param_pattern.search(docstring)
                                if match:
                                    param_type = match.group(1)
                    params.append(f'{param_name} ({param_type})')

                    return_type = 'None'
                    if node.returns:
                        return_type = ast.unparse(node.returns)

                    function_info = {
                        "nombre": function_name,
                        "linea_inicio": start_line,
                        "linea_fin": end_line,
                        "parametros": params,
                        "tipo_retorno": return_type,
                    }
                    functions_data.append(function_info)
            return {"NombreArchivo": functions_data}
        except SyntaxError as e:
            logger.error(f"SyntaxError: {e}")
            return {"NombreArchivo": []}
        except Exception as e:
            logger.exception("An unexpected error occurred during analysis.")
            return {"NombreArchivo": []}


class JavaScriptAnalyzer(CodeAnalyzer):
    """
    Analizador de código JavaScript.

    Este analizador recibe código fuente en JavaScript y extrae información
    clave de cada función definida. Debido a la naturaleza dinámica de JavaScript,
    la inferencia de tipos es limitada.

    Args:
        source_code (str): El código fuente en JavaScript a analizar.

    Returns:
        dict: Un diccionario con la estructura especificada, conteniendo la
              información de las funciones encontradas. Los tipos de retorno
              y parámetros serán generalmente 'unknown' debido a la dificultad
              de inferencia estática en JavaScript.
    """

    def analyze(self, source_code: str) -> dict:
        # Placeholder implementation - JavaScript analysis is complex and
        # requires a full JavaScript parser. This is just a stub.
        logger.warning("JavaScript analysis is not fully implemented.")
        return {"NombreArchivo": []}


def analizar_codigo(source_code: str, language: str) -> dict:
    """
    Analiza el código fuente en el lenguaje especificado y retorna un diccionario
    con información detallada sobre las clases y funciones encontradas.

    Args:
        source_code (str): El código fuente a analizar.
        language (str): El lenguaje de programación del código fuente (e.g., "python", "javascript").

    Returns:
        dict: Un diccionario con la estructura:
              {
                  "funciones": [
                      {
                          "nombre": str,
                          "linea_inicio": int,
                          "linea_fin": int,
                          "parametros": list[str],  # ["nombre_parametro (tipo de dato)"]
                          "tipo_retorno": str
                      }
                  ],
                  "clases": [
                      {
                          "nombre": str,
                          "metodos": list[dict],  # [{"nombre": str, "args": list[str]}]
                          "atributos": list[str],
                          "bases": list[str]
                      }
                  ]
              }
              Si no se encuentran funciones o clases, o si el lenguaje no es soportado,
              retorna un diccionario con listas vacías para "funciones" y "clases".

    Ejemplo:
        >>> codigo_fuente = '''
        ... def mi_funcion(a: int, b: str) -> bool:
        ...     return True
        ...
        ... class MiClase:
        ...     def __init__(self, x):
        ...         self.x = x
        ...     def mi_metodo(self):
        ...         return self.x
        ... '''
        >>> resultado = analizar_codigo(codigo_fuente, "python")
        >>> print(resultado)
        {
            'funciones': [
                {
                    'nombre': 'mi_funcion',
                    'linea_inicio': 2,
                    'linea_fin': 3,
                    'parametros': ['a (int)', 'b (str)'],
                    'tipo_retorno': 'bool'
                }
            ],
            'clases': [
                {
                    'nombre': 'MiClase',
                    'metodos': [
                        {'nombre': '__init__', 'args': ['self', 'x']},
                        {'nombre': 'mi_metodo', 'args': ['self']}
                    ],
                    'atributos': ['x'],
                    'bases': []
                }
            ]
        }
    """
    try:
        module = ast.parse(source_code)
        functions_data = []
        classes_data = []

        for node in ast.walk(module):
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                start_line = node.lineno
                end_line = node.end_lineno

                params = []
                for arg in node.args.args:
                    param_name = arg.arg
                    param_type = 'unknown'
                    if arg.annotation:
                        param_type = ast.unparse(arg.annotation)
                    else:
                        # Try to get type from docstring
                        docstring = ast.get_docstring(node)
                        if docstring:
                            param_pattern = re.compile(f":param {param_name}:\\s*([^\\s]+)")
                            match = param_pattern.search(docstring)
                            if match:
                                param_type = match.group(1)
                    params.append(f'{param_name} ({param_type})')

                return_type = 'None'
                if node.returns:
                    return_type = ast.unparse(node.returns)

                function_info = {
                    "nombre": function_name,
                    "linea_inicio": start_line,
                    "linea_fin": end_line,
                    "parametros": params,
                    "tipo_retorno": return_type,
                }
                functions_data.append(function_info)

            elif isinstance(node, ast.ClassDef):
                class_name = node.name
                methods = []
                attributes = []
                bases = [base.id for base in node.bases if hasattr(base, 'id')]

                for body_node in node.body:
                    if isinstance(body_node, ast.FunctionDef):
                        method_name = body_node.name
                        method_args = [arg.arg for arg in body_node.args.args]
                        methods.append({"nombre": method_name, "args": method_args})
                    elif isinstance(body_node, ast.Assign):
                        for target in body_node.targets:
                            if isinstance(target, ast.Name):
                                attributes.append(target.id)

                class_info = {
                    "nombre": class_name,
                    "metodos": methods,
                    "atributos": attributes,
                    "bases": bases,
                }
                classes_data.append(class_info)

        return {"funciones": functions_data, "clases": classes_data}
    except SyntaxError as e:
        logger.error(f"SyntaxError: {e}")
        return {"funciones": [], "clases": []}
    except Exception as e:
        logger.exception("An unexpected error occurred.")
        return {"funciones": [], "clases": []}


if __name__ == '__main__':
    # Example usage
    python_code = """
def mi_funcion(a: int, b: str) -> bool:
    return True

class MiClase:
    def __init__(self, x):
        self.x = x
    def mi_metodo(self):
        return self.x
"""
    analysis_result = analizar_codigo(python_code, "python")
    print(analysis_result)
