from fastapi import APIRouter, HTTPException
from app.story_engine import build_prompt, generate_next_node
from app.models import MichiStory, StoryNode
from app.db import db

router = APIRouter()

@router.post("/start")
async def start_michi_adventure(player_name: str):
    intro_text = (
        "Te despiertas dentro de una caja de cartón húmeda, junto a una tienda de sushi cerrada.\n"
        "Tienes hambre. Tienes sueño. Tienes pelusa en el bigote. Pero algo en tu alma felina te dice: 'Has nacido para algo más grande.'\n"
        "Frente a ti, una paloma con parche en el ojo te mira fijamente. Podría ser una aliada... o una amenaza."
    )

    choices = [
        "Maullar fuertemente para atraer humanos",
        "Seguir a la paloma misteriosa",
        "Comer un trozo de sushi sospechoso del suelo"
    ]

    first_node = StoryNode(step=1, text=intro_text, choices=choices)

    story = MichiStory(player_name=player_name, story=[first_node])
    await db["stories"].insert_one(story.dict())

    return {"story_id": story.id, "intro": first_node.text, "choices": first_node.choices}

@router.post("/decision/{story_id}")
async def continue_story(story_id: str, decision: str):
    story_doc = await db["stories"].find_one({"id": story_id})
    if not story_doc:
        raise HTTPException(status_code=404, detail="Historia no encontrada")

    # Añadimos la decisión al último nodo
    last_node = story_doc["story"][-1]
    last_node["decision"] = decision

    # print("............................")
    # print("Último nodo antes de continuar:", last_node)
    # print("Decisión del michi:", decision)
    # print("............................")

    # Construimos el prompt para generar el siguiente nodo.
    prompt = build_prompt(story_doc["story"], decision)
    print("Prompt generado:", prompt)
    print("............................")
    next_step = story_doc["current_step"] + 1
    result = generate_next_node(prompt, next_step)

    new_node = StoryNode(**result)
    updated_story = story_doc["story"] + [new_node.dict()]

    await db["stories"].update_one(
        {"id": story_id},
        {
            "$set": {
                "story": updated_story,
                "current_step": next_step
            }
        }
    )

    return {"step": next_step, "text": new_node.text, "choices": new_node.choices}