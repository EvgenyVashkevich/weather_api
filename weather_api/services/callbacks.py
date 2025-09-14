from weather_api.processors import configs
from weather_api.services import converters, scheme
from weather_api.services.network import Network


async def weather(city: str, requested_time: str) -> scheme.WeatherResponse:
    """Callback for `weather` endpoint"""

    async with Network() as network:
        result = await network.post(
            url=configs.weather.api_url_format.format(
                city=city, api_key=configs.weather.api_key.get_secret_value()
            )
        )
    return scheme.WeatherResponse(
        location_name=f"{city}",
        temperature_celsius=converters.kelvin2celsius(result["main"]["temp"]),
        temperature_fahrenheit=converters.kelvin2fahrenheit(result["main"]["temp"]),
        wind=f"{converters.wind2beaufort(result['wind']['speed'])}, "
        f"{result['wind']['speed']:.1f} m/s",
        cloudiness=converters.clouds2condition(result["clouds"]["all"]),
        pressure=f"{result['main']['pressure']} hpa",
        humidity=f"{result['main']['humidity']}%",
        sunrise=converters.utc2time(result["sys"]["sunrise"] + result["timezone"]),
        sunset=converters.utc2time(result["sys"]["sunset"] + result["timezone"]),
        geo_coordinates=f"[{result['coord']['lat']:.2f}, {result['coord']['lon']:.2f}]",
        requested_time=requested_time,
        forecast="",
    )
