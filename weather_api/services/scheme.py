from pydantic import BaseModel, Field


class WeatherResponse(BaseModel):
    location_name: str = Field(..., example='Bogota, CO')
    temperature_celsius: str = Field(..., example='17 °C')
    temperature_fahrenheit: str = Field(..., example='71 °F')
    wind: str = Field(..., example='Gentle breeze, 3.6 m/s, west-northwest')
    cloudiness: str = Field(..., example='Scattered clouds')
    pressure: str = Field(..., example='1027 hpa')
    humidity: str = Field(..., example='63%')
    sunrise: str = Field(..., example='06:07')
    sunset: str = Field(..., example='18:00')
    geo_coordinates: str = Field(..., example='[4.61, -74.08]')
    requested_time: str = Field(..., example='2018-01-09 11:57:00')
    forecast: str = Field(..., example='{}')
