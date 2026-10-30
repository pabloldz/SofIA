import json
from datetime import datetime
from pathlib import Path


CARPETA = Path(__file__).parent  # carpeta donde vive memoria.py


class Memoria:
    def __init__(self, ruta=None, max_contexto=20, max_guardado=200):
        self.ruta = Path(ruta) if ruta else CARPETA / "memoria.json"
        self.max_contexto = max_contexto
        self.max_guardado = max_guardado
        self.datos = {"hechos": [], "historial": []}
        self.cargar()

    # ---------- persistencia ----------
    def cargar(self):
        if not self.ruta.exists():
            return
        try:
            self.datos = json.loads(self.ruta.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            # archivo dañado: lo respaldamos y empezamos limpio
            self.ruta.replace(self.ruta.with_suffix(".corrupto.json"))
            self.datos = {"hechos": [], "historial": []}

    def guardar(self):
        self.datos["historial"] = self.datos["historial"][-self.max_guardado:]
        tmp = self.ruta.with_suffix(".tmp")
        tmp.write_text(
            json.dumps(self.datos, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        tmp.replace(self.ruta)  # escritura atómica: no se corrompe si se cierra a medias

    # ---------- historial ----------
    def agregar_mensaje(self, role, content):
        self.datos["historial"].append({"role": role, "content": content})
        self.guardar()

    def quitar_ultimo(self):
        if self.datos["historial"]:
            self.datos["historial"].pop()
            self.guardar()
            
    def limpiar_historial(self):
        """Borra la conversación pero conserva los hechos."""
        self.datos["historial"] = []
        self.guardar()

    # ---------- hechos ----------
    @property
    def hechos(self):
        return self.datos["hechos"]

    def agregar_hecho(self, texto):
        texto = texto.strip()
        if not texto:
            return False
        if any(h["texto"].lower() == texto.lower() for h in self.hechos):
            return False  # evita duplicados exactos
        self.hechos.append({
            "texto": texto,
            "fecha": datetime.now().strftime("%Y-%m-%d"),
        })
        self.guardar()
        return True

    def olvidar(self, indice):
        """indice empieza en 1, tal como se muestra al usuario."""
        if 1 <= indice <= len(self.hechos):
            eliminado = self.hechos.pop(indice - 1)
            self.guardar()
            return eliminado["texto"]
        return None

    def olvidar_todo(self):
        self.datos = {"hechos": [], "historial": []}
        self.guardar()

    # ---------- construir contexto para el modelo ----------
    def construir_mensajes(self, system_prompt):
        system = system_prompt
        if self.hechos:
            lista = "\n".join(f"- {h['texto']}" for h in self.hechos)
            system += f"\n\nDatos que sabes sobre el usuario:\n{lista}"
        recientes = self.datos["historial"][-self.max_contexto:]
        return [{"role": "system", "content": system}] + recientes