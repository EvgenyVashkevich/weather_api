from datetime import datetime


def kelvin2celsius(temperature: float) -> str:
    """ Convert `temperature` from Kelvin to Celsius """

    return f'{int(temperature - 273.15)} °C'


def kelvin2fahrenheit(temperature: float) -> str:
    """ Convert `temperature` from Kelvin to Fahrenheit """

    return f'{int((temperature - 273.15) * 9/5) + 32} °F'


def utc2time(utctime: int) -> str:
    """ Convert UTC timestamp to current time """

    return datetime.utcfromtimestamp(utctime).strftime('%H:%M')


def wind2beaufort(speed: float) -> str:
    """ Convert wind speed to Beaufort scale (see https://en.wikipedia.org/wiki/Beaufort_scale) """

    if speed <= 0.5:
        beaufort = 'Calm'
    elif speed <= 1.5:
        beaufort = 'Light air'
    elif speed <= 3.3:
        beaufort = 'Light breeze'
    elif speed <= 5.5:
        beaufort = 'Gentle breeze'
    elif speed <= 7.9:
        beaufort = 'Moderate breeze'
    elif speed <= 10.7:
        beaufort = 'Fresh breeze'
    elif speed <= 13.8:
        beaufort = 'Strong breeze'
    elif speed <= 17.1:
        beaufort = 'High wind'
    elif speed <= 20.7:
        beaufort = 'Gale'
    else:
        beaufort = 'Storm'
    return beaufort


def clouds2condition(clouds: int) -> str:
    """ Convert clouds percentage to condition """

    clouds /= 100
    if clouds <= 1 / 8:
        condition = 'Sunny'
    elif clouds <= 3 / 8:
        condition = 'Mostly Sunny'
    elif clouds <= 5 / 8:
        condition = 'Partly Sunny'
    elif clouds <= 7 / 8:
        condition = 'Mostly Cloudy'
    else:
        condition = 'Cloudy'
    return condition
