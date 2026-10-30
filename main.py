import ollama
from memoria.memoria import Memoria
import json

MODELO = "qwen3:4b-instruct"
SYSTEM_PROMPT = (
    "Eres Sofia, una asistente amable y concisa. "
    "Responde siempre en español."
)


def main():
    mem = Memoria()

    print("Hola, soy Sofia.")
    print("Comandos: '/recuerda <dato>', '/memoria' historial, '/olvida <n>', '/clear limpia el historial de chat'  'salir'")

    while True:
        mensaje = input("Tú: ").strip()
        if not mensaje:
            continue
        bajo = mensaje.lower()

        # ----- comandos -----
        if bajo == "salir":
            print("Sofia: Hasta luego.")
            break

        if bajo.startswith("/recuerda"):
            dato = mensaje[len("recuerda:"):]
            ok = mem.agregar_hecho(dato)
            print("Sofia:", "Guardado." if ok else "Eso ya lo tenía.")
            continue

        if bajo == "/memoria":
            if not mem.hechos:
                print("Sofia: Aún no tengo datos guardados.")
            for i, h in enumerate(mem.hechos, 1):
                print(f"  {i}. {h['texto']}  ({h['fecha']})")
            continue

        if bajo.startswith("/olvida "):
            try:
                n = int(bajo.split()[1])
            except (IndexError, ValueError):
                print("Sofia: Usa 'olvida <número>'.")
                continue
            borrado = mem.olvidar(n)
            print("Sofia:", f"Olvidado: {borrado}" if borrado else "Ese número no existe.")
            continue
            
        if bajo == "/clear":
            mem.limpiar_historial()
            print("Sofia: Historial borrado. Conservo tus datos guardados.")
            continue

        # ----- conversación normal -----
        mem.agregar_mensaje("user", mensaje)

        print("Sofia: ", end="", flush=True)
        respuesta = ""
        try:
            stream = ollama.chat(
                model=MODELO,
                messages=mem.construir_mensajes(SYSTEM_PROMPT),
                stream=True,
            )
            for fragmento in stream:
                texto = fragmento["message"]["content"]
                print(texto, end="", flush=True)
                respuesta += texto
            print()
        except Exception as e:
            print(f"\n[Error con Ollama: {e}]")
            mem.quitar_ultimo()
            continue

        mem.agregar_mensaje("assistant", respuesta)
        
def extraer_hechos(mensaje_usuario):
    instruccion = (
        "Extrae del mensaje solo datos personales duraderos del usuario "
        "(nombre, profesión, gustos, proyectos). Ignora preguntas y charla casual. "
        'Responde solo JSON: {"hechos": ["..."]}. Si no hay nada, {"hechos": []}.'
    )
    try:
        r = ollama.chat(
            model=MODELO,
            messages=[
                {"role": "system", "content": instruccion},
                {"role": "user", "content": mensaje_usuario},
            ],
            format="json",
        )
        return json.loads(r["message"]["content"]).get("hechos", [])
    except Exception:
        return []


if __name__ == "__main__":
    main()