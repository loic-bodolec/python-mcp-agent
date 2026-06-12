import asyncio
import os

from groq import Groq

from intent_router import detect_tool_request
from mcp_client import MCPToolClient
from settings import DEBUG, GROQ_MODEL


def debug_log(message: str) -> None:
    """Afficher les logs debug uniquement si DEBUG=true."""
    if DEBUG:
        print(message)

async def main() -> None:
    conversation_history = []
    api_key = os.environ.get("GROQ_API_KEY", "").strip()

    if not api_key or api_key in {"gsk_...", "your_groq_api_key_here"}:
        print("Erreur: GROQ_API_KEY est manquante ou invalide dans .env")
        print("Ajoutez une clé valide puis relancez `python client.py`.")
        return

    client = Groq(api_key=api_key)
    mcp_client = MCPToolClient()

    try:
        tool_names = await mcp_client.connect()
    except Exception as err:
        print(f"Erreur: Impossible de démarrer la session MCP: {err}")
        print("Vérifiez que server.py est présent et que les dépendances sont installées.")
        return

    missing_tools = {"get_weather", "get_time"} - tool_names
    if missing_tools:
        print(f"Erreur: Tools MCP manquants: {', '.join(sorted(missing_tools))}")
        await mcp_client.aclose()
        return

    print("Assistant Groq lancé (tape 'exit' pour quitter)")
    print(f"Session MCP active: {', '.join(sorted(tool_names))}")
    print()

    system_prompt = """Tu es un assistant intelligent et utile. 
Réponds aux questions de l'utilisateur de manière concise et amicale."""

    # Ajouter le système au début de l'historique
    conversation_history.append({"role": "system", "content": system_prompt})

    while True:
        user_input = input("Vous: ")

        if user_input.lower() == "exit":
            break

        # Ajouter message à l'historique
        conversation_history.append({"role": "user", "content": user_input})

        try:
            tool_request = detect_tool_request(user_input)

            if tool_request:
                debug_log(f"[DEBUG] Détecté: {tool_request.name} avec {tool_request.arguments}")
                tool_result = await mcp_client.call_tool(tool_request.name, tool_request.arguments)
                debug_log(f"[DEBUG] Résultat: {tool_result[:100]}...")

                conversation_history.append({
                    "role": "user",
                    "content": f"Voici le résultat de {tool_request.name}: {tool_result}"
                })

                response = client.chat.completions.create(
                    model=GROQ_MODEL,
                    max_tokens=1024,
                    messages=conversation_history
                )

                final_response = response.choices[0].message.content or ""
                print("Assistant:", final_response)
                conversation_history.append({"role": "assistant", "content": final_response})
            else:
                response = client.chat.completions.create(
                    model=GROQ_MODEL,
                    max_tokens=1024,
                    messages=conversation_history
                )

                final_response = response.choices[0].message.content or ""
                print("Assistant:", final_response)
                conversation_history.append({"role": "assistant", "content": final_response})

            print()

        except Exception as err:
            print(f"Erreur: {err}")
            print()

    await mcp_client.aclose()

if __name__ == "__main__":
    asyncio.run(main())