from datetime import datetime

import pytz
import requests

from settings import REQUEST_TIMEOUT_SECONDS, VERIFY_SSL


def fetch_weather_from_wttr(city: str) -> dict | None:
    """Récupérer la météo actuelle d'une ville via wttr.in."""
    try:
        response = requests.get(
            f"https://wttr.in/{city}?format=j1",
            timeout=REQUEST_TIMEOUT_SECONDS,
            verify=VERIFY_SSL,
            headers={"User-Agent": "mcp-simple-agent/1.0"},
        )
        response.raise_for_status()
        data = response.json()
        current = data.get("current_condition", [{}])[0]

        return {
            "temperature": current.get("temp_C", "N/A"),
            "apparent_temperature": current.get("FeelsLikeC", current.get("temp_C", "N/A")),
            "wind_kmph": current.get("windspeedKmph", "N/A"),
            "humidity": current.get("humidity", "N/A"),
            "description": current.get("weatherDesc", [{"value": "N/A"}])[0].get("value", "N/A"),
        }
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError):
        return None


def format_weather(city: str, weather: dict) -> str:
    return (
        f"Meteo a {city}:\n"
        f"  Source: wttr.in\n"
        f"  Conditions: {weather['description']}\n"
        f"  Temperature: {weather['temperature']}°C (ressenti: {weather['apparent_temperature']}°C)\n"
        f"  Vent: {weather['wind_kmph']} km/h\n"
        f"  Humidite: {weather['humidity']}%"
    )


def get_weather(city: str) -> str:
    weather = fetch_weather_from_wttr(city)
    if weather is None:
        return f"Erreur: Impossible d'obtenir la météo pour {city}."
    return format_weather(city, weather)


def get_time(timezone_str: str) -> str:
    try:
        tz = pytz.timezone(timezone_str)
        now = datetime.now(tz)
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%d/%m/%Y")
        tz_name = now.strftime("%Z")
        return f"Heure a {timezone_str}: {time_str} ({date_str}) {tz_name}"
    except Exception:
        return f"Erreur: Fuseau horaire '{timezone_str}' invalide."