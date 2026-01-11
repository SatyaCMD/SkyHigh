import random
import string
import json
from pathlib import Path
from flights.models import Airport

def generate_captcha():
    """Generates a random 6-character alphanumeric captcha string."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


BASE_DIR = Path(__file__).resolve().parent

def load_airports():
    """
    Loads airport data from flights/data/airports.json
    and returns a list of Airport dataclass objects
    """
    file_path = BASE_DIR / "data" / "airports.json"

    if not file_path.exists():
        return [] 

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [Airport(**item) for item in data]
