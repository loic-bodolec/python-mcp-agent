import unittest

from intent_router import ToolRequest, detect_tool_request


class DetectToolRequestTests(unittest.TestCase):
    def test_weather_city_extraction(self) -> None:
        result = detect_tool_request("Quelle est la meteo a Nantes ?")
        self.assertEqual(result, ToolRequest(name="get_weather", arguments={"city": "Nantes"}))

    def test_weather_defaults_to_paris_without_city(self) -> None:
        result = detect_tool_request("Donne la meteo")
        self.assertEqual(result, ToolRequest(name="get_weather", arguments={"city": "Paris"}))

    def test_time_tokyo(self) -> None:
        result = detect_tool_request("Quelle heure est-il a Tokyo ?")
        self.assertEqual(result, ToolRequest(name="get_time", arguments={"timezone": "Asia/Tokyo"}))

    def test_time_london(self) -> None:
        result = detect_tool_request("Heure a Londres")
        self.assertEqual(result, ToolRequest(name="get_time", arguments={"timezone": "Europe/London"}))

    def test_general_question_returns_none(self) -> None:
        result = detect_tool_request("Explique la relativite")
        self.assertIsNone(result)

    def test_weather_with_accent_and_city(self) -> None:
        result = detect_tool_request("Météo à Paris ?")
        self.assertEqual(result, ToolRequest(name="get_weather", arguments={"city": "Paris"}))

    def test_time_newyork_variants(self) -> None:
        result = detect_tool_request("current time in newyork")
        self.assertEqual(result, ToolRequest(name="get_time", arguments={"timezone": "America/New_York"}))

    def test_weather_article_only_falls_back_to_paris(self) -> None:
        result = detect_tool_request("meteo de la")
        self.assertEqual(result, ToolRequest(name="get_weather", arguments={"city": "Paris"}))


if __name__ == "__main__":
    unittest.main()
