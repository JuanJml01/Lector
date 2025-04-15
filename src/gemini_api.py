'''Este módulo se encarga de realizar requests a la API LLM de Google Gemini.'''

import requests
import json
import os
import logging
import re

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_api_key():
    """
    Recupera la API key de la variable de entorno GEMINI_API_KEY.

    Returns:
        str: La API key.

    Raises:
        ValueError: Si la variable de entorno no está definida o la API key no es válida.
    """
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        logging.error("La variable de entorno GEMINI_API_KEY no está definida.")
        raise ValueError("La API key no está definida en el entorno.")

    # Validar el formato de la API key (ejemplo: 32 caracteres alfanuméricos)

    return api_key


class LLMConfig:
    """
    Clase para encapsular las opciones de configuración de la API LLM.
    """
    def __init__(self, model: str = "gemini-2.0-flash", generation_config: dict = None, system_instruction: dict = None, response_schema: dict = None):
        """
        Inicializa una instancia de LLMConfig.

        Args:
            model (str, optional): El modelo a utilizar. Defaults to "gemini-2.0-flash".
            generation_config (dict, optional): Configuración para la generación. Defaults to None.
            system_instruction (dict, optional): Instrucciones para el sistema. Defaults to None.
            response_schema (dict, optional): Esquema JSON para la respuesta. Defaults to None.
        """
        self.model = model
        self.generation_config = generation_config
        self.system_instruction = system_instruction
        self.response_schema = response_schema
        self.validate_model()

    def validate_model(self):
        """
        Valida el modelo.
        """
        if self.model not in ["gemini-2.5-pro-preview-03-25", "gemini-2.0-flash"]:
            raise ValueError("Modelo inválido. Debe ser 'gemini-2.5-pro-preview-03-25' o 'gemini-2.0-flash'.")


def llm_request(prompt: str, config: LLMConfig = None):
    """
    Estructura de función para interactuar con una API LLM.

    Args:
        prompt (str): El prompt principal para la API LLM.
        config (LLMConfig, optional): Un objeto de configuración opcional. Defaults to None.
            Permite especificar opciones avanzadas como generationConfig, systemInstruction y model.

    Returns:
        str: La respuesta del servidor como una cadena JSON con el formato {"response": "answer"}.
    """
    try:
        api_key = get_api_key()
    except ValueError as e:
        print(f"Error al obtener la API key: {e}")
        return None

    # Si no se proporciona una configuración, crear una por defecto
    if config is None:
        config = LLMConfig()

    # Definir el esquema JSON por defecto
    default_response_schema = {
      "type": "object",
      "properties": {
        "response": {
          "type": "string"
        }
      }
    }

    # Construir el cuerpo de la solicitud (request body)
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
    }

    # Manejar generationConfig
    if config.generation_config:
        data["generationConfig"] = config.generation_config

    # Manejar systemInstruction
    if config.system_instruction:
        data["tools"] = [
            {
                "function_declarations": [
                    config.system_instruction
                ]
            }
        ],

    payload = json.dumps(data)

    # Configurar las cabeceras (headers)
    headers = {"Content-Type": "application/json"}

    # Construir la URL para streamGenerateContent
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{config.model}:streamGenerateContent?key={api_key}"

    try:
        # Realizar la solicitud POST
        response = requests.post(url, headers=headers, data=payload)

        # Manejar las excepciones y errores
        response.raise_for_status()  # Lanza una excepción para códigos de estado HTTP malos (4xx o 5xx)

        # Parsear la respuesta JSON
        response_json = response.json()

        # Extraer la respuesta y formatearla
        final_answer = ""
        if isinstance(response_json, list) and len(response_json) > 0 and "candidates" in response_json[-1] and len(response_json[-1]["candidates"]) > 0 and "content" in response_json[-1]["candidates"][0] and "parts" in response_json[-1]["candidates"][0]["content"] and len(response_json[-1]["candidates"][0]["content"]["parts"]) > 0 and "text" in response_json[-1]["candidates"][0]["content"]["parts"][0]:
            final_answer = response_json[-1]["candidates"][0]["content"]["parts"][0]["text"].strip()

        # Remove equals sign if present
        if final_answer.startswith("="):
            final_answer = final_answer[1:].strip()

        # Devolver la respuesta en el formato especificado
        return json.dumps({"response": final_answer})

    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return None
    except ValueError as e:
        print(f"Error de validación: {e}")
        return None
