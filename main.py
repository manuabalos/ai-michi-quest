import threading
import uvicorn
from interface.ui import create_interface

def run_fastapi():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)

def run_gradio():
    iface = create_interface()
    iface.launch(server_name="127.0.0.1", server_port=7860)

if __name__ == "__main__":
    threading.Thread(target=run_fastapi, daemon=True).start()
    run_gradio()