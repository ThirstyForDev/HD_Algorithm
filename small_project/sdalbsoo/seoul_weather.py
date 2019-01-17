import os
import datetime

import requests


today_date = datetime.date.today()
appid = os.environ["APPID"]
city = input("city 입력(서울=>seoul): ")
url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={appid}"


def Kelvin_to_Celsi(temperature):
    return round(float(temperature)-273.15)


def condition_wind(wind_speed):
    wind_speed = int(wind_speed)
    if (0.3 < wind_speed <= 3.3):
        return "여린 바람, 외출하기 좋음"
    elif (3.4 < wind_speed <= 5.4):
        return "중간 바람, 외출하기 좋음"
    elif (5.5 < wind_speed <= 10.7):
        return "쎈 바람, 외출...?"
    elif (10.7 < wind_speed <= 13.8):
        return "외출 자제"
    else:
        return "외출 하지 말 것"


def get_weather_info():
    res = requests.get(url)
    data = res.json()
    data = data['list']
    for i in range(0, 5):
        date = data[i*8]
        extract_weather_info(date)


def extract_weather_info(date):
    weather_date = date['dt_txt']
    weather = date['weather'][0]['description']
    temperature = date['main']['temp']
    wind_speed = date['wind']['speed']
    humid = date['main']['humidity']

    print_weather_info(weather_date, weather, temperature, wind_speed, humid)


def print_weather_info(weather_date, weather, temperature, wind, humid):
    print(f"{weather_date} {city}의 날씨: ", weather)
    print(f"{weather_date} {city}의 온도: ", Kelvin_to_Celsi(temperature))
    print(f"{weather_date} {city}의 바람세기: ", condition_wind(wind))
    print(f"{weather_date} {city}의 습도: ", humid, "%")
    print('='*15)


def main():
    get_weather_info()


if __name__ == '__main__':
    main()
