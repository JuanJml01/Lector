from gemini_api import LLMConfig, llm_request

if __name__ == "__main__":

    config = LLMConfig()
    reponse = llm_request("Hola, Quien eres?", config)
    print(reponse)
