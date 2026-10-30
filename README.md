# S.O.F.I.A

## Sistema Operativo de Funciones e Inteligencia Autonoma

Sofía comenzó como un programa básico de Python que recibía mensajes desde la terminal. El siguiente salto fue
conectarla con un modelo de lenguaje mediante Ollama.

## La idea

Su función será apoyar la rutina diaria y acompañar los proyectos futuros del usuario, evolucionando gradualmente desde una interfaz conversacional hacia un sistema capaz de utilizar herramientas, ejecutar tareas, mantener
memoria y, en etapas posteriores, incorporar voz, análisis en tiempo real y visión por computadora

## La conexion

Sofia comenzó utilizando la API de OpenAI como motor de generación de respuestas. El archivo
principal utilizaba el cliente de OpenAI y una clave almacenada mediante variables de entorno. Esta
arquitectura implicaba depender de un servicio externo, de disponibilidad de API y de consumo de créditos/tokens.
El objetivo de utilizar una conexion local con Ollama y Qwen3 fue mantener la personalidad, el contexto conversacional y la memoria persistente de Sofia, pero sustituir únicamente el motor de lenguaje por una solución local que no
dependiera de una API externa.

## Crear la identidad y personalidad

Una vez establecida la conexión con el modelo, se creó un conjunto de instrucciones para definir el
comportamiento de Sofía. Esto permite diferenciar al asistente del modelo de lenguaje que utiliza como motor.

Modelo de lenguaje = motor

Sofia = Asistente construido alrededor del motor

Se introdujo SYSTEM_PROMPT para establecer identidad, propósito, estilo de comunicación y reglas básicas. Estas instrucciones se envían mediante el parámetro instructions.
Se comprobó que las instrucciones modificaban el comportamiento del modelo. También se detectó que una preferencia concreta, como responder siempre en español, conviene expresarla explícitamente.
Esto estableció un principio importante: las características de Sofía deben definirse mediante reglas y componentes claros, en lugar de depender de suposiciones sobre el comportamiento del modelo.
