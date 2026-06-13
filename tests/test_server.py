import unittest
from unittest.mock import patch

import server


class ServerContractTests(unittest.IsolatedAsyncioTestCase):
    async def test_list_tools_exposes_weather_and_time(self) -> None:
        tools = await server.list_tools()
        names = {tool.name for tool in tools}

        self.assertEqual(names, {"get_weather", "get_time"})

        weather_tool = next(tool for tool in tools if tool.name == "get_weather")
        self.assertEqual(weather_tool.inputSchema["required"], ["city"])

        time_tool = next(tool for tool in tools if tool.name == "get_time")
        self.assertEqual(time_tool.inputSchema["required"], ["timezone"])

    @patch("server.get_weather", return_value="meteo test")
    async def test_call_tool_weather(self, mock_get_weather) -> None:
        result = await server.call_tool("get_weather", {"city": "Paris"})

        mock_get_weather.assert_called_once_with("Paris")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, "text")
        self.assertEqual(result[0].text, "meteo test")

    @patch("server.get_weather", return_value="meteo paris")
    async def test_call_tool_weather_uses_default_city(self, mock_get_weather) -> None:
        result = await server.call_tool("get_weather", {})

        mock_get_weather.assert_called_once_with("Paris")
        self.assertEqual(result[0].text, "meteo paris")

    @patch("server.get_time", return_value="heure test")
    async def test_call_tool_time(self, mock_get_time) -> None:
        result = await server.call_tool("get_time", {"timezone": "Europe/Paris"})

        mock_get_time.assert_called_once_with("Europe/Paris")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, "text")
        self.assertEqual(result[0].text, "heure test")

    @patch("server.get_time", return_value="heure paris")
    async def test_call_tool_time_uses_default_timezone(self, mock_get_time) -> None:
        result = await server.call_tool("get_time", {})

        mock_get_time.assert_called_once_with("Europe/Paris")
        self.assertEqual(result[0].text, "heure paris")

    async def test_call_tool_unknown(self) -> None:
        result = await server.call_tool("unknown_tool", {})

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, "text")
        self.assertIn("non pris en charge", result[0].text)


if __name__ == "__main__":
    unittest.main()
