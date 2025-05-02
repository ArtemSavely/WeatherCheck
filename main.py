from flet import *
import requests

API_KEY = 'e68c4de4bbb92f4801d22d1a96059b1d'


class StringField(Text):
    def __init__(self, size, value, color=Colors.WHITE):
        super().__init__()
        self.value = value
        self.size = size
        self.color = color
        self.weight = FontWeight.BOLD


class CurrentWeather:
    def __init__(
            self,
            city,
            temperature,

    ):
        self.temperature = temperature
        self.city = city


class WeatherSearchBar(SearchBar):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.bar_hint_text = "Где посмотрим погоду?"
        self.on_submit = self.get_weather
        self.on_tap = lambda e: self.open_view()

    def get_weather(self, e):
        query = e.data
        params = {
            "lang": 'ru',
            "access_key": API_KEY,
            "query": query
        }
        request = requests.get(f"http://api.weatherstack.com/current", params=params).json()
        temperature.value = request['current']['temperature']
        print(request)
        self.close_view()
        self.page.update()




# e68c4de4bbb92f4801d22d1a96059b1d
# API_KEY = 'e68c4de4bbb92f4801d22d1a96059b1d'
# print(request['current']['weather_descriptions'])
# from translate import Translator
# translator= Translator(from_lang="english", to_lang="russian")
# translation = translator.translate('hi')
# print(translation)

temperature = StringField(size=30, value="temp")
city = StringField(size=25, value="city")

Text()
def main(page: Page):
    page.title = "WeatherCheck"
    page.bgcolor = Colors.BLUE
    page.window.width = 350
    page.window.height = 700
    page.theme_mode = ThemeMode.DARK

    search_bar = WeatherSearchBar(page=page)
    page.add(
        Container(
            content=Column(
                controls=[
                    Container(
                        border_radius=40,
                        bgcolor=Colors.BLACK,
                        content=search_bar
                    ),
                    city,
                    temperature
                ]
            )
        )
    )

app(target=main)