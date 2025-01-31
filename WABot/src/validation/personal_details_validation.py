import re
from datetime import datetime

def validate_full_name(user_input):
    """
    Validates the full name format (First Name, Middle Name, Last Name).

    Parameters:
        user_input (str): The user-provided full name.

    Returns:
        dict: Contains 'is_valid' (bool) and 'message' (str).
    """
    if re.match(r"^[A-Z][a-z]+(\s[A-Z][a-z]+)+$", user_input):
        return {"is_valid": True, "message": "Full Name is valid."}
    return {"is_valid": False, "message": "Invalid Full Name. Please enter in the format: First Name Middle Name Last Name."}

def validate_date_of_birth(user_input):
    """
    Validates the date of birth format (DD/MM/YYYY) and logical validity.

    Parameters:
        user_input (str): The user-provided date of birth.

    Returns:
        dict: Contains 'is_valid' (bool) and 'message' (str).
    """
    try:
        dob = datetime.strptime(user_input, "%d/%m/%Y")
        if dob >= datetime.now():
            return {"is_valid": False, "message": "Date of Birth cannot be in the future."}
        return {"is_valid": True, "message": "Date of Birth is valid."}
    except ValueError:
        return {"is_valid": False, "message": "Invalid Date of Birth format. Please use DD/MM/YYYY."}

def validate_gender(user_input):
    """
    Validates the gender input (Male, Female, Other).

    Parameters:
        user_input (str): The user-provided gender.

    Returns:
        dict: Contains 'is_valid' (bool) and 'message' (str).
    """
    if user_input.lower() in ["male", "female"]:
        return {"is_valid": True, "message": "Gender is valid."}
    return {"is_valid": False, "message": "Invalid Gender. Please select Male, Female, or Other."}

def validate_contact_number(user_input):
    """
    Validates the contact number format (+263 7xx xxx xxx).

    Parameters:
        user_input (str): The user-provided contact number.

    Returns:
        dict: Contains 'is_valid' (bool) and 'message' (str).
    """
    if re.match(r"^\+263\s7\d{2}\s\d{3}\s\d{3}$", user_input):
        return {"is_valid": True, "message": "Contact Number is valid."}
    return {"is_valid": False, "message": "Invalid Contact Number. Please use the format: +263 7xx xxx xxx."}

def validate_address(user_input):
    """
    Validates the address format (non-empty and sufficiently descriptive).

    Parameters:
        user_input (str): The user-provided address.

    Returns:
        dict: Contains 'is_valid' (bool) and 'message' (str).
    """
    if len(user_input.strip()) > 5:
        return {"is_valid": True, "message": "Address is valid."}
    return {"is_valid": False, "message": "Invalid Address. Please provide a detailed address (e.g., 123 Street, City, Country)."}

def convert_to_datetime(date_str):
    """
    Converts a date string in the format dd/mm/yyyy to a datetime.date object.

    Args:
        date_str (str): The date string in the format dd/mm/yyyy.

    Returns:
        datetime.date: The corresponding date object.
    """
    try:
        # Parse the date string into a datetime object
        date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
        return date_obj
    except ValueError:
        raise ValueError("Invalid date format. Please use 'dd/mm/yyyy'.")

