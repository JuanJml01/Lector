z# Lector
For Gemini documentation

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Functions

### analyzer.py

*   `CodeAnalyzer.analyze(source_code: str) -> dict`: Analyzes the given source code and returns a dictionary containing information about the functions found. This is an abstract method that subclasses should implement.
*   `PythonAnalyzer.analyze(source_code: str) -> dict`: Analyzes Python source code and extracts information about functions, including start line, end line, parameters (with unknown types), and return type. Returns a dictionary containing the analysis results.
*   `analizar_codigo_fuente(source_code: str, language: str) -> dict`: Analyzes source code in the specified language (Python or JavaScript) and returns a dictionary with information about the functions found. It uses `PythonAnalyzer` for Python code and `JavaScriptAnalyzer` for JavaScript code.

### src/file_manager.py

*   `File.__init__(self, path: str)`: Constructor for the `File` class. Takes the file path as input, reads the file content, and initializes the object's attributes. Raises `FileNotFoundError` if the file doesn't exist and `IOError` if there's an error reading the file.
*   `File.borrar_contenido(self)`: Deletes the content of the file, both on disk and in the `contenido` attribute. Raises `IOError` if there's an error writing to the file.
*   `File.actualizar_contenido(self, linea_inicial: int = None, linea_final: int = None)`: Updates a specific range of lines within the file. It takes the starting and ending line numbers as input. Raises `IOError` if there's an error writing to the file. It also takes user input for the new content for each line.
*   `File.reescribir_contenido(self, nuevo_contenido: str)`: Rewrites the entire content of the file, both on disk and in the `contenido` attribute. It takes the new content as input. Raises `IOError` if there's an error writing to the file.
