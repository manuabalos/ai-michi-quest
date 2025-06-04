# from gpt4all import GPT4All
from llama_cpp import Llama

from app.models import StoryNode


# # Ruta del modelo local
# MODEL_PATH = "app/"
# MODEL_NAME = "mistral-7b-instruct-v0.1.Q4_0.gguf"

# model = GPT4All(model_path=MODEL_PATH, model_name=MODEL_NAME, allow_download=False)

MODEL_PATH = "./app/model/llama-2-7b-chat.Q4_K_M.gguf"
model = Llama(model_path=MODEL_PATH)

def build_prompt(story_nodes, last_decision):
    # Convertir los diccionarios en instancias de StoryNode
    story_nodes = [StoryNode(**node) for node in story_nodes]

    # Tomamos los últimos 1 o 2 nodos para contexto
    history = "\n".join([f"Paso {node.step}: {node.text}\nDecisión: {node.decision or '---'}" for node in story_nodes[-2:]])
    
    prompt = f"""
Eres un narrador que cuenta una historia interactiva humorística protagonizada por un gato (michi) callejero cuyo objetivo es conquistar el mundo.

Cada segmento debe:
- Ser divertido y absurdo.
- Terminar con 3 opciones de decisión.

---

Historia hasta ahora:
{history}

Última decisión del michi:
{last_decision}

---

Teniendo en cuenta la historia hasta ahora, genera un nuevo segmento de la historia basandote en la decisión tomada del michi. El nuevo fragmento debe ser breve y divertido.
Por último genera 2 o 3 opciones de decisión para el michi, cada una comenzando con un número o letra (1, 2, 3, A, B, C).
"""
    return prompt

def story_generator(prompt: str):
    # Generar texto usando GPT4All
    # generated_text = model.generate(prompt, max_tokens=300, top_k=40, top_p=0.9)
    
    # Generar texto usando LLaMA 2
    result = model(prompt, max_tokens=400, temperature=0.9, top_k=40, top_p=0.9)
    generated_text = result["choices"][0]["text"]

    return [{"generated_text": generated_text}]

def generate_next_node(prompt: str, step: int):
    output = story_generator(prompt)[0]["generated_text"]
    print("----------------------------------------") 
    print("output:", output) 
    print("----------------------------------------")

    if "---" in output:
        # Este delimitador se utiliza para separar el contenido principal de las opciones 
        # de decisión en el texto generado por el modelo.
        output = output.split("---")[-1].strip()

    lines = output.strip().split("\n")
    print("lines:", lines)
    print("****************************************")

    # Filtrar líneas que no son opciones (contenido principal)
    text_lines = [line for line in lines if not line.strip().startswith(tuple("123ABC"))]
    print("text_lines:", text_lines)
    print("****************************************")

    # Filtrar líneas que son opciones (comienzan con números o letras)
    choice_lines = [line.strip(" .") for line in lines if line.strip().startswith(tuple("123ABC"))]
    print("choice_lines:", choice_lines)
    print("****************************************")

    # Si no se encuentran opciones, usa valores predeterminados
    if not choice_lines:
        choice_lines = ["Seguir caminando", "Dormir", "Maullar al cielo"]

    return {
        "step": step,
        "text": "\n".join(text_lines).strip(),
        "choices": choice_lines
    }
