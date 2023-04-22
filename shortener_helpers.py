import re
import string
import random
import re

# Set the max URL length
INTERNET_MAX_PATH_LENGTH = 2048

# Set the length of the unique ID to use for shortened URLs
URI_LENGTH = 8

# Set the range of max_attempts to create a unique ID
MAX_ATTEMPTS = 100

def is_valid_url(url):

    """
    Validate the given URL using a regular expression and check for URL length and special characters.
    Args:
        url (str): The URL to validate.
    Returns:
        bool: True if the URL is valid, False otherwise.
    """

    # Check for URL length
    if len(url) > INTERNET_MAX_PATH_LENGTH:
        return False

    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:www\.)?'  # www.
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
        r'(?::\d+)?'  # optional port (number that follows the domain name or IP address and)
        r'(?:/?|[/?]\S+)$', re.IGNORECASE) # optional path after domain name

    # Check for special characters not allowed in URLs
    return False if re.search(r'[<>]', url) else bool(re.match(regex, url))

def generate_unique_id(url_data, max_attempts=MAX_ATTEMPTS):

    """
    Generate a unique identifier using a combination of ASCII letters and digits. 
    Raise an error if the max_attempts is reached.
    Args:
        length (int): The length of the unique identifier.
    Returns:
        str: A `length`-character unique identifier.
    """

    attempts = 0
    chars = string.ascii_letters + string.digits
    while attempts < max_attempts:
        unique_id = ''.join(random.choices(chars, k=URI_LENGTH))
        if unique_id not in url_data: # check for collision 
            return unique_id
        attempts += 1
    raise ValueError("Exceeded maximum number of attempts to generate a unique ID.")
