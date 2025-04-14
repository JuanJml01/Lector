"""Modulo principal"""
import manager_files
# import llm_api
from code_analysis import analizar_funciones

if __name__ == '__main__':
    nice = manager_files.read_file_range('src/manager_files.py')
    resutl = analizar_funciones(nice,'manager_files.py')
    manager_files.borrar_contenido_archivo_json('toy.json')

    print(resutl)
