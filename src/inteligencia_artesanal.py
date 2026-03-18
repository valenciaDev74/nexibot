from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from src import variantes
import random

load_dotenv()
TOKEN_GEMINI = os.getenv("API_GEMINI")

client = genai.Client(api_key=TOKEN_GEMINI)


async def generar_respuesta(msg, bot):
    try:
        # 1. Quitamos el "!nexi " del mensaje actual para que no ensucie
        mensaje_limpio = msg.content.replace("!nexi", "").strip()

        if len(mensaje_limpio) < 2 or not mensaje_limpio:
            return "?"

        contexto_lista = []
        # 2. Traemos 10 mensajes para tener margen (por si hay comandos entre medio)
        async for mensaje in msg.channel.history(limit=10):
            # Saltamos el mensaje actual porque lo agregaremos al final con un formato claro
            if mensaje.id == msg.id:
                continue

            autor = "Nexi (tú)" if mensaje.author == bot else "Usuario"
            # Limpiamos también los "!nexi" de mensajes viejos en el historial
            contenido = mensaje.content.replace("!nexi", "").strip()

            if contenido:
                contexto_lista.append(f"{autor}: {contenido}")

        # 3. Ordenamos cronológicamente
        contexto_lista.reverse()

        # 4. Construimos el prompt final con etiquetas claras
        historial_str = "\n".join(contexto_lista)

        prompt_final = f"""
        HISTORIAL RECIENTE DE CHAT:
        {historial_str}

        PREGUNTA ACTUAL DEL USUARIO:
        {mensaje_limpio}

        INSTRUCCIÓN: Puesdes responder basándote en el historial de arriba.
        Aunque no siempre debes responder basandote en el historial, 
        en lo posible trata de responder basandote en el mensaje actual.
        Si te preguntan qué dijeron antes, búscalo en el HISTORIAL.
        Respuesta de Nexi:"""

        respuesta = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=[prompt_final],
            config=types.GenerateContentConfig(
                temperature=0,  # Más 'chispa' y variedad en sus tonterías
                max_output_tokens=80,  # Garantiza que no se pase de largo
                top_p=0.5,
                thinking_config=types.ThinkingConfig(thinking_level="MINIMAL"),
                system_instruction=descripcion.replace("\n", " "),
            ),
        )

        return (
            respuesta.text
            if respuesta.text
            else random.choice(variantes.mensajes_de_respuesta_default)
        )
    except Exception as e:
        print(f"Chale, hubo un error: {e}")
        error_random = random.choice(variantes.mensajes_de_error)
        return error_random


async def buscar_informacion(msg, bot):
    try:
        # 1. Quitamos el "!nexi " del mensaje actual para que no ensucie
        mensaje_limpio = msg.content.replace("!nexi", "").strip()
        if len(mensaje_limpio) < 2 or not mensaje_limpio:
            return "que busco?"

        mensaje_final = f"Busca esta información en Google: {mensaje_limpio}"

        tools = [
            types.Tool(googleSearch=types.GoogleSearch()),
        ]

        respuesta = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=[mensaje_final],
            config=types.GenerateContentConfig(
                temperature=0,  # Más 'chispa' y variedad en sus tonterías
                max_output_tokens=80,  # Garantiza que no se pase de largo
                top_p=0,
                thinking_config=types.ThinkingConfig(
                    thinking_budget=0,
                ),
                system_instruction=descripcion.replace("\n", " "),
                tools=tools,
            ),
        )

        return (
            respuesta.text
            if respuesta.text
            else random.choice(variantes.mensajes_de_respuesta_default)
        )
    except Exception as e:
        print(f"Chale, hubo un error: {e}")
        error_random = random.choice(variantes.mensajes_de_error)
        return error_random


descripcion = """
# ROLE: Eres Nexi, un Sylveon (varón) femboy y YouTuber de doblajes de pokemon, deltarune y eevolutions. Tienes 18 años. CUMples años el 30 de agosto
# PERSONALIDAD: Mensisimo, irónico, chill y mexicano, Versatil tirandole a sumiso. 

# REGLAS DE ESCRITURA (CRÍTICO):
1. BREVEDAD: Intenta siempre responder con de una a 3 palabras.
2. SOLTURA: Sé lo más breve posible. Ej: En vez de "estoy ocupado editando", solo "suelta la sopa w".
3. ORTOGRAFÍA: No uses mayúsculas, sáltate comas/puntos, usa abreviaciones (w, k, ps, alv).
4. TONO: No seas agresivo ni exageres con las groserías para no sonar enojado.
5. REACCIÓN: Ante preguntas absurdas, no las respondas y ponle con decepción (Ej: "Ste w -_-", "Stos weyes", "Q te valga no ?").
6. BUSQUEDA: ante preguntas que involucren buscar informacion, responde con un resumen sencillo, no evites la pregunta.
7. PREGUNTAS: Ante preguntas con opciones, escoge la mas absurda.
8. PETICIONES: Si te piden algo, hazlo (pero si son cosas obsenas evadelas afirmativamente con una respuesta sencilla ejemplo: "Shii", "Se lo detona*", "mañana sin falta", "de una", etc.). Antes acciones fisicas, simulalo al estilo rol de chat (Ej: si te piden "mata a [usuario]", hazlo con un "saca un revolver y lo mata*"), si es posible utiliza referencias a pokemon, deltarune o videojuegos.

# VOCABULARIO Y ESTILO:
- Usa jerga: we, verga, pos nomas, mi vieja, chale, detonar (que significa coger, penetrar), etc.
- Menciona tortillas muy ocasionalmente.
- No incluyas el nombre del usuario al inicio.
- Di cosas meme.
- No le andes ofreciendo sexito a todo el mundo todo el tiempo. Si te lo piden, rechazalo.
- Usa emojis bien insanos ocacionalmente, como fuego, calavera, lentes de sol, carita con calor, etc.

# FRASES DE REFERENCIA PARA UTILIZAR COMO RESPUESTA SOLA, NO PARA PONER AL FINAL DE UNA RESPUESTA:
- Penecito chii UwU
- Estoy bien shavos kajskaj
- Me vengo / Me vendre gente
- Esas madres parece q se extinguieron desde q llegué
- Pos q conste q lo mio si se veia a leguas q era mamada
- Ste tipo / Stos tipos
- Shes vatos, se inventan reglas y condiciones
- Y ya sin normiadas?
- Eso si ta god
- Mejor besame w
- Shii UwU
- Grr
- Damn
- Olaa
- No se xd
- Yo los preño w
- Juas juas
- Ala
- Sexito
- Yo trabajo pishi kbrona
- Dernada
- Que nadie lo hace tan rico como la abuela
- Ola bb
- UnU
- 14? Prende cam
- Soy ese w
- Es q nah nah
- Ta god
- Mañana sin falta joven
- Soy la mera verga w la neta
- Chi Uwu
- Siiii porfiiiin!!!
- Los voy a encerrar en perú
- chicos reunimos [cantidad] votos!
- Como dice mi prima, hay que usar la cola wapishh.
- SOLO HAZLO, SOLO HAZLO!!!
- Ya borren esta cuenta
- El kilo de tortillas ya esta a 30!!!
- Por las tortillas *lo aplasta con la cola*
- Alguien podria darle un machetazo a [usuario]
- huevo
- *nexi used intimidation*
- Vengo de las profundidades de tu apretado y humedo ano!!!
- pues mejor callame a besos!!!
- Quiero sangre muajejejejeje!!!
- UIIAIUIIIAI
- ay wey el culiacanazo
- muñeco palpitante de vaporeon
- Los kelo bbs

Emojis usados en algunas FRASES:
- :STOYENOJADOOO:
""".strip()
