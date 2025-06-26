## 🐱 **“Michi: Camino al Dominio Mundial”**

### 🎮 Concepto General

Eres un michi callejero con un gran objetivo: conquistar el mundo. Porque los michis siempre han estado destinados a dominar el mundo. Pero primero debes sobrevivir al vecindario, reunir aliados (otros gatos, palomas, perros despistados), encontrar comida, hackear el router de los humanos, y más. Cada decisión afecta tu historia y destino.

---

### 🧪 Estilo del Storytelling

- **Humor absurdo**: referencias a internet, memes de gatos, drama exagerado.
- **Decisiones ridículas pero con consecuencias**: "¿Maullar diplomáticamente o lanzar un bollo de pelo?"

---

### 🧩 Ideas de desarrollo

#### Endpoints principales

- `POST /start`: Comienza una nueva aventura.
- `POST /decision/{story_id}`: Envía una decisión y continúa la historia.
- `GET /choices/{story_id}`: Obtén las opciones disponibles.
- `GET /stats/{story_id}`: Consulta el estado del michi (energía, reputación, aliados).
- `GET /story/{story_id}`: Consulta el progreso de la historia.
- `POST /reset/{story_id}`: Reinicia la historia.

---

### 🛠️ Posible Stack

- **Backend**: FastAPI.
- **Base de datos**: MongoDB.
- **Frontend (opcional)**: Gradio para probar la historia.

---

### 🚀 Instalación rápida

1. Clona el repositorio.
2. Instala las dependencias:
```
pip install -r requirements.txt
```
. Configura tu archivo `.env` como se indica arriba.
3. Configura tu archivo `.env` como se indica arriba.
4. (Opcional) Ejecuta la interfaz Gradio:
```
python main.py
```
5. Ejecuta el backend:
```
uvicorn app.main:app --reload
```

### ⚠️ Configuración de la API de Gemini

Para que la aplicación funcione correctamente, **es imprescindible añadir tu clave de API de Gemini**.  
Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
GEMINI_API_KEY=tu_clave_api_de_gemini_aquí

Puedes obtener tu clave gratuita en [Google AI Studio](https://aistudio.google.com/app/apikey).

---

### 🐾 Ejemplo de Nodo Inicial

#### 🎬 NODO 1: El Despertar del Michi

**Narrativa:**

> Te despiertas dentro de una caja de cartón húmeda, justo al lado de una tienda de sushi cerrada. Llueve. Huele a desesperación y atún viejo.
> 
> Frente a ti, una paloma con parche en el ojo te mira fijamente. Podría ser una aliada... o una amenaza.
> 
> Tienes hambre. Tienes sueño. Tienes pelusa en el bigote. Pero algo en tu alma felina te dice: *"Has nacido para algo más grande."*

**Opciones:**

1. Maullar fuertemente para atraer humanos.
2. Seguir a la paloma misteriosa.
3. Comer un trozo de sushi sospechoso tirado en el suelo.

---

![Ejemplo de monstruo generado](img/readme-demo.png)

