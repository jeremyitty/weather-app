import requests
from datetime import datetime
from config import API_KEY, LOCATION

class WeatherApp:
    def __init__(self, api_key, location):
        self.api_key = api_key
        self.location = location
        self.base_url = "http://api.weatherapi.com/v1"
    
    def get_current_weather(self):
        """Fetch current weather data"""
        url = f"{self.base_url}/current.json"
        params = {
            "key": self.api_key,
            "q": self.location,
            "aqi": "yes"
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching current weather: {e}")
            return None
    
    def get_forecast(self, days=1):
        """Fetch weather forecast data"""
        url = f"{self.base_url}/forecast.json"
        params = {
            "key": self.api_key,
            "q": self.location,
            "days": days,
            "aqi": "yes",
            "alerts": "no"
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forecast: {e}")
            return None
    
    def display_current_weather(self):
        """Display current weather in a formatted way"""
        data = self.get_current_weather()
        if not data:
            print("Could not fetch current weather data.")
            return
        
        current = data['current']
        location = data['location']
        
        print("\n" + "="*60)
        print(f"📍 CURRENT WEATHER FOR {location['name']}, {location['country']}")
        print("="*60)
        print(f"Temperature: {current['temp_c']}°C / {current['temp_f']}°F")
        print(f"Feels Like: {current['feelslike_c']}°C / {current['feelslike_f']}°F")
        print(f"Condition: {current['condition']['text']}")
        print(f"Humidity: {current['humidity']}%")
        print(f"Wind Speed: {current['wind_kph']} km/h ({current['wind_mph']} mph)")
        print(f"Wind Direction: {current['wind_dir']}")
        print(f"UV Index: {current['uv']}")
        if 'air_quality' in current:
            print(f"Air Quality Index: {current['air_quality'].get('us-epa-index', 'N/A')}")
        print("="*60 + "\n")
    
    def display_hourly_forecast(self):
        """Display hourly forecast for the next 24 hours"""
        data = self.get_forecast(days=1)
        if not data:
            print("Could not fetch forecast data.")
            return
        
        forecast_day = data['forecast']['forecastday'][0]
        hours = forecast_day['hour']
        
        print("\n" + "="*60)
        print("⏰ 24-HOUR HOURLY FORECAST")
        print("="*60)
        print(f"{'Time':<12} {'Temp (°C)':<12} {'Condition':<20} {'Rain %':<10} {'Wind (kph)':<12}")
        print("-"*60)
        
        for hour in hours:
            time = datetime.fromisoformat(hour['time']).strftime("%H:%M")
            temp = hour['temp_c']
            condition = hour['condition']['text']
            rain_chance = hour['chance_of_rain']
            wind = hour['wind_kph']
            
            print(f"{time:<12} {temp:<12} {condition:<20} {rain_chance:<10} {wind:<12}")
        
        print("="*60 + "\n")

def main():
    if not API_KEY:
        print("❌ Error: API key not configured in config.py")
        print("Please get a free API key from https://www.weatherapi.com/")
        return
    
    app = WeatherApp(API_KEY, LOCATION)
    
    print("\n🌤️  Welcome to Weather App!")
    app.display_current_weather()
    app.display_hourly_forecast()

if __name__ == "__main__":
    main()
