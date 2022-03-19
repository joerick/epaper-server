from __future__ import annotations
from dataclasses import dataclass
import datetime
import os
import requests
from dateutil.parser import isoparse
from PIL import Image
from dateutil.tz import tzutc

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
    url = "https://api.tomorrow.io/v4/timelines?location=51.50717853040887%2C-0.24805243109767183&fields=precipitationIntensity&fields=weatherCode&fields=windSpeed&fields=temperature&fields=temperatureApparent&fields=precipitationProbability&fields=weatherCodeFullDay&units=metric&timesteps=1h&timesteps=1d&apikey=UZE0E9hka7EhwtEG0Ze7yJo46orLHgLX"
    # url += '&startTime=2022-03-20T00:00:00Z'

    response = requests.request("GET", url, headers={"Accept": "application/json"})
    response.raise_for_status()

    json_data = response.json()
    json_hourly_values = json_data['data']['timelines'][0]['intervals']
    json_daily_values = json_data['data']['timelines'][1]['intervals']

    hourly = [ForecastInterval.from_json(v) for v in json_hourly_values]
    today = ForecastInterval.from_json(json_daily_values[1])

    return Forecast(today=today, hourly=hourly)

def get_weather_test_data():
    return Forecast(today=ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 6, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=10.76, temperatureApparent=10.76, weatherCode=1101, weatherCodeFullDay=1101, windSpeed=3.68), hourly=[ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 0, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=6.9, temperatureApparent=6.9, weatherCode=1000, weatherCodeFullDay=None, windSpeed=3.74), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 1, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=6.49, temperatureApparent=6.49, weatherCode=1000, weatherCodeFullDay=None, windSpeed=3.66), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 2, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=5.98, temperatureApparent=5.98, weatherCode=1000, weatherCodeFullDay=None, windSpeed=3.09), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 3, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=5.35, temperatureApparent=5.35, weatherCode=1000, weatherCodeFullDay=None, windSpeed=2.47), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 4, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=4.71, temperatureApparent=4.71, weatherCode=1000, weatherCodeFullDay=None, windSpeed=2), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 5, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=4.17, temperatureApparent=2.39, weatherCode=1000, weatherCodeFullDay=None, windSpeed=2), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 6, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=3.75, temperatureApparent=1.91, weatherCode=1000, weatherCodeFullDay=None, windSpeed=1.98), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 7, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=3.89, temperatureApparent=1.51, weatherCode=1101, weatherCodeFullDay=None, windSpeed=2.56), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 8, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=5.2, temperatureApparent=5.2, weatherCode=1100, weatherCodeFullDay=None, windSpeed=3.03), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 9, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=6.9, temperatureApparent=6.9, weatherCode=1101, weatherCodeFullDay=None, windSpeed=3.39), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 10, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=7.97, temperatureApparent=7.97, weatherCode=1101, weatherCodeFullDay=None, windSpeed=3.68), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 11, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=9.01, temperatureApparent=9.01, weatherCode=1101, weatherCodeFullDay=None, windSpeed=3.37), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 12, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=9.62, temperatureApparent=9.62, weatherCode=1102, weatherCodeFullDay=None, windSpeed=3.17), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 13, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=10.06, temperatureApparent=10.06, weatherCode=1102, weatherCodeFullDay=None, windSpeed=2.44), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 14, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=10.47, temperatureApparent=10.47, weatherCode=1100, weatherCodeFullDay=None, windSpeed=1.61), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 15, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=10.76, temperatureApparent=10.76, weatherCode=1101, weatherCodeFullDay=None, windSpeed=0.71), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 16, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=10.76, temperatureApparent=10.76, weatherCode=1101, weatherCodeFullDay=None, windSpeed=0.18), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 17, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=10.52, temperatureApparent=10.52, weatherCode=1101, weatherCodeFullDay=None, windSpeed=0.66), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 18, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=9.92, temperatureApparent=9.92, weatherCode=1100, weatherCodeFullDay=None, windSpeed=0.76), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 19, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=8.66, temperatureApparent=8.66, weatherCode=1100, weatherCodeFullDay=None, windSpeed=0.75), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 20, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=7.71, temperatureApparent=7.71, weatherCode=1101, weatherCodeFullDay=None, windSpeed=0.6), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 21, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=6.61, temperatureApparent=6.61, weatherCode=1101, weatherCodeFullDay=None, windSpeed=1.3), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 22, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=5.49, temperatureApparent=5.49, weatherCode=1100, weatherCodeFullDay=None, windSpeed=1.08), ForecastInterval(startTime=datetime.datetime(2022, 3, 20, 23, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=4.91, temperatureApparent=4.91, weatherCode=1000, weatherCodeFullDay=None, windSpeed=0.83), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 0, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=4.29, temperatureApparent=4.29, weatherCode=1000, weatherCodeFullDay=None, windSpeed=0.75), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 1, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=4.14, temperatureApparent=4.14, weatherCode=1000, weatherCodeFullDay=None, windSpeed=0.09), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 2, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=3.84, temperatureApparent=3.84, weatherCode=1000, weatherCodeFullDay=None, windSpeed=0.93), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 3, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=3.16, temperatureApparent=3.16, weatherCode=1000, weatherCodeFullDay=None, windSpeed=0.66), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 4, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=2.88, temperatureApparent=2.88, weatherCode=1000, weatherCodeFullDay=None, windSpeed=0.55), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 5, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=2.8, temperatureApparent=2.8, weatherCode=1000, weatherCodeFullDay=None, windSpeed=0.78), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 6, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=2.45, temperatureApparent=2.45, weatherCode=1000, weatherCodeFullDay=None, windSpeed=1.05), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 7, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=2.01, temperatureApparent=2.01, weatherCode=1000, weatherCodeFullDay=None, windSpeed=1.15), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 8, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=3.57, temperatureApparent=3.57, weatherCode=1101, weatherCodeFullDay=None, windSpeed=1.07), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 9, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=5.87, temperatureApparent=5.87, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.14), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 10, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=7.83, temperatureApparent=7.83, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.71), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 11, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=9.22, temperatureApparent=9.22, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.76), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 12, 0, tzinfo=tzutc()), precipitationIntensity=0.0156, precipitationProbability=5, temperature=10.67, temperatureApparent=10.67, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.83), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 13, 0, tzinfo=tzutc()), precipitationIntensity=0.0703, precipitationProbability=5, temperature=11.71, temperatureApparent=11.71, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.96), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 14, 0, tzinfo=tzutc()), precipitationIntensity=0.0527, precipitationProbability=5, temperature=12.63, temperatureApparent=12.63, weatherCode=1001, weatherCodeFullDay=None, windSpeed=2.26), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 15, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=13.91, temperatureApparent=13.91, weatherCode=1001, weatherCodeFullDay=None, windSpeed=2.45), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 16, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=14.43, temperatureApparent=14.43, weatherCode=1001, weatherCodeFullDay=None, windSpeed=2.47), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 17, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=14.26, temperatureApparent=14.26, weatherCode=1001, weatherCodeFullDay=None, windSpeed=2.44), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 18, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=13.2, temperatureApparent=13.2, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.79), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 19, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=11.76, temperatureApparent=11.76, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.32), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 20, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=10.83, temperatureApparent=10.83, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.36), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 21, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=10.23, temperatureApparent=10.23, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.33), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 22, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=9.86, temperatureApparent=9.86, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.34), ForecastInterval(startTime=datetime.datetime(2022, 3, 21, 23, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=9.53, temperatureApparent=9.53, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.25), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 0, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=9.09, temperatureApparent=9.09, weatherCode=1102, weatherCodeFullDay=None, windSpeed=1.21), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 1, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=8.85, temperatureApparent=8.85, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.23), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 2, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=8.6, temperatureApparent=8.6, weatherCode=1100, weatherCodeFullDay=None, windSpeed=1.24), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 3, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=8.43, temperatureApparent=8.43, weatherCode=1100, weatherCodeFullDay=None, windSpeed=1.17), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 4, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=8.05, temperatureApparent=8.05, weatherCode=1101, weatherCodeFullDay=None, windSpeed=1.18), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 5, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=7.55, temperatureApparent=7.55, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.22), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 6, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=7.15, temperatureApparent=7.15, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.17), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 7, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=7.12, temperatureApparent=7.12, weatherCode=1100, weatherCodeFullDay=None, windSpeed=1.08), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 8, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=8.55, temperatureApparent=8.55, weatherCode=1100, weatherCodeFullDay=None, windSpeed=1.15), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 9, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=10.99, temperatureApparent=10.99, weatherCode=1100, weatherCodeFullDay=None, windSpeed=1.2), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 10, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=13.2, temperatureApparent=13.2, weatherCode=1100, weatherCodeFullDay=None, windSpeed=1.67), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 11, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=15.12, temperatureApparent=15.12, weatherCode=1100, weatherCodeFullDay=None, windSpeed=1.88), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 12, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=16.63, temperatureApparent=16.63, weatherCode=1100, weatherCodeFullDay=None, windSpeed=2.22), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 13, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=17.29, temperatureApparent=17.29, weatherCode=1001, weatherCodeFullDay=None, windSpeed=3.42), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 14, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=17.51, temperatureApparent=17.51, weatherCode=1101, weatherCodeFullDay=None, windSpeed=3.44), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 15, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=17.53, temperatureApparent=17.53, weatherCode=1101, weatherCodeFullDay=None, windSpeed=3.33), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 16, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=17.1, temperatureApparent=17.1, weatherCode=1000, weatherCodeFullDay=None, windSpeed=3.21), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 17, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=16.21, temperatureApparent=16.21, weatherCode=1000, weatherCodeFullDay=None, windSpeed=2.92), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 18, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=14.75, temperatureApparent=14.75, weatherCode=1000, weatherCodeFullDay=None, windSpeed=2.28), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 19, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=13.4, temperatureApparent=13.4, weatherCode=1000, weatherCodeFullDay=None, windSpeed=2.04), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 20, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=12.05, temperatureApparent=12.05, weatherCode=1000, weatherCodeFullDay=None, windSpeed=1.8), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 21, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=10.7, temperatureApparent=10.7, weatherCode=1000, weatherCodeFullDay=None, windSpeed=1.56), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 22, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=9.97, temperatureApparent=9.97, weatherCode=1000, weatherCodeFullDay=None, windSpeed=1.55), ForecastInterval(startTime=datetime.datetime(2022, 3, 22, 23, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=9.24, temperatureApparent=9.24, weatherCode=1000, weatherCodeFullDay=None, windSpeed=1.54), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 0, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=8.51, temperatureApparent=8.51, weatherCode=1000, weatherCodeFullDay=None, windSpeed=1.53), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 1, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=8.11, temperatureApparent=8.11, weatherCode=1000, weatherCodeFullDay=None, windSpeed=1.46), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 2, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=7.72, temperatureApparent=7.72, weatherCode=1000, weatherCodeFullDay=None, windSpeed=1.39), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 3, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=7.33, temperatureApparent=7.33, weatherCode=1000, weatherCodeFullDay=None, windSpeed=1.31), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 4, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=7.08, temperatureApparent=7.08, weatherCode=1100, weatherCodeFullDay=None, windSpeed=1.34), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 5, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=6.82, temperatureApparent=6.82, weatherCode=1100, weatherCodeFullDay=None, windSpeed=1.36), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 6, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=6.57, temperatureApparent=6.57, weatherCode=1101, weatherCodeFullDay=None, windSpeed=1.38), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 7, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=8.01, temperatureApparent=8.01, weatherCode=1101, weatherCodeFullDay=None, windSpeed=1.34), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 8, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=9.46, temperatureApparent=9.46, weatherCode=1100, weatherCodeFullDay=None, windSpeed=1.31), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 9, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=10.9, temperatureApparent=10.9, weatherCode=1100, weatherCodeFullDay=None, windSpeed=1.27), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 10, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=12.8, temperatureApparent=12.8, weatherCode=1100, weatherCodeFullDay=None, windSpeed=1.68), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 11, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=14.69, temperatureApparent=14.69, weatherCode=1100, weatherCodeFullDay=None, windSpeed=2.09), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 12, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=16.58, temperatureApparent=16.58, weatherCode=1100, weatherCodeFullDay=None, windSpeed=2.51), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 13, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=16.69, temperatureApparent=16.69, weatherCode=1101, weatherCodeFullDay=None, windSpeed=2.13), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 14, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=16.8, temperatureApparent=16.8, weatherCode=1101, weatherCodeFullDay=None, windSpeed=1.75), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 15, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=16.91, temperatureApparent=16.91, weatherCode=1001, weatherCodeFullDay=None, windSpeed=1.37), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 16, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=16.24, temperatureApparent=16.24, weatherCode=1101, weatherCodeFullDay=None, windSpeed=1.75), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 17, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=15.56, temperatureApparent=15.56, weatherCode=1101, weatherCodeFullDay=None, windSpeed=2.13), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 18, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=14.89, temperatureApparent=14.89, weatherCode=1100, weatherCodeFullDay=None, windSpeed=2.51), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 19, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=11.33, temperatureApparent=11.33, weatherCode=1000, weatherCodeFullDay=None, windSpeed=2.85), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 20, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=10.54, temperatureApparent=10.54, weatherCode=1000, weatherCodeFullDay=None, windSpeed=2.63), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 21, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=9.81, temperatureApparent=9.81, weatherCode=1000, weatherCodeFullDay=None, windSpeed=2.55), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 22, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=9.2, temperatureApparent=9.2, weatherCode=1000, weatherCodeFullDay=None, windSpeed=2.38), ForecastInterval(startTime=datetime.datetime(2022, 3, 23, 23, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=8.54, temperatureApparent=8.54, weatherCode=1000, weatherCodeFullDay=None, windSpeed=2.25), ForecastInterval(startTime=datetime.datetime(2022, 3, 24, 0, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=8.03, temperatureApparent=8.03, weatherCode=1000, weatherCodeFullDay=None, windSpeed=2.14), ForecastInterval(startTime=datetime.datetime(2022, 3, 24, 1, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=7.53, temperatureApparent=7.53, weatherCode=1000, weatherCodeFullDay=None, windSpeed=2.12), ForecastInterval(startTime=datetime.datetime(2022, 3, 24, 2, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=7.12, temperatureApparent=7.12, weatherCode=1000, weatherCodeFullDay=None, windSpeed=1.96), ForecastInterval(startTime=datetime.datetime(2022, 3, 24, 3, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=6.66, temperatureApparent=6.66, weatherCode=1000, weatherCodeFullDay=None, windSpeed=1.98), ForecastInterval(startTime=datetime.datetime(2022, 3, 24, 4, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=6.32, temperatureApparent=6.32, weatherCode=1000, weatherCodeFullDay=None, windSpeed=2.06), ForecastInterval(startTime=datetime.datetime(2022, 3, 24, 5, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=5.96, temperatureApparent=5.96, weatherCode=1000, weatherCodeFullDay=None, windSpeed=1.98), ForecastInterval(startTime=datetime.datetime(2022, 3, 24, 6, 0, tzinfo=tzutc()), precipitationIntensity=0, precipitationProbability=0, temperature=5.66, temperatureApparent=5.66, weatherCode=1000, weatherCodeFullDay=None, windSpeed=1.99)])

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
