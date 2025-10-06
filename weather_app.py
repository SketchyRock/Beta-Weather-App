import requests
from sys import exit

api_key = "76b436ddf0dd462d879145954250110" #api key for the weather website
home_screen = """ 
        .--.    
     .-(    ).  
    ( ___.__)__) 
     '  '  '  '

+------------------------+
|      WEATHER APP       |
+------------------------+
| 1) Current Forecast    |
| 2) 14-Day Forecast     |
| 3) Exit                |
+------------------------+
"""


#gives the forecast for specified amount of days including today for a city
def forecast(api_key: str, city: str, days: str):

    day_data = data_request_forecast(api_key, city, str(int(days) + 1))

    print(f"Fetching forecast for {city}...\n")
    print("Loading...\n")

    print(f"=== 14 DAY FORECAST for '{city}' ===")
    for forecast_day in day_data['forecast']['forecastday']:
        daily = forecast_day['day']
        print(f"Date: {forecast_day['date']}")
        print(f"Max Temp: {daily['maxtemp_c']}°C")
        print(f"Min Temp: {daily['mintemp_c']}°C")
        print(f"Condition: {daily['condition']['text']}")
        print(f"Chance of rain: {daily.get('daily_chance_of_rain', 'N/A')}%\n")

    input("(Press ENTER to Return)")
            

#current forecast for the day in a city
def current_forecast(city):
    data = data_request(api_key, "current", city)
    condition_text = data["current"]["condition"]["text"]
    temperature_f = data["current"]["temp_f"]
    uv_index = data["current"]["uv"]
    wind_speed = data["current"]["wind_mph"]
    precipitation_in = data["current"]["precip_in"]
    is_day = data["current"]["is_day"]

    print(f"=== Weather for '{city}' ===")
    print(f"  Condition: {condition_text}")
    print(f"  Temperature: {str(temperature_f)}°F")
    print(f"  UV: {str(uv_index)}")
    print(f"  Wind Speed: {str(wind_speed)} mph")
    print(f"  Precipitation: {str(precipitation_in)} in")

    if is_day == 1:
        day_or_night = "DAY"
    else:
        day_or_night = "NIGHT"
    print(f"  Hour: {day_or_night}")

    input("(Press ENTER to Return)")


#general request sent and dict recieved for a specific city
def data_request(api_key: str, request_type: str, city: str) -> dict:
    url = f"http://api.weatherapi.com/v1/{request_type}.json?key={api_key}&q={city}"
    response = requests.get(url)
    return response.json()


#special request fo forecast because it has an extra request parameter
def data_request_forecast(api_key: str, city: str, day: str) -> dict:
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days={day}"
    response = requests.get(url)
    return response.json()


# asks user for input until its one of the options
def main_menu_handling() -> str:
    while True:
        user_input = input("SEARCH: ").strip().lower()
        if user_input in ("current forecast", "14 day forecast","exit", "1", "2", "3"):
            return user_input
        else:
            print("Error: Invalid Input")


#main loop that returns to the homescreen after desired action is complete
def main():
    while True:
        print(home_screen)
        user_input = main_menu_handling()

        match(user_input):
            case "current forecast" | "1":
                city = input("Enter City Name: ")
                print()
                current_forecast(city)

            case "14 day forecast" | "2":
                city = input("Enter City Name: ")
                days = input("Enter Forecast for __ Days: ")
                print()
                forecast(city, days)

            case "exit" | "3":
                exit("Bye Bye!")
            
            case _:
                print("ERROR: main() case_")


if __name__ == "__main__":
    main()
