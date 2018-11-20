
import random

def geocode(address: str):
    """Returns a random geocoordinate"""
    longitude = random.uniform(-180.0000, 180.0000)
    latitude = random.uniform(-90.0000, 90.0000)
    return (longitude, latitude)
