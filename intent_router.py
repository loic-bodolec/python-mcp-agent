from dataclasses import dataclass


@dataclass(frozen=True)
class ToolRequest:
    name: str
    arguments: dict[str, str]


def detect_tool_request(user_input: str) -> ToolRequest | None:
    """Détecter si la requête doit être routée vers un tool MCP."""
    lowered = user_input.lower()

    weather_keywords = [
        "meteo",
        "météo",
        "temps",
        "pluie",
        "nuage",
        "chaud",
        "froid",
        "neige",
        "température",
        "temperature",
        "temp",
        "climat",
        "weather",
        "condition",
    ]
    if any(word in lowered for word in weather_keywords):
        for keyword in [" à ", " a ", " de "]:
            if keyword in lowered:
                pos = lowered.rfind(keyword)
                city_part = lowered[pos + len(keyword):].strip().rstrip("?.")
                words = city_part.split()
                if words:
                    city = words[0].strip("?.,;:")
                    if city.lower() not in {"la", "le", "les"}:
                        return ToolRequest(name="get_weather", arguments={"city": city.title()})

        if any(word in lowered for word in ["meteo", "météo", "température", "temperature", "weather"]):
            return ToolRequest(name="get_weather", arguments={"city": "Paris"})

    if any(word in lowered for word in ["quelle heure", "heure", "what time", "current time"]):
        if "tokyo" in lowered or "japon" in lowered:
            return ToolRequest(name="get_time", arguments={"timezone": "Asia/Tokyo"})
        if "new york" in lowered or "newyork" in lowered:
            return ToolRequest(name="get_time", arguments={"timezone": "America/New_York"})
        if "london" in lowered or "londres" in lowered:
            return ToolRequest(name="get_time", arguments={"timezone": "Europe/London"})
        return ToolRequest(name="get_time", arguments={"timezone": "Europe/Paris"})

    return None