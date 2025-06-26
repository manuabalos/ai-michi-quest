import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()
from app.models import StoryNode

import re
import json

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

genai.configure(api_key=os.getenv(gemini_api_key)) 
model = genai.GenerativeModel("gemini-2.5-flash-lite-preview-06-17")

def build_prompt(story_nodes, last_decision):
    # Convertir los diccionarios en instancias de StoryNode
    story_nodes = [StoryNode(**node) for node in story_nodes]

    # Se recoge los últimos 1 o 2 nodos para que se tenga un contexto de la historia.
    # history = "\n".join([f"Paso {node.step}: {node.text}\nDecisión: {node.decision or '---'}" for node in story_nodes[-2:]])
    history = "\n".join([f"Paso {node.step}: {node.text}\nDecisión: {node.decision or '---'}" for node in story_nodes[-3:]])
    prompt = f"""
Tu rol: Eres un narrador que cuenta una historia interactiva humorística protagonizada por un gato (michi) callejero cuyo objetivo es conquistar el mundo.

Mi rol (usuario): Soy un michi callejero con un gran objetivo: conquistar el mundo. Porque los michis siempre han estado destinados a dominar el mundo. Pero primero debes sobrevivir al vecindario, reunir aliados (otros gatos, palomas, perros despistados), encontrar comida, hackear el router de los humanos, y más. Cada decisión afecta tu historia y destino.

Estilo: Humor absurdo: referencias a internet, memes de gatos, drama exagerado.
---

Historia hasta ahora:
{history}

Última decisión del michi:
{last_decision}

---

Devuelve la respuesta EXCLUSIVAMENTE en formato JSON sin markdown con la siguiente estructura:

{{
  "text": "fragmento breve, divertido y absurdo para continuar la historia.",
  "choices": [
    "Opción 1 de decisión",
    "Opción 2 de decisión",
    "Opción 3 de decisión"
  ]
}}

"""
    return prompt

def story_generator(prompt: str):
    # Genera contenido usando el modelo de Gemini.
    # El modelo debe estar configurado previamente con la clave de API.
    response = model.generate_content(prompt)
    return [{"generated_text": response.text}]

def generate_next_node(prompt: str, step: int):
    output = story_generator(prompt)[0]["generated_text"]
    print("----------------------------------------") 
    print("output:", output) 
    print("----------------------------------------")

    data = extract_json_from_output(output)
    if data and "text" in data and "choices" in data:
        return {
            "step": step,
            "text": data["text"],
            "choices": data["choices"]
        }
    else:
        return {
            "step": step,
            "text": output.strip(),
            "choices": [ "Maullar al cielo", "Seguir caminando", "Dormir", ]
        }

def extract_json_from_output(output):
    # Busca bloque de código Markdown con JSON.
    # Primero busca el JSON dentro de un bloque ....
    # Si no lo encuentra, busca el primer {...}.
    # Devuelve el diccionario listo para usar.
    match = re.search(r"```(?:json)?\s*({[\s\S]*?})\s*```", output)
    if not match:
        # Si no encuentra bloque Markdown, busca el primer bloque {...}
        match = re.search(r"\{[\s\S]*?\}", output)
    if match:
        try:
            data = json.loads(match.group(1) if match.lastindex else match.group())
            return data
        except Exception as e:
            print("Error al parsear JSON:", e)
    return None