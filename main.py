from flet import *
import requests



# e68c4de4bbb92f4801d22d1a96059b1d
API_KEY = 'e68c4de4bbb92f4801d22d1a96059b1d'
params = {
    "lang": 'ru',
    "access_key": API_KEY,
    "query": 'Москва'
}
request = requests.get(f"http://api.weatherstack.com/current", params=params).json()
print(request)
print(request['current']['weather_descriptions'])
from translate import Translator
translator= Translator(from_lang="english", to_lang="russian")
translation = translator.translate('hi')
print(translation)

# def main(Page: page):
#     page.title = "WeatherCheck"
#     page.bgcolor = colors.BLACK
#
#
#
# flet.app(main)