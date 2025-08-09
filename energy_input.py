# energy_input.py

def validate_and_get_appliance_data(name_str, wattage_str, hours_str, quantity_str):
    """
    Validates and converts appliance input strings to appropriate types.
    Returns a dictionary of appliance data or raises a ValueError on invalid input.
    """
    if not name_str or not wattage_str or not hours_str or not quantity_str:
        raise ValueError("All appliance fields must be filled.")

    try:
        wattage = float(wattage_str)
        hours = float(hours_str)
        quantity = int(quantity_str)
        if wattage <= 0 or hours < 0 or quantity <= 0:
            raise ValueError("Wattage and Quantity must be positive. Hours can be zero or positive.")
    except ValueError:
        raise ValueError("Wattage, Hours, and Quantity must be valid numbers.")

    return {
        'name': name_str.strip(),
        'wattage': wattage,
        'hours_of_use': hours,
        'quantity': quantity
    }


def validate_and_get_household_data(home_size_str):
    """
    Validates and converts household input strings.
    Returns a dictionary of household data or raises a ValueError on invalid input.
    """
    if not home_size_str:
        raise ValueError("Home Size field must be filled.")

    try:
        home_size_sqft = float(home_size_str)
        if home_size_sqft <= 0:
            raise ValueError("Home size must be a positive number.")
    except ValueError:
        raise ValueError("Home Size must be a valid number.")

    return {
        'home_size_sqft': home_size_sqft
    }


def validate_city_input(city_str):
    """
    Validates the city input string.
    Returns the stripped city string or raises a ValueError if empty.
    """
    if not city_str.strip():
        raise ValueError("City field must be filled.")
    return city_str.strip()


def validate_api_key(api_key_str):
    """
    Checks if the API key is provided and not the placeholder.
    Returns True if valid, False otherwise.
    """
    if not api_key_str or api_key_str == "replace with your api":
        return False
    return True

