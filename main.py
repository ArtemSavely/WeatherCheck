from translate import Translator
from flet import *
import requests

api = '06a63ec768msh6db0228a9020b71p167e4cjsn1cfb40d489bc'
url = "https://weatherapi-com.p.rapidapi.com/current.json"
#{'location': {'name': 'Лондон', 'region': 'City of London, Greater London', 'country': 'Великобритания', 'lat': 51.5171, 'lon': -0.1062, 'tz_id': 'Europe/London', 'localtime_epoch': 1747411418, 'localtime': '2025-05-16 17:03'}, 'current': {'last_updated_epoch': 1747411200, 'last_updated': '2025-05-16 17:00', 'temp_c': 18.0, 'temp_f': 64.4, 'is_day': 1, 'condition': {'text': 'Sunny', 'icon': '//cdn.weatherapi.com/weather/64x64/day/113.png', 'code': 1000}, 'wind_mph': 12.8, 'wind_kph': 20.5, 'wind_degree': 16, 'wind_dir': 'NNE', 'pressure_mb': 1024.0, 'pressure_in': 30.24, 'precip_mm': 0.0, 'precip_in': 0.0, 'humidity': 49, 'cloud': 25, 'feelslike_c': 18.0, 'feelslike_f': 64.4, 'windchill_c': 17.2, 'windchill_f': 63.0, 'heatindex_c': 17.2, 'heatindex_f': 63.0, 'dewpoint_c': 5.2, 'dewpoint_f': 41.4, 'vis_km': 10.0, 'vis_miles': 6.0, 'uv': 2.2, 'gust_mph': 14.7, 'gust_kph': 23.6}}

headers = {
    "x-rapidapi-lang": 'ru',
	"x-rapidapi-key": api,
	"x-rapidapi-host": "weatherapi-com.p.rapidapi.com"
}

class StringField(Text):
    def __init__(self, size, value, color=Colors.WHITE, text_align=TextAlign.JUSTIFY):
        super().__init__()
        self.value = value
        self.size = size
        self.color = color
        self.weight = FontWeight.BOLD
        self.text_align = text_align


class WeatherInfoContainer(Container):
    def __init__(self, controls):
        super().__init__()
        self.expand = True
        self.padding = 20
        self.bgcolor = "#40000000"
        self.border_radius = 30
        self.height = 140
        self.content = Column(
            controls=controls
        )


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
        self.full_weather_result = ''

    def update_screen_info(self, result):
        translator = Translator(from_lang="english", to_lang="russian")
        directions = {
            'N': "С",
            'S': 'Ю',
            'W': 'З',
            'E': 'В'
        }
        self.full_weather_result = result
        temperature.value = str(int(result['current']['temp_c'])) + chr(176)
        wind_dir.value = ''.join([directions[i] for i in result['current']['wind_dir']])
        wind_speed.value = str(int(result['current']['wind_kph'])) + ' км/ч'
        humidity.value = str(result['current']['humidity']) + '%'
        condition.value = translator.translate(result['current']['condition']['text'])
        pressure.value = str(int(result['current']['pressure_mb'])) + ' мбар'
        city.value = result['location']['name'].title()
        self.page.bgcolor = backgrounds[self.full_weather_result['current']['is_day']]
        print(self.page.bgcolor)
        self.page.overlay.clear()
        self.page.update()


    def get_weather(self, city_for_search):
        params = {'q': city_for_search}
        request = requests.get(url, headers=headers, params=params)
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
        params = {'q': query}
        request = requests.get(url, headers=headers, params=params)
        cities = self.page.client_storage.get('cities')
        if query in cities:
            cities.remove(query)
        if query not in self.base_cities:
            cities.append(query)
        self.page.client_storage.set('cities', cities)
        print(cities)
        self.update_search_history()
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
condition = StringField(value="condition", size=20)
pressure = StringField(value="pressure", size=20)
backgrounds = ['#0a2667', Colors.BLUE_700]


def main(page: Page):
    page.title = "WeatherCheck"
    page.window.width = 350
    page.window.height = 700
    page.theme_mode = ThemeMode.DARK
    page.scroll = True
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
    page.bgcolor = backgrounds[current_weather.full_weather_result['current']['is_day']]


    page.add(
        Container(
            content=Column(
                controls=[
                    Container(
                        border_radius=40,
                        content=search_bar,
                        margin=20,
                    ),
                    city,
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Stack(
                                clip_behavior=ClipBehavior.NONE,
                                controls=[
                                    Container(
                                        width=250,
                                        height=250,
                                        shape=BoxShape.CIRCLE,
                                        bgcolor=Colors.WHITE,
                                        alignment=alignment.center
                                    ),
                                    Container(
                                        content=Image(src='assets/cloud_sun.png', height=120),
                                        left=35,
                                        top=20
                                    ),
                                    Container(
                                        content=temperature, left=95, top=90, width=170, alignment=alignment.center, #bgcolor=Colors.BLACK
                                    ),
                                ]
                            )
                        ]
                    ),
                    Container(
                        margin=30,
                        content=condition
                    ),
                    Container(
                        #bgcolor=Colors.BLACK,
                        margin=20,
                        content=Column(
                            #vertical_alignment=CrossAxisAlignment.START,
                            controls=[
                                Row(
                                    controls=[
                                        WeatherInfoContainer(controls=[Row([StringField(value="Ветер", size=12), Icon(name=Icons.AIR_ROUNDED)]), wind_speed, wind_dir]),
                                        WeatherInfoContainer(controls=[Row([StringField(value="Влажность", size=12), Icon(name=Icons.WATER_DROP_ROUNDED)]), humidity])
                                    ]
                                ),
                                Row(
                                    controls=[
                                        WeatherInfoContainer(controls=[Row([StringField(value='Давление', size=12), Icon(name=Icons.ARROW_DOWNWARD_ROUNDED), pressure])])
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )
    )

app(target=main, assets_dir='assets')