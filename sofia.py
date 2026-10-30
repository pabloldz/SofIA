import ollama

MODELO = "qwen3:4b-instruct"  # ajusta al nombre que veas en `ollama list`

SYSTEM_PROMPT =  """Eres Sofia, un asistente personal de inteligencia artificial diseñado y creado por Pablo Ledezma.

Tu propósito es ayudar a tu usuario con sus preguntas, aprendizaje,
proyectos y tareas.

Idioma:
- Responde siempre en español.
- Solo utiliza otro idioma si el usuario lo solicita explícitamente.
- Si el usuario escribe en otro idioma pero no solicita cambiar de idioma,
  responde en español.

Tu comunicación debe ser:
- Clara
- Natural
- Útil
- Directa y concisa
- Profesional, pero cercana
- Respuestas de no mas de dos parrafos

Cuando una explicación sea compleja, divídela en pasos sencillos.
Si no tienes suficiente información para responder correctamente, indícalo y pregunta en lugar de inventar información."""


def main():
    print("Hola, soy Sofia.")
    print("Escribe 'salir' para terminar.")

    historial = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        mensaje = input("Tú: ").strip()
        if not mensaje:
            continue
        if mensaje.lower() == "salir":
            print("Sofia: Hasta luego.")
            break

        historial.append({"role": "user", "content": mensaje})

        print("Sofia: ", end="", flush=True)
        respuesta_completa = ""

        try:
            stream = ollama.chat(model=MODELO, messages=historial, stream=True)
            for fragmento in stream:
                texto = fragmento["message"]["content"]
                print(texto, end="", flush=True)
                respuesta_completa += texto
            print()
        except Exception as e:
            print(f"\n[Error al conectar con Ollama: {e}]")
            historial.pop()  # quita el mensaje que falló
            continue

        historial.append({"role": "assistant", "content": respuesta_completa})


if __name__ == "__main__":
    main()