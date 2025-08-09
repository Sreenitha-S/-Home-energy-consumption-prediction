# energy_processor.py

import requests
import json


def calculate_energy_consumption_kwh(wattage, hours_of_use, quantity=1):
    """
    Calculates energy consumption in kilowatt-hours (kWh).
    Formula: Energy (kWh) = (Appliance Wattage × Hours of Use × Quantity) / 1000
    """
    # Validation for non-negative values is assumed to be handled by the input layer,
    # but a safeguard is here.
    if wattage < 0 or hours_of_use < 0 or quantity < 0:
        return 0.0
    return (wattage * hours_of_use * quantity) / 1000


def fetch_weather_data(city, api_key):
    """
    Fetches real-time weather data for a given city using the OpenWeatherMap API.
    Returns a dictionary with weather info or raises an exception on failure.
    """
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

    try:
        url = f"{BASE_URL}appid={api_key}&q={city}&units=metric"  # 'units=metric' for Celsius
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        weather_info = response.json()

        temperature = weather_info['main']['temp']
        humidity = weather_info['main']['humidity']
        description = weather_info['weather'][0]['description']

        return {
            'city': city,
            'temperature': temperature,
            'humidity': humidity,
            'description': description,
            'simulated': False
        }
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to retrieve weather data for {city}: {e}. Check city name, internet, or API key.")
    except KeyError as e:
        raise Exception(f"Error parsing weather data for {city}. Unexpected API response structure: {e}. "
                        "API key might be invalid/inactive or city not found.")


def predict_daily_total_energy(appliances_data, household_data, weather_data):
    """
    Calculates the total daily energy consumption for all provided appliances
    and formats the output including household and weather data.
    """
    total_kwh = 0.0
    results_output = []

    if not appliances_data:
        results_output.append("No appliances entered.")
    else:
        results_output.append("--- Daily Energy Breakdown ---")
        for appliance in appliances_data:
            name = appliance['name']
            wattage = appliance['wattage']
            hours = appliance['hours_of_use']
            quantity = appliance['quantity']

            kwh = calculate_energy_consumption_kwh(wattage, hours, quantity)
            results_output.append(f"{quantity}x {name}: {wattage}W/unit x {hours}h/unit = {kwh:.2f} kWh/day")
            total_kwh += kwh

    results_output.append("\n--- Additional Factors Considered ---")
    if household_data:
        results_output.append(f"Home Size: {household_data.get('home_size_sqft', 'N/A')} sqft")

    if weather_data:
        results_output.append(f"City: {weather_data.get('city', 'N/A')}")
        if not weather_data.get('simulated', True):
            results_output.append(f"Actual Outdoor Temperature: {weather_data.get('temperature', 'N/A')}°C")
            results_output.append(f"Humidity: {weather_data.get('humidity', 'N/A')}%")
            results_output.append(f"Conditions: {weather_data.get('description', 'N/A')}")
        else:
            results_output.append(f"Simulated Outdoor Temperature: {weather_data.get('temperature', 'N/A')}°C")
            if weather_data.get('error'):
                results_output.append(f"(Error during API call: {weather_data['error']})")

    results_output.append("\n------------------------------")
    if appliances_data:
        results_output.append(f"Predicted Total Daily Energy Consumption: {total_kwh:.2f} kWh")
        results_output.append(f"This is approximately {total_kwh * 30:.2f} kWh per month.")
    else:
        results_output.append("No appliance types were entered, so total energy consumption is 0 kWh.")
    results_output.append("------------------------------")
    results_output.append(
        "\nNote: This is a basic prediction based on appliance usage and collected data. For more accurate AI predictions, you'd integrate actual weather API calls and develop a predictive model that uses home size, weather, and historical data to learn patterns and forecast energy usage.")

    return "\n".join(results_output), total_kwh

