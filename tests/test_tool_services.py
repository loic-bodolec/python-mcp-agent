import unittest
from unittest.mock import Mock, patch

import tool_services


class FetchWeatherFromWttrTests(unittest.TestCase):
    @patch("tool_services.requests.get")
    def test_parses_current_condition_payload(self, mock_get: Mock) -> None:
        mock_response = Mock()
        mock_response.json.return_value = {
            "current_condition": [
                {
                    "temp_C": "18",
                    "FeelsLikeC": "17",
                    "windspeedKmph": "10",
                    "humidity": "64",
                    "weatherDesc": [{"value": "Partly cloudy"}],
                }
            ]
        }
        mock_get.return_value = mock_response

        result = tool_services.fetch_weather_from_wttr("Paris")

        mock_get.assert_called_once_with(
            "https://wttr.in/Paris?format=j1",
            timeout=tool_services.REQUEST_TIMEOUT_SECONDS,
            verify=tool_services.VERIFY_SSL,
            headers={"User-Agent": "mcp-simple-agent/1.0"},
        )

        self.assertEqual(
            result,
            {
                "temperature": "18",
                "apparent_temperature": "17",
                "wind_kmph": "10",
                "humidity": "64",
                "description": "Partly cloudy",
            },
        )

    @patch("tool_services.requests.get")
    def test_returns_none_on_request_exception(self, mock_get: Mock) -> None:
        mock_get.side_effect = tool_services.requests.RequestException("network error")
        self.assertIsNone(tool_services.fetch_weather_from_wttr("Paris"))

    @patch("tool_services.requests.get")
    def test_uses_fallback_fields_when_missing(self, mock_get: Mock) -> None:
        mock_response = Mock()
        mock_response.json.return_value = {
            "current_condition": [
                {
                    "temp_C": "19",
                }
            ]
        }
        mock_get.return_value = mock_response

        result = tool_services.fetch_weather_from_wttr("Paris")

        self.assertEqual(
            result,
            {
                "temperature": "19",
                "apparent_temperature": "19",
                "wind_kmph": "N/A",
                "humidity": "N/A",
                "description": "N/A",
            },
        )


class WeatherAndTimeFacadeTests(unittest.TestCase):
    @patch("tool_services.fetch_weather_from_wttr")
    def test_get_weather_success(self, mock_fetch: Mock) -> None:
        mock_fetch.return_value = {
            "temperature": "12",
            "apparent_temperature": "10",
            "wind_kmph": "15",
            "humidity": "80",
            "description": "Light rain",
        }

        text = tool_services.get_weather("Lyon")

        self.assertIn("Meteo a Lyon", text)
        self.assertIn("Source: wttr.in", text)
        self.assertIn("Light rain", text)

    @patch("tool_services.fetch_weather_from_wttr")
    def test_get_weather_error(self, mock_fetch: Mock) -> None:
        mock_fetch.return_value = None
        text = tool_services.get_weather("Lyon")
        self.assertEqual(text, "Erreur: Impossible d'obtenir la météo pour Lyon.")

    def test_get_time_invalid_timezone(self) -> None:
        text = tool_services.get_time("Invalid/Timezone")
        self.assertIn("Erreur: Fuseau horaire 'Invalid/Timezone' invalide.", text)


if __name__ == "__main__":
    unittest.main()
