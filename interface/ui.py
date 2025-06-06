import gradio as gr
import requests
API_URL = "http://127.0.0.1:8000"

def start_story(player_name):
  response = requests.post(f"{API_URL}/start", params={"player_name": player_name})
  data = response.json()
  return data["story_id"], data["intro"], data["choices"]

def continue_story(story_id, decision):
  response = requests.post(f"{API_URL}/decision/{story_id}", params={"decision": decision})
  data = response.json()
  return data["text"], data["choices"]

def gradio_start(player_name):
  story_id, intro, choices = start_story(player_name)
  return story_id, intro, gr.update(choices=choices, value=None), gr.update(visible=True)

def gradio_continue(story_id, decision):
  text, choices = continue_story(story_id, decision)
  return text, gr.update(choices=choices, value=None)

def create_interface():
  with gr.Blocks() as demo:
    gr.Markdown("# 🐾 Michi: Camino al Dominio Mundial")
    gr.Markdown("En esta aventura felina, encarnarás a un michi con un sueño tan ambicioso como adorable: ¡dominar el mundo en nombre de todos los gatos! Tu camino estará lleno de decisiones cruciales que te llevarán por destinos inesperados. ¿Serás coronado como el rey amado de todos los michis, o acabarás atrapado en la jaula emocional de una niña pegajosa y llorona que te viste con moños y jamás te deja escapar? Cada elección cuenta, y tu destino como conquistador (o mascota condenada) está en tus patas. *<span style='color: #888'>Meow! 🐱👑</span>*")
    
    name = gr.Textbox(label="Nombre del michi", placeholder="Intriduce el nombre de tu michi", lines=1)
    btn_start = gr.Button("Iniciar aventura")
    
    story_id = gr.State()
    intro = gr.Textbox(label="Historia", interactive=False)
    options = gr.Radio(choices=[], label="Qué hara el michi?", visible=False)

    btn_continue = gr.Button("Enviar decisión", visible=True)

    btn_start.click(
      gradio_start,
      inputs=name,
      outputs=[story_id, intro, options, options]
    )

    btn_continue.click(
      gradio_continue,
      inputs=[story_id, options],
      outputs=[intro, options]
    )

  return demo