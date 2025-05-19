from translate import Translator
from flet import *
import requests
import datetime

api = '06a63ec768msh6db0228a9020b71p167e4cjsn1cfb40d489bc'
#{'location': {'name': 'Лондон', 'region': 'City of London, Greater London', 'country': 'Великобритания', 'lat': 51.5171, 'lon': -0.1062, 'tz_id': 'Europe/London', 'localtime_epoch': 1747411418, 'localtime': '2025-05-16 17:03'}, 'current': {'last_updated_epoch': 1747411200, 'last_updated': '2025-05-16 17:00', 'temp_c': 18.0, 'temp_f': 64.4, 'is_day': 1, 'condition': {'text': 'Sunny', 'icon': '//cdn.weatherapi.com/weather/64x64/day/113.png', 'code': 1000}, 'wind_mph': 12.8, 'wind_kph': 20.5, 'wind_degree': 16, 'wind_dir': 'NNE', 'pressure_mb': 1024.0, 'pressure_in': 30.24, 'precip_mm': 0.0, 'precip_in': 0.0, 'humidity': 49, 'cloud': 25, 'feelslike_c': 18.0, 'feelslike_f': 64.4, 'windchill_c': 17.2, 'windchill_f': 63.0, 'heatindex_c': 17.2, 'heatindex_f': 63.0, 'dewpoint_c': 5.2, 'dewpoint_f': 41.4, 'vis_km': 10.0, 'vis_miles': 6.0, 'uv': 2.2, 'gust_mph': 14.7, 'gust_kph': 23.6}}
url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
querystring1 = {"q":"London","days":"2"}
headers = {
    "x-rapidapi-lang": 'ru',
	"x-rapidapi-key": api,
	"x-rapidapi-host": "weatherapi-com.p.rapidapi.com"
}

def get_weather_icon_src(condition, is_day):
    weather_icons = {
        'sunny': 'sun',
        'clear': 'moon',
        'partly cloudy': ['moon_cloud', 'cloud_sun'],
        'cloudy': 'cloud',
        'overcast': 'overcast',
        'mist': 'fog',
        'patchy rain possible': ['rain_night', 'rain_sun'],
        'patchy snow possible': ['snow_night', 'snow_sun'],
        'patchy sleet possible': 'snow_rain',
        'patchy freezing drizzle possible': 'snow_rain',
        'thundery outbreaks possible': 'outbrakes',
        'blowing snow': 'snow',
        'blizzard': 'wind',
        'fog': 'fog',
        'freezing fog': 'fog',
        'patchy light drizzle': ['rain_night', 'rain_sun'],
        'light drizzle': ['rain_night', 'rain_sun'],
        'freezing drizzle': 'snow_rain',
        'heavy freezing drizzle': 'snow_rain',
        'patchy light rain': ['rain_night', 'rain_sun'],
        'light rain': 'rain',
        'moderate rain at times': 'rain',
        'moderate rain': 'rain',
        'heavy rain at times': 'heavy_rain',
        'heavy rain': 'heavy_rain',
        'light freezing rain': ['rain_night', 'rain_sun'],
        'moderate or heavy freezing rain': 'heavy_rain',
        'light sleet': 'snow_rain',
        'moderate or heavy sleet': 'snow_rain',
        'patchy light snow': ['snow_night', 'snow_sun'],
        'light snow': 'snow',
        'patchy moderate snow': ['snow_night', 'snow_sun'],
        'moderate snow': 'snow',
        'patchy heavy snow': ['snow_night', 'snow_sun'],
        'heavy snow': 'snow',
        'ice pellets': 'ice',
        'light rain shower': ['rain_night', 'rain_sun'],
        'moderate or heavy rain shower': 'rain',
        'torrential rain shower': 'heavy_rain',
        'light sleet showers': 'snow_rain',
        'moderate or heavy sleet showers': 'snow_rain',
        'light snow showers': 'snow',
        'moderate or heavy snow showers': 'snow',
        'light showers of ice pellets': 'ice',
        'moderate or heavy showers of ice pellets': 'ice',
        'patchy light rain with thunder': 'storm',
        'moderate or heavy rain with thunder': 'storm',
        'patchy light snow with thunder': 'storm_snow',
        'moderate or heavy snow with thunder': 'storm_snow'
    }
    if condition.lower() in weather_icons:
        icon_result = weather_icons[condition.lower()]
    else:
        if 'rain' in condition.lower() or 'drizzle' in condition.lower():
            icon_result = 'rain'
        else:
            icon_result = ['moon_cloud', 'cloud_sun']
    if type(icon_result) == list:
        icon_src = f'assets/{icon_result[is_day]}.png'
    else:
        icon_src = f'assets/{icon_result}.png'
    return icon_src


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


class HourForecastInfo(Container):
    def __init__(self, forecast):
        super().__init__()
        self.margin = margin.only(left=7)
        self.content = Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                StringField(value=forecast['time'][-5:], size=12),
                Image(src=get_weather_icon_src(forecast['condition']['text'], is_day=forecast['is_day']), height=20),
                StringField(value=f'{str(int(forecast['temp_c']))}{chr(176)}', size=12)
            ]
        )


class DayForecastInfo(Container):
    def __init__(self, forecast):
        super().__init__()
        self.content = Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                StringField(value=self.get_day_from_date(forecast), size=16),
                Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Container(content=Image(src=get_weather_icon_src(forecast['day']['condition']['text'], is_day=1), height=20)),
                        Container(content=StringField(value=f'{str(int(forecast['day']['maxtemp_c']))}{chr(176)}', size=16)),
                        Container(content=StringField(value=f'{str(int(forecast['day']['mintemp_c']))}{chr(176)}', size=16))
                    ]
                )
            ]
        )
        self.border_radius = 30
        self.padding = 20
        self.height = 70
        self.bgcolor = "#40000000"
        self.margin = margin.symmetric(horizontal=10)

    def get_day_from_date(self, forecast):
        days = {
            0: 'Понедельник',
            1: 'Вторник',
            2: 'Среда',
            3: 'Четверг',
            4: 'Пятница',
            5: 'Суббота',
            6: 'Воскресенье'

        }
        y, m, d = [int(i) for i in forecast['date'].split('-')]
        date = datetime.datetime(y, m, d)
        return days[date.weekday()]


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
        condition_original_text = result['current']['condition']['text']
        icon_src = get_weather_icon_src(condition_original_text, result['current']['is_day'])
        weather_icon_image.src = icon_src
        condition.value = f'{translator.translate(condition_original_text)}\nОщущается как {int(result['current']['feelslike_c'])}{chr(176)}'
        pressure.value = str(int(result['current']['pressure_mb'])) + ' мбар'
        vis_km.value = str(int(result['current']['vis_km'])) + ' км'
        city.value = result['location']['name'].title()
        sunset.value = self.full_weather_result['forecast']['forecastday'][0]['astro']['sunset']
        sunrise.value = self.full_weather_result['forecast']['forecastday'][0]['astro']['sunrise']
        self.page.bgcolor = backgrounds[self.full_weather_result['current']['is_day']]
        day_forecast.content.controls.clear()
        for i in range(3):
            day_forecast.content.controls.append(
                DayForecastInfo(current_weather.full_weather_result['forecast']['forecastday'][i])
            )
        current_hour = int(result['location']['localtime'][11:13])
        hour_forecast.content.controls.clear()
        for i in range(current_hour, 24):
            hour_forecast.content.controls.append(
                HourForecastInfo(result['forecast']['forecastday'][0]['hour'][i])
            )
        for i in range(0, current_hour):
            hour_forecast.content.controls.append(
                HourForecastInfo(result['forecast']['forecastday'][1]['hour'][i])
            )
        self.page.overlay.clear()
        self.page.update()


    def get_weather(self, city_for_search):
        params = {'q': city_for_search, "days":"3"}
        request = requests.get(url, headers=headers, params=params)
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


class WeatherSearchBar(SearchBar):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.full_screen = True
        self.bar_bgcolor = Colors.GREY_900
        self.divider_color = Colors.WHITE
        self.bar_hint_text = "Где посмотрим погоду?"
        self.view_hint_text = 'Где посмотрим погоду?'
        self.view_bgcolor = Colors.BLUE_900
        self.bar_trailing = [IconButton(Icons.SEARCH_ROUNDED, icon_color=Colors.WHITE)]
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

    def del_list_tile(self, e):
        recent = self.page.client_storage.get('cities')
        recent.remove(e.control.data)
        self.page.client_storage.set('cities', recent)
        self.controls.remove(e.control)
        snack_bar = SnackBar(content=Row(
            [StringField(value=f"Поисковый запрос удален", size=15), Icon(Icons.DELETE, color=Colors.WHITE, size=25)]),
            bgcolor=Colors.BLUE_900)
        self.close_view()
        self.page.open(snack_bar)
        self.page.update()

    def update_search_history(self):
        self.controls.clear()
        for i in self.page.client_storage.get('cities')[::-1]:
            self.controls.append(
                ListTile(title=StringField(value=i, size=15), on_click=self.get_search_request_from_control, on_long_press=self.del_list_tile, data=i, trailing=Icon(name=Icons.ACCESS_TIME_ROUNDED))
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
        params = {'q': query, "days":"3"}
        request = requests.get(url, headers=headers, params=params)
        cities = self.page.client_storage.get('cities')
        if query in cities:
            cities.remove(query)
        #if query not in self.base_cities:
        cities.append(query)
        self.page.client_storage.set('cities', cities)
        self.update_search_history()
        if request.status_code == 200:
            result = request.json()
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


current_weather = CurrentWeather(page=0)
temperature = StringField(size=90, value="temp", color=Colors.WHITE)
city = StringField(size=30, value="city")
wind_speed = StringField(value="speed", size=20)
wind_dir = StringField(value="dir", size=20)
humidity = StringField(value="humidity", size=20)
condition = StringField(value="condition", size=20)
pressure = StringField(value="pressure", size=20)
vis_km = StringField(value='vis_km', size=20)
backgrounds = ['#0a2667', Colors.BLUE_700]
weather_icon_image = Image(src='assets/cloud_sun.png', height=120)
sunset = StringField(value='s', size=18)
sunrise = StringField(value='s', size=18)
day_forecast = Container(
    content=Column(
        controls=[]
    )
)
hour_forecast = Container(
    border_radius=30,
    padding=30,
    bgcolor = "#40000000",
    content=Row(
        controls=[],
        scroll=ScrollMode.HIDDEN
    )
)


def main(page: Page):
    page.title = "WeatherCheck"
    page.window.width = 350
    page.window.height = 700
    page.theme_mode = ThemeMode.DARK
    page.scroll = ScrollMode.HIDDEN
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
                                size=30,
                                text_align=TextAlign.CENTER
                            ),
                            margin=40
                        ),
                        Container(
                            alignment=alignment.center,
                            border_radius=40,
                            content=WeatherSearchBar(page=page),
                            margin=20,
                        ),
                    ]
                )
            )
        )
        page.update()

    current_weather.page = page
    if page.client_storage.contains_key('cities'):
        current_weather.get_weather(page.client_storage.get('cities')[-1])
        page.bgcolor = backgrounds[current_weather.full_weather_result['current']['is_day']]
    else:
        first_start()

    search_bar = WeatherSearchBar(page=page)


    page.add(
        Container(
            content=Column(
                controls=[
                    Container(
                        alignment=alignment.center,
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
                                        alignment=alignment.center
                                    ),
                                    Container(
                                        content=weather_icon_image,
                                        left=20,
                                        top=20
                                    ),
                                    Container(
                                        content=temperature, left=65, top=90, width=220, alignment=alignment.center,
                                    ),
                                ]
                            )
                        ]
                    ),
                    Container(
                        margin=30,
                        content=condition
                    ),
                    Container(content=hour_forecast, margin=10),
                    Container(
                        margin=10,
                        content=Column(
                            controls=[
                                Row(
                                    controls=[
                                        WeatherInfoContainer(controls=[Row([Container(content=Icon(name=Icons.AIR_ROUNDED), margin=-4), Container(content=StringField(value='Ветер', size=12), margin=-4)]), wind_speed, wind_dir]),
                                        WeatherInfoContainer(controls=[Row([Container(content=Icon(name=Icons.WATER_DROP_ROUNDED), margin=-4), Container(content=StringField(value='Влажность', size=12), margin=-4)]), humidity])
                                    ]
                                ),
                                Row(
                                    controls=[
                                        WeatherInfoContainer(controls=[Row([Container(content=Icon(name=Icons.ARROW_DOWNWARD_ROUNDED), margin=-4), Container(content=StringField(value='Давление', size=12), margin=-4)]), pressure]),
                                        WeatherInfoContainer(controls=[Row([Container(content=Icon(name=Icons.VISIBILITY_ROUNDED), margin=-4), Container(content=StringField(value='Видимость', size=12), margin=-4)]), vis_km])
                                    ]
                                )
                            ]
                        )
                    ),
                    Container(
                        border_radius=30,
                        padding=20,
                        margin=10,
                        bgcolor="#40000000",
                        content=Row(
                            alignment=MainAxisAlignment.SPACE_AROUND,
                            controls=[
                                Column(
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Image(src='assets/sunrise.png', height=40),
                                        StringField(value='Восход', size=16),
                                        sunrise
                                    ]
                                ),
                                Column(
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Image(src='assets/sunset.png', height=40),
                                        StringField(value='Закат', size=16),
                                        sunset
                                    ]
                                )
                            ]
                        )
                    ),
                    StringField(value='Прогноз погоды на 3 дня:', size=20),
                    day_forecast
                ]
            )
        )
    )

app(target=main, assets_dir='assets')