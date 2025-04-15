# Documentación de las funciones en el directorio `src/`

## Tabla de Contenidos
1.  [get\_api\_key](#get_api_key)
2.  [LLMConfig](#llmconfig)
3.  [llm\_request](#llm_request)
4.  [CodeAnalyzer](#codeanalyzer)
5.  [PythonAnalyzer](#pythonanalyzer)
6.  [JavaScriptAnalyzer](#javascriptanalyzer)
7.  [analizar\_codigo](#analizar_codigo)

## Funciones

### 1. get\_api\_key

#### Propósito
Recupera la API key de la variable de entorno `GEMINI_API_KEY`.

#### Parámetros
Ninguno

#### Valores de Retorno
*   `str`: La API key.

#### Posibles errores
*   `ValueError`: Si la variable de entorno no está definida o la API key no es válida.

#### Ejemplo de uso
```python
api_key = get_api_key()
print(api_key)
```

### 2. LLMConfig

#### Propósito
Clase para encapsular las opciones de configuración de la API LLM.

#### Parámetros
*   `model` (`str`, opcional): El modelo a utilizar. Por defecto es `"gemini-2.0-flash"`.
*   `generation_config` (`dict`, opcional): Configuración para la generación. Por defecto es `None`.
*   `system_instruction` (`dict`, opcional): Instrucciones para el sistema. Por defecto es `None`.
*   `response_schema` (`dict`, opcional): Esquema JSON para la respuesta. Por defecto es `None`.

#### Métodos
*   `__init__(self, model: str = "gemini-2.0-flash", generation_config: dict = None, system_instruction: dict = None, response_schema: dict = None)`: Inicializa una instancia de `LLMConfig`.
*   `validate_model(self)`: Valida el modelo.

#### Posibles errores
*   `ValueError`: Si el modelo no es válido.

#### Ejemplo de uso
```python
config = LLMConfig(model="gemini-2.0-flash")
```

### 3. llm\_request

#### Propósito
Estructura de función para interactuar con una API LLM.

#### Parámetros
*   `prompt` (`str`): El prompt principal para la API LLM.
*   `config` (`LLMConfig`, opcional): Un objeto de configuración opcional. Por defecto es `None`. Permite especificar opciones avanzadas como `generationConfig`, `systemInstruction` y `model`.

#### Valores de Retorno
*   `str`: La respuesta del servidor como una cadena JSON con el formato `{"response": "answer"}`.

#### Posibles errores
*   `requests.exceptions.RequestException`: Si hay un error al realizar la solicitud.
*   `ValueError`: Si hay un error de validación.

#### Ejemplo de uso
```python
from src.gemini_api import llm_request, LLMConfig

prompt = "Escribe un poema corto sobre la primavera."
config = LLMConfig(model="gemini-2.0-flash")
response = llm_request(prompt, config)
print(response)
```

### 4. CodeAnalyzer

#### Propósito
Clase base abstracta para analizadores de código.

#### Parámetros
Ninguno

#### Métodos
*   `__init__(self)`: Inicializa una instancia de `CodeAnalyzer`.

#### Ejemplo de uso
```python
analyzer = CodeAnalyzer()
```

### 5. PythonAnalyzer

#### Propósito
Analizador de código Python.

#### Parámetros
*   `source_code` (`str`): El código fuente en Python a analizar.

#### Métodos
*   `analyze(self, source_code: str) -> dict`: Analiza el código fuente y retorna un diccionario con información sobre las funciones encontradas.

#### Valores de Retorno
*   `dict`: Un diccionario con la estructura especificada, conteniendo la información de las funciones encontradas.

#### Posibles errores
*   `SyntaxError`: Si el código fuente contiene errores de sintaxis.
*   `Exception`: Si ocurre un error inesperado durante el análisis.

#### Ejemplo de uso
```python
analyzer = PythonAnalyzer()
source_code = "def mi_funcion(): return 1"
result = analyzer.analyze(source_code)
print(result)
```

### 6. JavaScriptAnalyzer

#### Propósito
Analizador de código JavaScript.

#### Parámetros
*   `source_code` (`str`): El código fuente en JavaScript a analizar.

#### Métodos
*   `analyze(self, source_code: str) -> dict`: Analiza el código fuente y retorna un diccionario con información sobre las funciones encontradas.

#### Valores de Retorno
*   `dict`: Un diccionario con la estructura especificada, conteniendo la información de las funciones encontradas.

#### Ejemplo de uso
```python
analyzer = JavaScriptAnalyzer()
source_code = "function miFuncion() { return 1; }"
result = analyzer.analyze(source_code)
print(result)
```

### 7. analizar\_codigo

#### Propósito
Analiza el código fuente en el lenguaje especificado y retorna un diccionario con información detallada sobre las clases y funciones encontradas.

#### Parámetros
*   `source_code` (`str`): El código fuente a analizar.
*   `language` (`str`): El lenguaje de programación del código fuente (e.g., "python", "javascript").

#### Valores de Retorno
*   `dict`: Un diccionario con la estructura:
    ```
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
    ```
    
    ### 8. File
    
    #### Propósito
    Clase para representar y manipular archivos en un entorno profesional.
    
    #### Atributos
    *   `nombre` (`str`): El nombre del archivo.
    *   `path` (`str`): La ruta absoluta del archivo.
    *   `extension` (`str`): La extensión del archivo.
    *   `metadatos` (`dict`, opcional): Un diccionario para almacenar metadatos adicionales del archivo. Por defecto, un diccionario vacío.
    *   `oculto` (`bool`): Un indicador de si el archivo está oculto.
    *   `contenido` (`str`): Una cadena que representa el contenido actual del archivo, cargado al instanciar la clase.
    
    #### Métodos
    *   `__init__(self, path: str)`: Constructor de la clase `File`.
        *   `path` (`str`): La ruta al archivo.
        *   Raises:
            *   `FileNotFoundError`: Si el archivo no existe.
            *   `IOError`: Si ocurre un error al leer el archivo.
    *   `borrar_contenido(self)`: Borra el contenido del archivo tanto en el disco como en el atributo 'contenido'.
        *   Raises:
            *   `IOError`: Si ocurre un error al escribir en el archivo.
    *   `actualizar_contenido(self, linea_inicial: int = None, linea_final: int = None)`: Actualiza un rango específico de líneas dentro del archivo.
        *   `linea_inicial` (`int`, optional): La línea inicial para actualizar (1-indexado). Si es `None` o <= 0, comienza desde la primera línea. Si excede el número total de líneas, el cursor se mueve a la última línea y se ignora `linea_final`.
        *   `linea_final` (`int`, optional): La línea final para actualizar (1-indexado). Si es `None` o excede el número total de líneas, se trata como la última línea. Si ambos son `None`, se actualiza todo el contenido.
        *   Raises:
            *   `IOError`: Si ocurre un error al escribir en el archivo.
    *   `reescribir_contenido(self, nuevo_contenido: str)`: Reescribe el contenido completo del archivo tanto en el disco como en el atributo 'contenido'.
        *   `nuevo_contenido` (`str`): El nuevo contenido para el archivo.
        *   Raises:
            *   `IOError`: Si ocurre un error al escribir en el archivo.
    
    #### Ejemplo de uso
    ```python
    from src.file_manager import File
    
    try:
        archivo = File("mi_archivo.txt")
        print(archivo.contenido)
        archivo.reescribir_contenido("Nuevo contenido")
        print(archivo.contenido)
    except FileNotFoundError as e:
        print(e)
    except IOError as e:
        print(e)
    ```
    Si no se encuentran funciones o clases, o si el lenguaje no es soportado, retorna un diccionario con listas vacías para "funciones" y "clases".

#### Ejemplo de uso
```python
codigo_fuente = """
def mi_funcion(a: int, b: str) -> bool:
    return True

class MiClase:
    def __init__(self, x):
        self.x = x
    def mi_metodo(self):
        return self.x
"""
resultado = analizar_codigo(codigo_fuente, "python")
print(resultado)
```
