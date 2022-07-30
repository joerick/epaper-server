from __future__ import annotations
from dataclasses import dataclass
import datetime
import os
from urllib.parse import urlencode
import requests
from dateutil.parser import isoparse
from PIL import Image
from dateutil.tz import tzutc

API_KEY = 'UZE0E9hka7EhwtEG0Ze7yJo46orLHgLX'

@dataclass
class Forecast:
    today: ForecastInterval
    hourly: list[ForecastInterval]

    @property
    def today_hours(self):
        today_start = self.today.startTime.replace(hour=6, minute=0, second=0, microsecond=0)
        today_end = today_start + datetime.timedelta(days=1)

        return [h for h in self.hourly if today_start <= h.startTime <= today_end]


@dataclass
class ForecastInterval:
    startTime: datetime.datetime
    precipitationIntensity: float
    precipitationProbability: float
    temperature: float
    temperatureApparent: float
    weatherCode: int
    weatherCodeFullDay: int | None
    windSpeed: float

    @staticmethod
    def from_json(data):
        return ForecastInterval(
            startTime=isoparse(data['startTime']),
            precipitationIntensity=data['values']['precipitationIntensity'],
            precipitationProbability=data['values']['precipitationProbability'],
            temperature=data['values']['temperature'],
            temperatureApparent=data['values']['temperatureApparent'],
            weatherCode=data['values']['weatherCode'],
            weatherCodeFullDay=data['values'].get('weatherCodeFullDay'),
            windSpeed=data['values']['windSpeed'],
        )


def get_weather() -> Forecast:
    query = urlencode({
        'location': '51.50717853040887,-0.24805243109767183',
        'fields': [
            'precipitationIntensity',
            'weatherCode',
            'windSpeed',
            'temperature',
            'temperatureApparent',
            'precipitationProbability',
            'weatherCodeFullDay',
        ],
        'startTime': 'now',
        'endTime': 'nowPlus48h',
        'units': 'metric',
        'timesteps': ['1h', '1d'],
        'apikey': API_KEY,
    }, doseq=True)
    url = f"https://api.tomorrow.io/v4/timelines?{query}"

    response = requests.request("GET", url, headers={"Accept": "application/json"})
    response.raise_for_status()

    json_data = response.json()
    timelines = json_data['data']['timelines']

    hourly_timeline = next(t for t in timelines if t['timestep'] == '1h')
    daily_timeline = next(t for t in timelines if t['timestep'] == '1d')

    json_hourly_values = hourly_timeline['intervals']
    json_daily_values = daily_timeline['intervals']

    hourly = [ForecastInterval.from_json(v) for v in json_hourly_values]
    today = ForecastInterval.from_json(json_daily_values[1])

    return Forecast(today=today, hourly=hourly)

def get_weather_test_data():
    return Forecast(today=ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 5, 0, tzinfo=tzutc()), precipitationIntensity=0.1641, precipitationProbability=10, temperature=23.18, temperatureApparent=23.18, weatherCode=1001, weatherCodeFullDay=1001, windSpeed=5), hourly=[ForecastInterval(startTime=datetime.datetime(2022, 7, 30, 15, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=24.38, temperatureApparent=24.38, weatherCode=1001, weatherCodeFullDay=None, windSpeed=3.69), ForecastInterval(startTime=datetime.datetime(2022, 7, 30, 16, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=24.34, temperatureApparent=24.34, weatherCode=1001, weatherCodeFullDay=None, windSpeed=3.32), ForecastInterval(startTime=datetime.datetime(2022, 7, 30, 17, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=24.61, temperatureApparent=24.61, weatherCode=1001, weatherCodeFullDay=None, windSpeed=3.58), ForecastInterval(startTime=datetime.datetime(2022, 7, 30, 18, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=24.18, temperatureApparent=24.18, weatherCode=1001, weatherCodeFullDay=None, windSpeed=3.68), ForecastInterval(startTime=datetime.datetime(2022, 7, 30, 19, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=23.06, temperatureApparent=23.06, weatherCode=1001, weatherCodeFullDay=None, windSpeed=3.19), ForecastInterval(startTime=datetime.datetime(2022, 7, 30, 20, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=22.29, temperatureApparent=22.29, weatherCode=1001, weatherCodeFullDay=None, windSpeed=3.03), ForecastInterval(startTime=datetime.datetime(2022, 7, 30, 21, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=21.5, temperatureApparent=21.5, weatherCode=1001, weatherCodeFullDay=None, windSpeed=2.89), ForecastInterval(startTime=datetime.datetime(2022, 7, 30, 22, 0, tzinfo=tzutc()), precipitationIntensity=0.0215, precipitationProbability=5, temperature=20.71, temperatureApparent=20.71, weatherCode=1001, weatherCodeFullDay=None, windSpeed=2.49), ForecastInterval(startTime=datetime.datetime(2022, 7, 30, 23, 0, tzinfo=tzutc()), precipitationIntensity=0.0605, precipitationProbability=10, temperature=20, temperatureApparent=20, weatherCode=1001, weatherCodeFullDay=None, windSpeed=2.66), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 0, 0, tzinfo=tzutc()), precipitationIntensity=0.0547, precipitationProbability=25, temperature=19.35, temperatureApparent=19.35, weatherCode=1001, weatherCodeFullDay=None, windSpeed=2.43), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 1, 0, tzinfo=tzutc()), precipitationIntensity=0.0615, precipitationProbability=30, temperature=18.75, temperatureApparent=18.75, weatherCode=1001, weatherCodeFullDay=None, windSpeed=2.49), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 2, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=18.61, temperatureApparent=18.61, weatherCode=1001, weatherCodeFullDay=None, windSpeed=2.25), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 3, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=18.67, temperatureApparent=18.67, weatherCode=1001, weatherCodeFullDay=None, windSpeed=2.68), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 4, 0, tzinfo=tzutc()), precipitationIntensity=0.0117, precipitationProbability=25, temperature=18.46, temperatureApparent=18.46, weatherCode=1001, weatherCodeFullDay=None, windSpeed=3.51), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 5, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=18.29, temperatureApparent=18.29, weatherCode=1001, weatherCodeFullDay=None, windSpeed=3.65), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 6, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=18.39, temperatureApparent=18.39, weatherCode=1001, weatherCodeFullDay=None, windSpeed=3.94), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 7, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=18.99, temperatureApparent=18.99, weatherCode=1001, weatherCodeFullDay=None, windSpeed=4.92), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 8, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=19.9, temperatureApparent=19.9, weatherCode=1001, weatherCodeFullDay=None, windSpeed=4.24), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 9, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=20.66, temperatureApparent=20.66, weatherCode=1001, weatherCodeFullDay=None, windSpeed=4.56), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 10, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=21.77, temperatureApparent=21.77, weatherCode=1001, weatherCodeFullDay=None, windSpeed=5), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 11, 0, tzinfo=tzutc()), precipitationIntensity=0.1641, precipitationProbability=5, temperature=21.93, temperatureApparent=21.93, weatherCode=1001, weatherCodeFullDay=None, windSpeed=4.62), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 12, 0, tzinfo=tzutc()), precipitationIntensity=0.1035, precipitationProbability=10, temperature=21.91, temperatureApparent=21.91, weatherCode=1001, weatherCodeFullDay=None, windSpeed=4.42), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 13, 0, tzinfo=tzutc()), precipitationIntensity=0.1025, precipitationProbability=10, temperature=22.66, temperatureApparent=22.66, weatherCode=1001, weatherCodeFullDay=None, windSpeed=4.27), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 14, 0, tzinfo=tzutc()), precipitationIntensity=0.1094, precipitationProbability=10, temperature=23.06, temperatureApparent=23.06, weatherCode=1001, weatherCodeFullDay=None, windSpeed=4.14), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 15, 0, tzinfo=tzutc()), precipitationIntensity=0.0986, precipitationProbability=5, temperature=23.18, temperatureApparent=23.18, weatherCode=1001, weatherCodeFullDay=None, windSpeed=3.83), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 16, 0, tzinfo=tzutc()), precipitationIntensity=0.1406, precipitationProbability=5, temperature=22.71, temperatureApparent=22.71, weatherCode=1001, weatherCodeFullDay=None, windSpeed=3.41), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 17, 0, tzinfo=tzutc()), precipitationIntensity=0.1211, precipitationProbability=5, temperature=22.59, temperatureApparent=22.59, weatherCode=1001, weatherCodeFullDay=None, windSpeed=2.92), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 18, 0, tzinfo=tzutc()), precipitationIntensity=0.1045, precipitationProbability=5, temperature=22.1, temperatureApparent=22.1, weatherCode=1001, weatherCodeFullDay=None, windSpeed=2.43), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 19, 0, tzinfo=tzutc()), precipitationIntensity=0.0947, precipitationProbability=5, temperature=21.51, temperatureApparent=21.51, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.71), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 20, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=21.02, temperatureApparent=21.02, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.25), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 21, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=20.27, temperatureApparent=20.27, weatherCode=1001, weatherCodeFullDay=None, windSpeed=0.88), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 22, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=19.76, temperatureApparent=19.76, weatherCode=1001, weatherCodeFullDay=None, windSpeed=0.77), ForecastInterval(startTime=datetime.datetime(2022, 7, 31, 23, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=19.3, temperatureApparent=19.3, weatherCode=1001, weatherCodeFullDay=None, windSpeed=0.83), ForecastInterval(startTime=datetime.datetime(2022, 8, 1, 0, 0, tzinfo=tzutc()), precipitationIntensity=0.0215, precipitationProbability=5, temperature=18.85, temperatureApparent=18.85, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.14), ForecastInterval(startTime=datetime.datetime(2022, 8, 1, 1, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=18.48, temperatureApparent=18.48, weatherCode=1102, weatherCodeFullDay=None, windSpeed=1.11), ForecastInterval(startTime=datetime.datetime(2022, 8, 1, 2, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=17.93, temperatureApparent=17.93, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.01), ForecastInterval(startTime=datetime.datetime(2022, 8, 1, 3, 0, tzinfo=tzutc()), precipitationIntensity=0.0127, precipitationProbability=5, temperature=17.64, temperatureApparent=17.64, weatherCode=1001, weatherCodeFullDay=None, windSpeed=0.8), ForecastInterval(startTime=datetime.datetime(2022, 8, 1, 4, 0, tzinfo=tzutc()), precipitationIntensity=0.0293, precipitationProbability=5, temperature=17.29, temperatureApparent=17.29, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.2), ForecastInterval(startTime=datetime.datetime(2022, 8, 1, 5, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=17.24, temperatureApparent=17.24, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.1), ForecastInterval(startTime=datetime.datetime(2022, 8, 1, 6, 0, tzinfo=tzutc()), precipitationIntensity=0.0186, precipitationProbability=5, temperature=17.56, temperatureApparent=17.56, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.29), ForecastInterval(startTime=datetime.datetime(2022, 8, 1, 7, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=18.1, temperatureApparent=18.1, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.3), ForecastInterval(startTime=datetime.datetime(2022, 8, 1, 8, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=18.84, temperatureApparent=18.84, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.33), ForecastInterval(startTime=datetime.datetime(2022, 8, 1, 9, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=19.95, temperatureApparent=19.95, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.03), ForecastInterval(startTime=datetime.datetime(2022, 8, 1, 10, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=21.45, temperatureApparent=21.45, weatherCode=1001, weatherCodeFullDay=None, windSpeed=0.49), ForecastInterval(startTime=datetime.datetime(2022, 8, 1, 11, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=22.82, temperatureApparent=22.82, weatherCode=1001, weatherCodeFullDay=None, windSpeed=0.28), ForecastInterval(startTime=datetime.datetime(2022, 8, 1, 12, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=24.1, temperatureApparent=24.1, weatherCode=1102, weatherCodeFullDay=None, windSpeed=0.33), ForecastInterval(startTime=datetime.datetime(2022, 8, 1, 13, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=25, temperatureApparent=25, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.71), ForecastInterval(startTime=datetime.datetime(2022, 8, 1, 14, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=25.7, temperatureApparent=25.7, weatherCode=1001, weatherCodeFullDay=None, windSpeed=2.15), ForecastInterval(startTime=datetime.datetime(2022, 8, 1, 15, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=26.1, temperatureApparent=26.1, weatherCode=1001, weatherCodeFullDay=None, windSpeed=2.32)])

# clear_day
# clear_night
# cloudy
# drizzle
# flurries
# fog_light
# fog
# freezing_drizzle
# freezing_rain_heavy
# freezing_rain_light
# freezing_rain
# ice_pellets_heavy
# ice_pellets_light
# ice_pellets
# mostly_clear_day
# mostly_clear_night
# mostly_cloudy
# partly_cloudy_day
# partly_cloudy_night
# rain_heavy
# rain_light
# rain
# snow_heavy
# snow_light
# snow
# tstorm

def image_for_weather_code(code: int, resolution: int = 1, night=False) -> Image.Image | None:
    image_name = weatherCodeImageMap.get(code)
    if not image_name: 
        return None

    path = f'icons/{image_name}{"@2x" if resolution == 2 else ""}.png'

    if night:
        night_path = path.replace('day', 'night')
        if os.path.exists(night_path):
            path = night_path

    return Image.open(path)


def image_for_weather_code_full_day(code: int, resolution: int = 1) -> Image.Image | None:
    image_name = weatherCodeFullDayImageMap.get(code)
    if not image_name: 
        return None

    return Image.open(f'icons/{image_name}{"@2x" if resolution == 2 else ""}.png')


weatherCodeImageMap = {
  0: "",  # "Unknown",
  1000: "clear_day",  # "Clear, Sunny",
  1100: "mostly_clear_day",  # "Mostly Clear",
  1101: "partly_cloudy_day",  # "Partly Cloudy",
  1102: "mostly_cloudy",  # "Mostly Cloudy",
  1001: "cloudy",  # "Cloudy",
  2000: "fog",  # "Fog",
  2100: "fog_light",  # "Light Fog",
  4000: "drizzle",  # "Drizzle",
  4001: "rain",  # "Rain",
  4200: "rain_light",  # "Light Rain",
  4201: "rain_heavy",  # "Heavy Rain",
  5000: "snow",  # "Snow",
  5001: "flurries",  # "Flurries",
  5100: "snow_light",  # "Light Snow",
  5101: "snow_heavy",  # "Heavy Snow",
  6000: "freezing_drizzle",  # "Freezing Drizzle",
  6001: "freezing_rain",  # "Freezing Rain",
  6200: "freezing_rain_light",  # "Light Freezing Rain",
  6201: "freezing_rain_heavy",  # "Heavy Freezing Rain",
  7000: "ice_pellets",  # "Ice Pellets",
  7101: "ice_pellets_heavy",  # "Heavy Ice Pellets",
  7102: "ice_pellets_light",  # "Light Ice Pellets",
  8000: "tstorm",  # "Thunderstorm"
}

weatherCodeFullDayImageMap = {
  0: "",  # "Unknown",
  1000: "clear_day",  # "Clear, Sunny",
  1100: "mostly_clear_day",  # "Mostly Clear",
  1101: "partly_cloudy_day",  # "Partly Cloudy",
  1102: "mostly_cloudy",  # "Mostly Cloudy",
  1001: "cloudy",  # "Cloudy",
  1103: "partly_cloudy_day",  # "Partly Cloudy and Mostly Clear",
  2100: "fog_light",  # "Light Fog",
  2101: "fog_light",  # "Mostly Clear and Light Fog",
  2102: "fog_light",  # "Partly Cloudy and Light Fog",
  2103: "fog_light",  # "Mostly Cloudy and Light Fog",
  2106: "fog",  # "Mostly Clear and Fog",
  2107: "fog",  # "Partly Cloudy and Fog",
  2108: "fog",  # "Mostly Cloudy and Fog",
  2000: "fog",  # "Fog",
  4204: "drizzle",  # "Partly Cloudy and Drizzle",
  4203: "drizzle",  # "Mostly Clear and Drizzle",
  4205: "drizzle",  # "Mostly Cloudy and Drizzle",
  4000: "drizzle",  # "Drizzle",
  4200: "rain_light",  # "Light Rain",
  4213: "rain_light",  # "Mostly Clear and Light Rain",
  4214: "rain_light",  # "Partly Cloudy and Light Rain",
  4215: "rain_light",  # "Mostly Cloudy and Light Rain",
  4209: "rain",  # "Mostly Clear and Rain",
  4208: "rain",  # "Partly Cloudy and Rain",
  4210: "rain",  # "Mostly Cloudy and Rain",
  4001: "rain",  # "Rain",
  4211: "heavy_rain",  # "Mostly Clear and Heavy Rain",
  4202: "heavy_rain",  # "Partly Cloudy and Heavy Rain",
  4212: "heavy_rain",  # "Mostly Cloudy and Heavy Rain",
  4201: "heavy_rain",  # "Heavy Rain",
  5115: "flurries",  # "Mostly Clear and Flurries",
  5116: "flurries",  # "Partly Cloudy and Flurries",
  5117: "flurries",  # "Mostly Cloudy and Flurries",
  5001: "flurries",  # "Flurries",
  5100: "snow_light",  # "Light Snow",
  5102: "snow_light",  # "Mostly Clear and Light Snow",
  5103: "snow_light",  # "Partly Cloudy and Light Snow",
  5104: "snow_light",  # "Mostly Cloudy and Light Snow",
  5122: "snow_light",  # "Drizzle and Light Snow",
  5105: "snow",  # "Mostly Clear and Snow",
  5106: "snow",  # "Partly Cloudy and Snow",
  5107: "snow",  # "Mostly Cloudy and Snow",
  5000: "snow",  # "Snow",
  5101: "snow_heavy",  # "Heavy Snow",
  5119: "snow_heavy",  # "Mostly Clear and Heavy Snow",
  5120: "snow_heavy",  # "Partly Cloudy and Heavy Snow",
  5121: "snow_heavy",  # "Mostly Cloudy and Heavy Snow",
  5110: "freezing_drizzle",  # "Drizzle and Snow",
  5108: "snow",  # "Rain and Snow",
  5114: "freezing_rain",  # "Snow and Freezing Rain",
  5112: "snow",  # "Snow and Ice Pellets",
  6000: "freezing_drizzle",  # "Freezing Drizzle",
  6003: "freezing_drizzle",  # "Mostly Clear and Freezing drizzle",
  6002: "freezing_drizzle",  # "Partly Cloudy and Freezing drizzle",
  6004: "freezing_drizzle",  # "Mostly Cloudy and Freezing drizzle",
  6204: "freezing_drizzle",  # "Drizzle and Freezing Drizzle",
  6206: "freezing_drizzle",  # "Light Rain and Freezing Drizzle",
  6205: "freezing_rain_light",  # "Mostly Clear and Light Freezing Rain",
  6203: "freezing_rain_light",  # "Partly Cloudy and Light Freezing Rain",
  6209: "freezing_rain_light",  # "Mostly Cloudy and Light Freezing Rain",
  6200: "freezing_rain_light",  # "Light Freezing Rain",
  6213: "freezing_rain",  # "Mostly Clear and Freezing Rain",
  6214: "freezing_rain",  # "Partly Cloudy and Freezing Rain",
  6215: "freezing_rain",  # "Mostly Cloudy and Freezing Rain",
  6001: "freezing_rain",  # "Freezing Rain",
  6212: "freezing_rain",  # "Drizzle and Freezing Rain",
  6220: "freezing_rain",  # "Light Rain and Freezing Rain",
  6222: "freezing_rain",  # "Rain and Freezing Rain",
  6207: "freezing_rain_heavy",  # "Mostly Clear and Heavy Freezing Rain",
  6202: "freezing_rain_heavy",  # "Partly Cloudy and Heavy Freezing Rain",
  6208: "freezing_rain_heavy",  # "Mostly Cloudy and Heavy Freezing Rain",
  6201: "freezing_rain_heavy",  # "Heavy Freezing Rain",
  7110: "ice_pellets_light",  # "Mostly Clear and Light Ice Pellets",
  7111: "ice_pellets_light",  # "Partly Cloudy and Light Ice Pellets",
  7112: "ice_pellets_light",  # "Mostly Cloudy and Light Ice Pellets",
  7102: "ice_pellets_light",  # "Light Ice Pellets",
  7108: "ice_pellets",  # "Mostly Clear and Ice Pellets",
  7107: "ice_pellets",  # "Partly Cloudy and Ice Pellets",
  7109: "ice_pellets",  # "Mostly Cloudy and Ice Pellets",
  7000: "ice_pellets",  # "Ice Pellets",
  7105: "ice_pellets",  # "Drizzle and Ice Pellets",
  7106: "ice_pellets",  # "Freezing Rain and Ice Pellets",
  7115: "ice_pellets",  # "Light Rain and Ice Pellets",
  7117: "ice_pellets",  # "Rain and Ice Pellets",
  7103: "ice_pellets_heavy",  # "Freezing Rain and Heavy Ice Pellets",
  7113: "ice_pellets_heavy",  # "Mostly Clear and Heavy Ice Pellets",
  7114: "ice_pellets_heavy",  # "Partly Cloudy and Heavy Ice Pellets",
  7116: "ice_pellets_heavy",  # "Mostly Cloudy and Heavy Ice Pellets",
  7101: "ice_pellets_heavy",  # "Heavy Ice Pellets",
  8001: "tstorm",  # "Mostly Clear and Thunderstorm",
  8003: "tstorm",  # "Partly Cloudy and Thunderstorm",
  8002: "tstorm",  # "Mostly Cloudy and Thunderstorm",
  8000: "tstorm",  # "Thunderstorm"
}
