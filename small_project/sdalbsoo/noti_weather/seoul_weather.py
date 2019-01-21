import os
import sys
import time

import requests

from slack import SlackMessage
from slack import NotiTemplate


class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Setting(metaclass=Singleton):
    def __init__(self, appid, apikey, city, url, url_pm):
        self.APPID = appid
        self.APIKEY = apikey
        self.CITY = city
        self.URL = url
        self.URL_PM = url_pm


class Weather():
    def __init__(self, appid, apikey, city, url, url_pm):
        self.setting = Setting(appid, apikey, city, url, url_pm)

    def kelvin_to_celsi(self, temperature):
        return round(float(temperature)-273.15)

    def wind_speed_to_message(self, wind_speed):
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

    def PM_grade_to_message(self, grade_PM):
        if (int(grade_PM) == 1):
            return '좋음'
        if (int(grade_PM) == 2):
            return '보통'
        if (int(grade_PM) == 3):
            return '나쁨'
        if (int(grade_PM) == 4):
            return '매우나쁨 그러니 외출 금지'

    def get_weather_data(self):
        res = requests.get(self.setting.URL)
        raw_data = res.json()
        data = raw_data['list']

        res_PM = requests.get(self.setting.URL_PM)
        data_PM = res_PM.json()

        self.print_weather_PM(data_PM)
        self.extract_weather_info(data[0])

    def print_weather_PM(self, data_PM):
        text_PM = (
            f"(강남)미세먼지 농도: {data_PM['list'][0]['pm10Value']}\n"
            f"미세먼지 등급: {self.PM_grade_to_message(data_PM['list'][0]['pm10Grade'])}\n"  # noqa
            f"(강남)초미세먼지 농도: {data_PM['list'][0]['pm25Value']}\n"
            f"초미세먼지 등급: {self.PM_grade_to_message(data_PM['list'][0]['pm25Grade'])}"  # noqa
        )
        self.send_to_slack("오늘의 미세먼지", text_PM)

    def extract_weather_info(self, date):
        weather_date = date['dt_txt']
        weather = date['weather'][0]['description']
        temperature = date['main']['temp']
        wind_speed = date['wind']['speed']
        humid = date['main']['humidity']

        self.print_weather_info(
            weather_date, weather, temperature, wind_speed, humid
        )

    def print_weather_info(self, weather_date, weather, temperature, wind, humid):  # noqa
        text_weather = (
            f"{weather_date} {self.setting.CITY}의 날씨: {weather}\n"
            f"{weather_date} {self.setting.CITY}의 온도: {self.kelvin_to_celsi(temperature)}\n"  # noqa
            f"{weather_date} {self.setting.CITY}의 바람세기: {self.wind_speed_to_message(wind)}\n"  # noqa
            f"{weather_date} {self.setting.CITY}의 습도: {humid}%\n"
        )
        self.send_to_slack("오늘의 날씨", text_weather)

    def send_to_slack(self, kind, text_data):
        slack_message = SlackMessage()
        template = NotiTemplate(kind, text_data)
        slack_message.send(template)


def main():
    loop_time = sys.argv[1]  # 864000
    APPID = os.environ["APPID"]
    APIKEY = os.environ["APIKEY"]
    CITY = input("city 입력(서울=>seoul): ")
    URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={APPID}"  # noqa
    URL_PM = (
        f"http://openapi.airkorea.or.kr/openapi/services/rest/"
        f"ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?"
        f"stationName=%EA%B0%95%EB%82%A8%EA%B5%AC&dataTerm=month"
        f"&pageNo=1&numOfRows=10&ServiceKey={APIKEY}&ver=1.3&_returnType=json"
    )
    detect_weathter = Weather(APPID, APIKEY, CITY, URL, URL_PM)
    while 1:
        detect_weathter.get_weather_data()
        time.sleep(int(loop_time))


if __name__ == '__main__':
    main()
