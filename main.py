from cookiecutter.utils import work_in
from flet import *
import requests

API_KEY = 'e68c4de4bbb92f4801d22d1a96059b1d'


class StringField(Text):
    def __init__(self, size, value, color=Colors.WHITE, text_align=TextAlign.JUSTIFY):
        super().__init__()
        self.value = value
        self.size = size
        self.color = color
        self.weight = FontWeight.BOLD
        self.text_align = text_align


class CurrentWeather:
    def __init__(self, page):
        self.page = page
        self.error_bottom_sheet = BottomSheet(
            content=Container(
                padding=35,
                content=StringField(value="", size=25, text_align=TextAlign.CENTER)
            ),
            dismissible=True,
            show_drag_handle=True
        )

    def update_screen_info(self, result):
        temperature.value = str(result['current']['temperature']) + chr(176)
        wind_dir.value = result['current']['wind_dir']
        wind_speed.value = result['current']['wind_speed']
        humidity.value = str(result['current']['humidity']) + '%'
        city.value = result['location']['name'].title()
        self.page.overlay.clear()
        self.page.update()


    def get_weather(self, city_for_search):
        params = {
            "lang": 'ru',
            "access_key": API_KEY,
            "query": city_for_search
        }
        request = requests.get(f"http://api.weatherstack.com/current", params=params)
        print(request.status_code)
        if request.status_code == 200:
            result = request.json()
            if "success" not in result:
                self.update_screen_info(request.json())
            else:
                self.error_bottom_sheet.content.content.value = "Упс, подобного города не нашлось:(\nМожет вы сделали опечатку?"
                self.page.overlay.append(self.error_bottom_sheet)
                self.page.update()
                self.page.open(self.error_bottom_sheet)

        else:
            self.error_bottom_sheet.content.content.value = "Упс, кажется, нам не удалось отправить запрос\tМожет попробуем еще раз?"
            self.page.overlay.append(self.error_bottom_sheet)
            self.page.open(self.error_bottom_sheet)


    print(request.json())



class WeatherSearchBar(SearchBar):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.full_screen = True
        self.bar_hint_text = "Где посмотрим погоду?"
        self.on_submit = self.get_search_request_from_bar
        self.on_tap = lambda e: self.open_view()
        self.cities = []
        self.error_bottom_sheet = BottomSheet(
                content=Container(
                    padding=35,
                    content=StringField(value="", size=25, text_align=TextAlign.CENTER)
                ),
                dismissible=True,
                show_drag_handle=True
            )
        self.controls = []
        self.base_cities = ['Москва', "Лондон", "Париж", "Нью-Йорк", "Токио", "Сидней"]
        self.update_search_history()

    def update_search_history(self):
        self.controls.clear()
        for i in self.page.client_storage.get('cities')[::-1]:
            self.controls.append(
                ListTile(title=StringField(value=i, size=15), on_click=self.get_search_request_from_control, data=i, trailing=Icon(name=Icons.ACCESS_TIME_ROUNDED))
            )
        for i in self.base_cities:
            self.controls.append(
                ListTile(title=StringField(value=i, size=15), on_click=self.get_search_request_from_control, data=i, trailing=Icon(name=Icons.ARROW_OUTWARD_ROUNDED))
            )



    def get_search_request_from_control(self, e):
        self.get_weather(e.control.data)

    def get_search_request_from_bar(self, e):
        self.get_weather(e.data)

    def get_weather(self, query):
        params = {
            "lang": 'ru',
            "access_key": API_KEY,
            "query": query
        }
        cities = self.page.client_storage.get('cities')
        if query in cities:
            cities.remove(query)
        if query not in self.base_cities:
            cities.append(query)
        self.page.client_storage.set('cities', cities)
        print(cities)
        self.update_search_history()
        request = requests.get(f"http://api.weatherstack.com/current", params=params)
        if request.status_code == 200:
            result = request.json()
            print(result)
            self.close_view()
            self.page.update()
            if "success" not in result:
                current_weather.update_screen_info(result)
            else:
                self.error_bottom_sheet.content.content.value = "Упс, подобного города не нашлось:(\nМожет вы сделали опечатку?"
                self.page.overlay.append(self.error_bottom_sheet)
                self.page.update()
                self.page.open(self.error_bottom_sheet)
        else:
            self.error_bottom_sheet.content.content.value = "Упс, кажется, нам не удалось отправить запрос\tМожет попробуем еще раз?"
            self.page.overlay.append(self.error_bottom_sheet)
            self.page.open(self.error_bottom_sheet)
        #print(self.page.client_storage.get('cities'))




#   москва
# e68c4de4bbb92f4801d22d1a96059b1d
# API_KEY = 'e68c4de4bbb92f4801d22d1a96059b1d'
# print(request['current']['weather_descriptions'])
# from translate import Translator
# translator= Translator(from_lang="english", to_lang="russian")
# translation = translator.translate('hi')
# print(translation)
current_weather = CurrentWeather(page=0)
temperature = StringField(size=95, value="temp", color=Colors.BLACK)
city = StringField(size=30, value="city")
wind_speed = StringField(value="speed", size=20)
wind_dir = StringField(value="dir", size=20)
humidity = StringField(value="humidity", size=20)


def main(page: Page):
    page.title = "WeatherCheck"
    page.bgcolor = Colors.BLUE
    page.window.width = 350
    page.window.height = 700
    page.theme_mode = ThemeMode.DARK
    #page.client_storage.clear()


    def first_start():
        page.client_storage.set('cities', [])
        page.overlay.append(
            Container(
                width=800,
                height=800,
                bgcolor=Colors.WHITE,
                content=Column(
                    controls=[
                        Container(
                            content=StringField(
                                value="Добро пожаловать в WeatherCheck!",
                                color=Colors.BLUE_700,
                                size=50,
                                text_align=TextAlign.CENTER
                            ),
                            margin=40
                        ),
                        WeatherSearchBar(page=page)
                    ]
                )
            )
        )
        page.update()

    current_weather.page = page
    if page.client_storage.contains_key('cities'):
        print(page.client_storage.get('cities'))
        current_weather.get_weather(page.client_storage.get('cities')[-1])
    else:
        first_start()

    search_bar = WeatherSearchBar(page=page)

    page.add(
        Container(
            content=Column(
                controls=[
                    Container(
                        border_radius=40,
                        bgcolor=Colors.BLACK,
                        content=search_bar,
                        margin=20,
                    ),
                    city,
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Container(
                                content=temperature,
                                width=250,
                                height=250,
                                shape=BoxShape.CIRCLE,
                                bgcolor=Colors.WHITE,
                                alignment=alignment.center
                            )
                        ]
                    ),
                    Container(
                        bgcolor=Colors.BLACK,
                        margin=20,
                        content=Row(
                            vertical_alignment=CrossAxisAlignment.START,
                            controls=[
                                Column(
                                    expand=1,
                                    controls=[
                                        Icon(name=Icons.AIR_ROUNDED),
                                        wind_speed,
                                        wind_dir
                                    ]
                                ),
                                Column(
                                    expand=1,
                                    controls=[
                                        Icon(name=Icons.WATER_DROP_ROUNDED),
                                        humidity
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )
    )

app(target=main)