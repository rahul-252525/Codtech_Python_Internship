import matplotlib.pyplot as plt # Visualization ke liye
import requests # API requests ke liye
import json # JSON data handle karne ke liye

# Tumhari OpenWeatherMap API Key
# Apni asli key yahan paste karna
API_KEY = "9fb0e84cd1ff5ae375f6594dc840dc58"

# City jiska weather chahiye
CITY = "Mumbai" # Example ke liye Mumbai

# OpenWeatherMap API ka URL
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

# Pura URL banana
complete_url = f"{BASE_URL}appid={API_KEY}&q={CITY}&units=metric"

print(f"Fetching weather for: {CITY}")

# API request bhejna
response = requests.get(complete_url)

# Response ko JSON format mein parse karna
data = response.json()

# Check karna ki request successful thi ya nahi
if data["cod"] != "404":
    # Main weather data extract karna
    main_data = data["main"]
    weather_desc = data["weather"][0]["description"]

    # Temperatures
    current_temp = main_data["temp"]
    feels_like_temp = main_data["feels_like"]
    min_temp = main_data["temp_min"]
    max_temp = main_data["temp_max"]

    # Humidity
    humidity = main_data["humidity"]

    # Wind speed
    wind_speed = data["wind"]["speed"]

    # Print karna fetched data
    print(f"Weather in {CITY}: {weather_desc.capitalize()}")
    print(f"Current Temperature: {current_temp}°C")
    print(f"Feels Like: {feels_like_temp}°C")
    print(f"Min Temp: {min_temp}°C, Max Temp: {max_temp}°C")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")

else:
    print(f"City not found for: {CITY}. Please check the city name.")
    

# ... (Existing code from Step 6 remains above this) ...

# Agar data successfully mila hai, toh visualization banayenge
if data["cod"] != "404":
    # Data points for visualization
    labels = ['Current', 'Min', 'Max', 'Feels Like']
    temperatures = [current_temp, min_temp, max_temp, feels_like_temp]
    
    # Bar Chart banana
    plt.figure(figsize=(8, 6)) # Chart size set karna
    plt.bar(labels, temperatures, color=['skyblue', 'lightcoral', 'lightgreen', 'orange'])
    
    plt.ylabel('Temperature (°C)')
    plt.title(f'Temperature Overview in {CITY}')
    plt.grid(axis='y', linestyle='--', alpha=0.7) # Grid lines add karna
    
    # Values ko bars ke upar display karna
    for i, temp in enumerate(temperatures):
        plt.text(i, temp + 0.5, f'{temp}°C', ha='center', va='bottom')

    plt.tight_layout() # Layout adjust karna
    plt.show() # Chart display karna

    # Optional: Humidity aur Wind Speed ke liye ek aur plot
    # Ye simple hai, agar tum chaho to add kar sakte ho
    # plt.figure(figsize=(6, 4))
    # categories = ['Humidity', 'Wind Speed']
    # values = [humidity, wind_speed]
    # plt.bar(categories, values, color=['lightsteelblue', 'mediumaquamarine'])
    # plt.title(f'Other Metrics for {CITY}')
    # plt.show()

else:
    print(f"No visualization generated as city data was not found.")