from llama_cpp import Llama

from app.models import StoryNode

import re
import json

# https://huggingface.co/SanctumAI/Meta-Llama-3.1-8B-Instruct-GGUF
MODEL_PATH = "./app/model/meta-llama-3.1-8b-instruct.Q4_K_M.gguf"
model = Llama(model_path=MODEL_PATH)

def build_prompt(story_nodes, last_decision):
    # Convertir los diccionarios en instancias de StoryNode
    story_nodes = [StoryNode(**node) for node in story_nodes]

    # Se recoge los últimos 1 o 2 nodos para que se tenga un contexto de la historia.
    # history = "\n".join([f"Paso {node.step}: {node.text}\nDecisión: {node.decision or '---'}" for node in story_nodes[-2:]])
    history = "\n".join([f"Paso {node.step}: {node.text}\nDecisión: {node.decision or '---'}" for node in story_nodes[-1:]])
    prompt = f"""
Eres un narrador que cuenta una historia interactiva humorística protagonizada por un gato (michi) callejero cuyo objetivo es conquistar el mundo.

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

No agregues explicaciones ni texto fuera del JSON.

"""
    return prompt

def story_generator(prompt: str):
    result = model(prompt, max_tokens=512, temperature=0.9, top_k=40, top_p=0.9)
    generated_text = result["choices"][0]["text"]
    return [{"generated_text": generated_text}]

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