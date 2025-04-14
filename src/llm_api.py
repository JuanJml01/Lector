# -*- coding: utf-8 -*-
"""
Módulo para interactuar con la API del modelo de lenguaje Gemini de Google.
"""

import os
import json
import requests
from typing import Optional, Dict, Any, Union

# --- Constantes ---
# Define el modelo de Gemini a utilizar. Puedes cambiarlo por otros modelos disponibles como 'gemini-pro'.
# 'gemini-1.5-flash' es una opción eficiente y rápida.
MODELO_PREDETERMINADO = "gemini-1.5-flash"
# Endpoint base de la API de Gemini v1beta
URL_BASE_API = "https://generativelanguage.googleapis.com/v1beta/models/"
# Acción a realizar en la API (generar contenido)
ACCION_API = "generateContent"
# Nombre de la variable de entorno para la clave API
NOMBRE_VARIABLE_API_KEY = "GEMINI_API_KEY"
# Tipos de contenido soportados por esta implementación para el *envío*
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_TEXT = "text/plain"


# --- Excepciones Personalizadas ---
class GeminiApiException(Exception):
    """Excepción base para errores relacionados con la API de Gemini."""
    pass


class CredencialesInvalidasError(GeminiApiException):
    """Excepción lanzada cuando la clave API es inválida o falta."""
    pass


class ErrorDeRedError(GeminiApiException):
    """Excepción lanzada por problemas de conexión con la API."""
    pass


class RespuestaInesperadaError(GeminiApiException):
    """Excepción lanzada cuando la API devuelve una respuesta no esperada."""

    def __init__(self, mensaje, respuesta_bruta=None):
        super().__init__(mensaje)
        self.respuesta_bruta = respuesta_bruta

    def __str__(self):
        msg = super().__str__()
        if self.respuesta_bruta:
            msg += f"\nRespuesta bruta recibida:\n{self.respuesta_bruta}"
        return msg


class TipoContenidoNoSoportadoError(ValueError, GeminiApiException):
    """Excepción lanzada cuando se intenta usar un Content-Type no soportado por la función."""
    pass


# --- Función Principal ---

def interactuar_con_gemini(
        contenido: str,
        modelo_id: str = MODELO_PREDETERMINADO,
        instruccion_sistema: Optional[str] = None,
        configuracion_generacion: Optional[Dict[str, Any]] = None,
        content_type_envio: str = CONTENT_TYPE_JSON,
) -> str:
    """
    Envía una solicitud a la API del modelo Gemini de Google y devuelve la respuesta generada.

    Esta función se encarga de construir la solicitud HTTP, manejar la autenticación
    mediante una clave API (obtenida de una variable de entorno), enviar la solicitud
    según el `content_type_envio` especificado, procesar la respuesta (asumiendo JSON)
    y manejar posibles errores durante el proceso.

    Args:
        contenido (str): El texto de entrada (prompt) o datos que se enviarán al modelo.
                         Su formato dependerá del `content_type_envio`.
        modelo_id (str, optional): El identificador del modelo Gemini a utilizar.
                                   Por defecto es 'gemini-1.5-flash'.
        instruccion_sistema (Optional[str], optional): Instrucciones adicionales para guiar
                                                      el comportamiento del modelo.
                                                      **Solo aplicable si `content_type_envio`
                                                      es 'application/json'**.
                                                      Por defecto es None.
        configuracion_generacion (Optional[Dict[str, Any]], optional):
                                    Un diccionario para configurar parámetros avanzados
                                    de generación (ej: temperatura, top_p, max_output_tokens).
                                    **Solo aplicable si `content_type_envio`
                                    es 'application/json'**.
                                    Consulte la documentación de la API de Gemini para
                                    las opciones disponibles. Por defecto es None.
        content_type_envio (str, optional): El tipo de contenido del cuerpo de la solicitud.
                                           Debe ser 'application/json' o 'text/plain'.
                                           Por defecto es 'application/json'.
                                           **Nota:** La API estándar de Gemini (`generateContent`)
                                           espera 'application/json'. Usar 'text/plain'
                                           puede requerir un endpoint o modelo diferente y
                                           podría no ser compatible con `instruccion_sistema`
                                           o `configuracion_generacion`.

    Returns:
        str: El texto generado por el modelo Gemini como respuesta (asumiendo que la
             respuesta de la API es JSON y contiene texto).

    Raises:
        CredencialesInvalidasError: Si la variable de entorno GEMINI_API_KEY no está
                                   configurada o la clave es rechazada por la API.
        ErrorDeRedError: Si ocurre un problema de red al intentar conectar con la API
                         (ej: sin conexión a internet, timeout).
        RespuestaInesperadaError: Si la API devuelve un código de estado inesperado
                                 o si la estructura de la respuesta JSON (si se espera)
                                 no es la esperada.
        ValueError: Si el argumento 'contenido' está vacío.
        TipoContenidoNoSoportadoError: Si se proporciona un `content_type_envio`
                                       diferente a 'application/json' o 'text/plain'.
    """
    # --- Validación de Entrada ---
    if not contenido:
        raise ValueError("El parámetro 'contenido' no puede estar vacío.")

    if content_type_envio not in [CONTENT_TYPE_JSON, CONTENT_TYPE_TEXT]:
        raise TipoContenidoNoSoportadoError(
            f"Tipo de contenido de envío no soportado: '{content_type_envio}'. "
            f"Use '{CONTENT_TYPE_JSON}' o '{CONTENT_TYPE_TEXT}'."
        )

    # --- Obtención de Credenciales ---
    clave_api = os.getenv(NOMBRE_VARIABLE_API_KEY)
    if not clave_api:
        raise CredencialesInvalidasError(
            f"La variable de entorno '{NOMBRE_VARIABLE_API_KEY}' no está configurada. "
            "Por favor, defina su clave API de Gemini."
        )

    # --- Construcción de la URL del Endpoint ---
    url_endpoint = f"{URL_BASE_API}{modelo_id}:{ACCION_API}?key={clave_api}"

    # --- Definición de Cabeceras HTTP ---
    headers = {
        "Content-Type": content_type_envio
    }

    # --- Construcción del Cuerpo de la Solicitud (Data) ---
    request_data: Union[str, bytes]

    if content_type_envio == CONTENT_TYPE_JSON:
        # Construye el payload JSON estructurado como antes
        partes_contenido = [{"text": contenido}]
        payload: Dict[str, Any] = {
            "contents": [
                {
                    "role": "user",
                    "parts": partes_contenido
                }
            ]
        }

        if instruccion_sistema:
            payload["systemInstruction"] = {
                "parts": [
                    {"text": instruccion_sistema}
                ]
            }

        # Asegura que el tipo de respuesta MIME sea JSON para facilitar el parseo
        # y añade la configuración de generación si se proporciona.
        config_gen_final = configuracion_generacion if configuracion_generacion else {}
        config_gen_final["responseMimeType"] = CONTENT_TYPE_JSON  # Aseguramos JSON en respuesta
        payload["generationConfig"] = config_gen_final

        try:
            # Convierte el diccionario Python a una cadena JSON.
            request_data = json.dumps(payload)
        except TypeError as e:
            raise ValueError(f"Error al serializar el payload a JSON: {e}") from e

    elif content_type_envio == CONTENT_TYPE_TEXT:
        # Para text/plain, el cuerpo es simplemente el contenido en sí.
        # 'requests' prefiere bytes para datos no codificados como form/multipart,
        # especialmente si contienen caracteres no ASCII. UTF-8 es un estándar seguro.
        if not isinstance(contenido, str):
            # Aunque ya validamos que no esté vacío, aseguramos que sea string
            raise TypeError("El 'contenido' debe ser una cadena para 'text/plain'.")
        request_data = contenido.encode('utf-8')
        # Advertencia si se usan opciones solo JSON
        if instruccion_sistema or configuracion_generacion:
            print(f"Advertencia: 'instruccion_sistema' y 'configuracion_generacion' "
                  f"generalmente solo tienen efecto con Content-Type '{CONTENT_TYPE_JSON}'. "
                  f"Están siendo ignorados para '{CONTENT_TYPE_TEXT}'.")

    # (Aquí se podría añadir un else para manejar otros content_type si se expandiera,
    # pero ya lo validamos al inicio)

    # --- Realización de la Solicitud HTTP ---
    try:
        respuesta_api = requests.post(
            url_endpoint,
            headers=headers,
            data=request_data,  # Usa los datos preparados (JSON string o bytes)
            timeout=60  # Timeout de 60 segundos para la conexión y lectura.
        )

        # --- Verificación del Código de Estado HTTP ---
        respuesta_api.raise_for_status()

    except requests.exceptions.Timeout as err_timeout:
        raise ErrorDeRedError(f"La solicitud a la API de Gemini ha expirado: {err_timeout}") from err_timeout
    except requests.exceptions.ConnectionError as err_conn:
        raise ErrorDeRedError(f"Error de conexión con la API de Gemini: {err_conn}") from err_conn
    except requests.exceptions.HTTPError as err_http:
        status_code = err_http.response.status_code
        # Intenta obtener detalles del error desde la respuesta (JSON o texto)
        try:
            error_details = err_http.response.json()
            error_raw = json.dumps(error_details)  # Para el mensaje de error
        except json.JSONDecodeError:
            error_details = err_http.response.text  # Si no es JSON, usa el texto plano.
            error_raw = error_details

        error_msg_base = f"Error HTTP {status_code} de la API de Gemini."

        if status_code == 400:
            raise RespuestaInesperadaError(
                f"{error_msg_base} Solicitud incorrecta. Verifique los datos enviados "
                f"(formato {content_type_envio}) y los parámetros. Detalles: {error_raw}",
                error_raw
            ) from err_http
        elif status_code in [401, 403]:
            raise CredencialesInvalidasError(
                f"{error_msg_base} Credenciales inválidas o permisos insuficientes. "
                f"Verifique su clave API ({NOMBRE_VARIABLE_API_KEY}). Detalles: {error_raw}"
            ) from err_http
        elif status_code == 429:
            raise RespuestaInesperadaError(
                f"{error_msg_base} Demasiadas solicitudes (Rate Limit Exceeded). "
                f"Ha excedido la cuota de la API. Detalles: {error_raw}",
                error_raw
            ) from err_http
        else:
            # Otros errores HTTP.
            raise RespuestaInesperadaError(
                f"{error_msg_base} Error inesperado. Detalles: {error_raw}",
                error_raw
            ) from err_http
    except requests.exceptions.RequestException as err_req:
        # Captura cualquier otro error de la librería 'requests'.
        raise ErrorDeRedError(f"Error inesperado durante la solicitud a la API: {err_req}") from err_req

    # --- Procesamiento de la Respuesta Exitosa ---
    # ASUNCIÓN: La API *siempre* devuelve JSON en caso de éxito,
    # incluso si la solicitud fue text/plain (esto es común en APIs REST).
    # Si la API pudiera devolver texto plano en éxito, esta parte necesitaría cambiar.
    try:
        datos_respuesta = respuesta_api.json()

        # --- Extracción del Texto Generado (asumiendo estructura de generateContent) ---
        if not datos_respuesta.get("candidates"):
            raise RespuestaInesperadaError(
                "La respuesta JSON de la API no contiene la clave 'candidates'.",
                respuesta_api.text  # Mostrar texto bruto si falla el parseo esperado
            )

        candidatos = datos_respuesta["candidates"]
        if not isinstance(candidatos, list) or len(candidatos) == 0:
            raise RespuestaInesperadaError(
                "La clave 'candidates' en la respuesta no es una lista válida o está vacía.",
                respuesta_api.text
            )

        # Usualmente, la primera candidata contiene la respuesta principal.
        candidato_principal = candidatos[0]

        if not isinstance(candidato_principal, dict) or "content" not in candidato_principal:
            raise RespuestaInesperadaError(
                "El primer candidato en la respuesta no tiene la clave 'content'.",
                respuesta_api.text
            )

        contenido_candidato = candidato_principal["content"]

        if not isinstance(contenido_candidato, dict) or "parts" not in contenido_candidato:
            raise RespuestaInesperadaError(
                "El 'content' del candidato principal no tiene la clave 'parts'.",
                respuesta_api.text
            )

        partes_respuesta = contenido_candidato["parts"]
        if not isinstance(partes_respuesta, list) or len(partes_respuesta) == 0:
            raise RespuestaInesperadaError(
                "La clave 'parts' en el contenido del candidato está vacía o no es una lista.",
                respuesta_api.text
            )

        # Accede a la primera parte del contenido (generalmente es texto).
        primera_parte = partes_respuesta[0]
        if not isinstance(primera_parte, dict) or "text" not in primera_parte:
            raise RespuestaInesperadaError(
                "La primera parte de la respuesta del candidato no contiene la clave 'text'.",
                respuesta_api.text
            )

        texto_generado = primera_parte["text"]
        if not isinstance(texto_generado, str):
            raise RespuestaInesperadaError(
                "El valor de 'text' en la respuesta no es una cadena.",
                respuesta_api.text
            )

        return texto_generado.strip()  # Devuelve el texto limpio de espacios extra.

    except json.JSONDecodeError as err_json:
        raise RespuestaInesperadaError(
            "Error al decodificar la respuesta JSON de la API. Se esperaba JSON.",
            respuesta_api.text  # Incluye el texto original para depuración.
        ) from err_json
    except (KeyError, IndexError, TypeError) as err_struct:
        # Captura errores si la estructura JSON no es la esperada.
        raise RespuestaInesperadaError(
            f"La estructura de la respuesta JSON de la API no es la esperada: {err_struct}",
            datos_respuesta if 'datos_respuesta' in locals() else respuesta_api.text
        ) from err_struct


# --- Ejemplo de Uso (Opcional) ---
# if __name__ == "__main__":
#     # Para ejecutar este ejemplo:
#     # 1. Asegúrate de tener la librería 'requests': pip install requests
#     # 2. Define la variable de entorno GEMINI_API_KEY con tu clave API.
#     #    En Linux/macOS: export GEMINI_API_KEY="TU_CLAVE_API_AQUI"
#     #    En Windows (cmd): set GEMINI_API_KEY=TU_CLAVE_API_AQUI
#     #    En Windows (PowerShell): $env:GEMINI_API_KEY="TU_CLAVE_API_AQUI"
#
#     print("--- Ejemplo con application/json (predeterminado) ---")
#     try:
#         prompt_json = "Explica brevemente qué es la computación cuántica."
#         respuesta_json = interactuar_con_gemini(
#             contenido=prompt_json,
#             instruccion_sistema="Responde de forma concisa y para principiantes.",
#             configuracion_generacion={"temperature": 0.7}
#         )
#         print(f"Pregunta: {prompt_json}")
#         print(f"Respuesta Gemini (JSON):\n{respuesta_json}")
#
#     except GeminiApiException as e:
#         print(f"Error de API Gemini (JSON): {e}")
#     except ValueError as e:
#         print(f"Error de validación (JSON): {e}")
#     except Exception as e:
#         print(f"Error inesperado (JSON): {e}")
#
#     print("\n--- Ejemplo con text/plain ---")
#     print("ADVERTENCIA: El endpoint estándar 'generateContent' de Gemini espera JSON.")
#     print("Usar 'text/plain' podría fallar o requerir un endpoint/modelo diferente.")
#     try:
#         prompt_text = "Dame un poema corto sobre la lluvia."
#         # Nota: instruccion_sistema y configuracion_generacion serían ignorados aquí
#         respuesta_text = interactuar_con_gemini(
#             contenido=prompt_text,
#             content_type_envio=CONTENT_TYPE_TEXT
#         )
#         print(f"\nPregunta: {prompt_text}")
#         # Asumimos que la *respuesta* sigue siendo JSON y la parseamos igual
#         print(f"Respuesta Gemini (Text -> JSON parseado):\n{respuesta_text}")
#
#     except TipoContenidoNoSoportadoError as e:
#         print(f"Error de tipo de contenido (Text): {e}")  # No debería ocurrir con text/plain
#     except GeminiApiException as e:
#         print(f"Error de API Gemini (Text): {e}")  # Más probable si el endpoint no acepta text/plain
#     except ValueError as e:
#         print(f"Error de validación (Text): {e}")
#     except Exception as e:
#         print(f"Error inesperado (Text): {e}")
