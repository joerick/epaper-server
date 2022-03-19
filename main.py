from datetime import timedelta
import io
import os
import time

from flask import Flask
from PIL import Image, ImageDraw, ImageFont, ImageOps
import weather
import pytz

app = Flask(__name__)

small_font = ImageFont.truetype("SourceSansPro-Regular.ttf", 14)
font = ImageFont.truetype("OpenSans-Regular.ttf", 14)
font_semibold = ImageFont.truetype("OpenSans-SemiBold.ttf", 14)
font_bold = ImageFont.truetype("OpenSans-Bold.ttf", 14)


def draw_image():
    forecast = weather.get_weather_test_data()
    # print(forecast)

    w = 400
    h = 300

    im = Image.new('1', (w, h), 255)

    draw = ImageDraw.Draw(im)

    ###############
    # DRAW HEADER #
    ###############

    draw.line((0, 0) + im.size, fill=128)
    draw.line((0, im.size[1], im.size[0], 0), fill=128)

    today_time = forecast.today.startTime.astimezone(pytz.timezone('Europe/London'))

    timestamp = today_time.strftime(
        '%A %d %B %Y'
    )

    draw.text((11, 21), timestamp, font=small_font.font_variant(size=14), fill=0, anchor='ls')
    draw.text((w-11, 21), time.strftime('Updated %H : %M'), font=small_font.font_variant(size=9), fill=0, anchor='rs')

    if forecast.today.weatherCodeFullDay:
        day_icon = weather.image_for_weather_code_full_day(forecast.today.weatherCodeFullDay, resolution=2)
        if day_icon:
            # draw.bitmap((10, 36), day_icon, fill=0)
            draw_with_threshold(draw, (10, 36), day_icon, threshold=127)

    temp_high = max(h.temperature for h in forecast.today_hours)
    temp_low = min(h.temperature for h in forecast.today_hours)

    draw.text((62, 75), f'{temp_high:.0f}°', font=font_semibold.font_variant(size=40), anchor='ls')
    draw.text((142, 75), f'{temp_low:.0f}°', font=font_bold.font_variant(size=18), anchor='ls')

    ##############
    # DRAW GRAPH #
    ##############

    high_y = 90
    high_temp = max(20, temp_high)
    axis_y = 190

    y_for_temp = lambda temp: (temp / high_temp) * (high_y - axis_y) + axis_y
    today_start = forecast.today.startTime.replace(hour=6, minute=0, second=0, microsecond=0)
    today_start_timestamp = today_start.timestamp()
    x_for_time = lambda time: (time.timestamp() - today_start_timestamp) / (24*60*60) * 360 + 20

    # draw lines
    polygon_points = [
        (x_for_time(hour.startTime), y_for_temp(hour.temperature)) for hour in forecast.today_hours
    ]
    draw.line(polygon_points, width=3, fill=0)

    im_fade = Image.new('L', (w, h))
    polygon_points = [
        (x_for_time(hour.startTime), y_for_temp(hour.temperatureApparent)) for hour in forecast.today_hours
    ]
    ImageDraw.Draw(im_fade).line(polygon_points, width=3, fill=127)
    draw.bitmap((0, 0), im_fade.convert('1'), fill=0)

    # label lines
    for hour in forecast.today_hours:
        if hour.temperature == temp_high:
            xy = (x_for_time(hour.startTime), y_for_temp(hour.temperature) - 4)
            draw.text(xy, f'{hour.temperature:.0f}°', font=font.font_variant(size=12), anchor='ms')
            break

    for hour in forecast.today_hours:
        if hour.temperature == temp_low:
            xy = (x_for_time(hour.startTime), y_for_temp(hour.temperature) - 4)
            draw.text(xy, f'{hour.temperature:.0f}°', font=font.font_variant(size=12), anchor='ms')
            break

    # rainfall
    high_rainfall = 10
    y_for_rainfall = lambda precipIntensity: (precipIntensity / high_rainfall) * (high_y - axis_y) + axis_y

    for hour in forecast.today_hours:
        x = x_for_time(hour.startTime)
        draw.rectangle(
            xy=(
                (x - 3, y_for_rainfall(hour.precipitationIntensity)),
                (x + 3, axis_y),
            ),
            fill=0,
            width=0,
        )

    # time labels
    for i in range(5):
        timestamp = today_start + timedelta(hours=i * 6)
        string = timestamp.strftime("%H:%M")
        if string == '06:00': 
            string = '6:00'
        x = x_for_time(timestamp)
        # if i == 0:
        #     x += 4
        # if i == 4:
        #     x -= 4
        draw.text(
            xy=(x, axis_y + 6), 
            text=string,
            font=font.font_variant(size=12), 
            anchor='mt'
        )

    ################
    # DRAW SYMBOLS #
    ################

    for index, hour in enumerate(forecast.today_hours):
        if index % 6 != 0:
            continue

        x = x_for_time(hour.startTime)
        image = weather.image_for_weather_code(hour.weatherCode, night=hour.startTime.hour < 6)
        print(image)

        if image:
            draw_with_threshold(draw, (x-12, 236), image, threshold=90)
            image.close()

    #############
    # DRAW WIND #
    #############

    for index, hour in enumerate(forecast.today_hours):
        if index % 6 != 0:
            continue
        speed_mph = 2.23694 * hour.windSpeed

        style = 'black' if speed_mph > 10 else 'white'

        x = x_for_time(hour.startTime)
        y = 280

        if style == 'white':
            draw.arc(((x-9, y-9), (x+8, y+8)), 0, 360, fill=0)
        else:
            draw.ellipse(((x-9, y-9), (x+8, y+8)), fill=0, outline=0)

        draw.text(
            (x,y), 
            text=f'{speed_mph:.0f}',
            fill=0 if style == 'white' else 1,
            font=font_bold.font_variant(size=12),
            anchor='mm'
        )

    return im

def draw_with_threshold(draw: ImageDraw.ImageDraw, xy: tuple[float, float], image: Image.Image, threshold: int):
    image = image.split()[-1]
    draw.bitmap(xy, image.point([0]*threshold + [255]*(256-threshold)), fill=0)


def draw_with_levels(draw: ImageDraw.ImageDraw, xy: tuple[float, float], image: Image.Image, black_point: int, white_point: int):
    alpha = image.split()[-1]
    temp_image = ImageOps.colorize(alpha, 'black', 'white', blackpoint=black_point, whitepoint=white_point)
    temp_image = temp_image.convert('L')
    draw.bitmap(xy, temp_image, fill=0)
    

@app.route("/")
def hello_world():
    im = draw_image()
    im = im.convert('1')

    im_byte_arr = io.BytesIO()
    im.save(im_byte_arr, format='BMP')
    return im_byte_arr.getvalue(), 200, {'content-type': 'image/bmp'}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
