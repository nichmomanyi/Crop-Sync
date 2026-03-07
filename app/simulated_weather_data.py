import requests
import pandas as pd
from datetime import datetime
import time
import calendar

# Your OpenWeatherMap API key
api_key = "9e49de9fd8dfac17c62a8685c0fe3470"

# List of places and their coordinates in specified countries
places_coordinates = {
    ("Ghana", "Tamale"): {"lat": 9.4072, "lon": -0.8406},
    ("Ghana", "Accra"): {"lat": 5.6037, "lon": -0.1870},
    ("Ghana", "Kumasi"): {"lat": 6.6953, "lon": -1.6113},
    ("Burkina Faso", "Ouagadougou"): {"lat": 12.3714, "lon": -1.5197},
    ("Burkina Faso", "Bobo-Dioulasso"): {"lat": 11.1785, "lon": -4.2975},
    ("Cameroon", "Yaoundé"): {"lat": 3.8667, "lon": 11.5167},
    ("Cameroon", "Douala"): {"lat": 4.0511, "lon": 9.7679},
    ("Chad", "N'Djamena"): {"lat": 12.1348, "lon": 15.0557},
    ("Kenya", "Nairobi"): {"lat": -1.2921, "lon": 36.8219},
    ("Kenya", "Mombasa"): {"lat": -4.0435, "lon": 39.6682},
    ("Mozambique", "Maputo"): {"lat": -25.9686, "lon": 32.5804},
    ("Mozambique", "Chimoio"): {"lat": -19.1167, "lon": 33.4667},
    ("Niger", "Niamey"): {"lat": 13.5150, "lon": 2.1175},
    ("South Sudan", "Juba"): {"lat": 4.8517, "lon": 31.5825},
    ("Tanzania", "Dar es Salaam"): {"lat": -6.8235, "lon": 39.2695},
    ("Tanzania", "Arusha"): {"lat": -3.3667, "lon": 36.6833},
    ("Togo", "Lomé"): {"lat": 6.1725, "lon": 1.2308},
    ("Uganda", "Kampala"): {"lat": 0.3476, "lon": 32.5825},
    ("Uganda", "Entebbe"): {"lat": 0.0612, "lon": 32.4699}
}

def fetch_current_weather_data(api_key, lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "country": data['sys']['country'],
            "town": data['name'],
            "lat": lat,
            "lon": lon,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"],
            "rainfall": data.get("rain", {}).get("1h", 0),
            "date": datetime.now().strftime("%Y-%m-%d")
        }
    else:
        print(f"Failed to fetch data for coordinates: Latitude {lat}, Longitude {lon}")
        return None

# Fetch current weather data for each place
weather_data = []
for (country, town), coords in places_coordinates.items():
    data = fetch_current_weather_data(api_key, coords["lat"], coords["lon"])
    if data:
        data["country"] = country
        data["town"] = town
        weather_data.append(data)
    time.sleep(1)  # Avoid hitting API rate limits

# Convert to DataFrame
weather_df = pd.DataFrame(weather_data)

# Simulate monthly averages for 2024 and 2025
def simulate_monthly_averages(df, years=[2024, 2025]):
    monthly_data = []
    for country in df['country'].unique():
        for town in df[df['country'] == country]['town'].unique():
            base_temp = df[(df['country'] == country) & (df['town'] == town)]['temperature'].mean()
            base_humidity = df[(df['country'] == country) & (df['town'] == town)]['humidity'].mean()
            base_rainfall = df[(df['country'] == country) & (df['town'] == town)]['rainfall'].mean()
            base_condition = df[(df['country'] == country) & (df['town'] == town)]['condition'].iloc[0]
            lat = df[(df['country'] == country) & (df['town'] == town)]['lat'].iloc[0]
            lon = df[(df['country'] == country) & (df['town'] == town)]['lon'].iloc[0]

            for year in years:
                for month in range(1, 13):
                    # Simulate slight variations for each month
                    temperature = round(base_temp + (month % 3 - 1), 2)
                    humidity = round(base_humidity + (month % 2 * 2 - 1), 2)
                    rainfall = round(base_rainfall + (month % 2 * 0.2 - 0.1), 2)

                    monthly_data.append({
                        "country": country,
                        "town": town,
                        "year": year,
                        "month": calendar.month_name[month],
                        "temperature": temperature,
                        "humidity": humidity,
                        "condition": base_condition,
                        "rainfall": rainfall,
                        "lat": lat,
                        "lon": lon
                    })
    return pd.DataFrame(monthly_data)

monthly_weather_df = simulate_monthly_averages(weather_df, years=[2024, 2025])

# Save to CSV
monthly_weather_df.to_csv('./data_processed/monthly_weather_2024_2025.csv', index=False)
print("Monthly weather data for 2024 and 2025 saved to monthly_weather_2024_2025.csv")
