from pydantic import BaseModel, Field


class WeatherResponse(BaseModel):
    location_name: str = Field(...)
    temperature_celsius: str = Field(...)
    temperature_fahrenheit: str = Field(...)
    wind: str = Field(...)
    cloudiness: str = Field(...)
    pressure: str = Field(...)
    humidity: str = Field(...)
    sunrise: str = Field(...)
    sunset: str = Field(...)
    geo_coordinates: str = Field(...)
    requested_time: str = Field(...)
    forecast: str = Field(...)

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "location_name": "Warsaw",
                "temperature_celsius": "17 °C",
                "temperature_fahrenheit": "71 °F",
                "wind": "Gentle breeze, 3.6 m/s, west-northwest",
                "cloudiness": "Scattered clouds",
                "pressure": "1027 hpa",
                "humidity": "63%",
                "sunrise": "06:07",
                "sunset": "18:00",
                "geo_coordinates": "[4.61, -74.08]",
                "requested_time": "2018-01-09 11:57:00",
                "forecast": "{}",
            }]
        }
    }
