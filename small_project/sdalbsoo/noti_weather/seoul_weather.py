import os
import sys
import time

import requests

from slack import SlackMessage
from slack import NotiTemplate


APPID = os.environ["APPID"]
APIKEY = os.environ["APIKEY"]
CITY = input("city 입력(서울=>seoul): ")
URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={APPID}"
URL_PM = f"http://openapi.airkorea.or.kr/openapi/services/rest/\
ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?\
stationName=%EA%B0%95%EB%82%A8%EA%B5%AC&dataTerm=month\
&pageNo=1&numOfRows=10&ServiceKey={APIKEY}&ver=1.3&_returnType=json"


def Kelvin_to_Celsi(temperature):
    return round(float(temperature)-273.15)


def condition_wind(wind_speed):
    if (0.3 < int(wind_speed) <= 3.3):
        return "여린 바람, 외출하기 좋음"
    elif (3.4 < int(wind_speed) <= 5.4):
        return "중간 바람, 외출하기 좋음"
    elif (5.5 < int(wind_speed) <= 10.7):
        return "쎈 바람, 외출...?"
    elif (10.7 < int(wind_speed) <= 13.8):
        return "외출 자제"
    else:
        return "외출 하지 말 것"


def get_weather_date():
    res = requests.get(URL)
    res_PM = requests.get(URL_PM)
    raw_data = res.json()
    data = raw_data['list']

    data_PM = res_PM.json()

    print(res_PM)

    print_weather_PM(data_PM)
    extract_weather_info(data[0])


def print_weather_PM(data_PM):
    text_PM = (
        f"(강남)미세먼지 농도: {data_PM['list'][0]['pm10Value']}\n"
        f"미세먼지 등급: {print_PM_grade(data_PM['list'][0]['pm10Grade'])}\n"
        f"(강남)초미세먼지 농도: {data_PM['list'][0]['pm25Value']}\n"
        f"초미세먼지 등급: {print_PM_grade(data_PM['list'][0]['pm25Grade'])}"
    )
    template = NotiTemplate("오늘의 미세먼지", text_PM)
    slack_message = SlackMessage()
    slack_message.send(template)


def print_PM_grade(grade_PM):
    if (int(grade_PM) == 1):
        return '좋음'
    if (int(grade_PM) == 2):
        return '보통'
    if (int(grade_PM) == 3):
        return '나쁨'
    if (int(grade_PM) == 4):
        return '매우나쁨 그러니 외출 금지'


def extract_weather_info(date):
    weather_date = date['dt_txt']
    weather = date['weather'][0]['description']
    temperature = date['main']['temp']
    wind_speed = date['wind']['speed']
    humid = date['main']['humidity']

    print_weather_info(weather_date, weather, temperature, wind_speed, humid)


def print_weather_info(weather_date, weather, temperature, wind, humid):
    text_weather = (
        f"{weather_date} {CITY}의 날씨: {weather}\n"
        f"{weather_date} {CITY}의 온도: {Kelvin_to_Celsi(temperature)}\n"
        f"{weather_date} {CITY}의 바람세기: {condition_wind(wind)}\n"
        f"{weather_date} {CITY}의 습도: {humid}%\n"
    )
    print(text_weather)
    template = NotiTemplate("오늘의 날씨", text_weather)
    slack_message = SlackMessage()
    slack_message.send(template)


def main():
    loop_time = sys.argv[1]  # 864000
    while 1:
        get_weather_date()
        time.sleep(int(loop_time))


if __name__ == '__main__':
    main()
