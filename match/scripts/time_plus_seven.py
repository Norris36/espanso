# We are importing the necessary modules here. The datetime module helps us work with times and dates,
# and the os module lets us interact with the operating system, which we use to get the environment variables.
from datetime import datetime, timedelta
import os

def time_plus_seven(time_str):
    time_format = '%H%M'  # The format we are expecting the time to be in: 'HHMM'.
    time_obj = datetime.strptime(time_str, time_format)  # Convert the time string into a datetime object.
    time_minus_seven = (time_obj + timedelta(hours=7)).time()  # Subtract 7 hours from the original time.
    return time_obj.strftime('%H:%M'), time_minus_seven.strftime('%H:%M')  # Return the original and new times in 'HH:MM' format.

def time_minus_seven(time_str):
    time_format = '%H%M'  # The format we are expecting the time to be in: 'HHMM'.
    time_obj = datetime.strptime(time_str, time_format)  # Convert the time string into a datetime object.
    time_minus_seven = (time_obj - timedelta(hours=7)).time()  # Subtract 7 hours from the original time.
    return time_obj.strftime('%H:%M'), time_minus_seven.strftime('%H:%M')  # Return the original and new times in 'HH:MM' format.

def time_minus_two(time_str):
    time_format = '%H%M'  # The format we are expecting the time to be in: 'HHMM'.
    time_obj = datetime.strptime(time_str, time_format)  # Convert the time string into a datetime object.
    time_minus_seven = (time_obj - timedelta(hours=2)).time()  # Subtract 7 hours from the original time.
    return time_obj.strftime('%H:%M'), time_minus_seven.strftime('%H:%M')  # Return the original and new times in 'HH:MM' format.

if __name__ == "__main__":
    number = os.getenv('ESPANSO_NUMBER')  # Get the number variable from the environment variables.
    country_code = os.getenv('ESPANSO_COUNTRY')  # Get the country code variable from the environment variables.


    number = number.strip()  # Remove any whitespace from the number variable.

    if number == 'now':
        number = datetime.now().strftime('%H%M')
    else:
        number = number

    # If the country code is 'dk', we want to get the current time in Denmark and subtract 7 hours from it.
    if country_code == 'dk':
        dk_time = number  # The time is directly provided by the 'number' variable.
        chi_time, dk_minus_7 = time_minus_seven(dk_time)  # Subtract 7 hours from the Denmark time.

        # Print the times in the desired format.
        print(f"DK {chi_time} [Chi {dk_minus_7}]")
    elif country_code == 'pol':
        chi_time = number  # The time is directly provided by the 'number' variable.
        dk_time, chi_minus_7 = time_plus_seven(chi_time)  # Subtract 7 hours from the Chicago time.

        # Print the times in the desired format.
        print(f"US {dk_time} [POL {chi_minus_7}]")
    # If the country code is 'us', we want to get the current time in Chicago and subtract 7 hours from it.
    elif country_code == 'us':
        chi_time = number  # The time is directly provided by the 'number' variable.
        dk_time, chi_minus_7 = time_plus_seven(chi_time)  # Subtract 7 hours from the Chicago time.

        # Print the times in the desired format.
        print(f"US {dk_time} [DK {chi_minus_7}]")
    elif country_code == 'ca':
        chi_time = number  # The time is directly provided by the 'number' variable.
        dk_time, chi_minus_7 = time_minus_two(chi_time)  # Subtract 2 hours from the Chicago time.

        # Print the times in the desired format.
        print(f"CHI {dk_time} [CALI {chi_minus_7}]")