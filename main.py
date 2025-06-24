from tkinter import *
import tkintermapview

# Global selection indexes
selected_archive_index = None
selected_employee_index = None
selected_client_index = None

class Archive:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.coordinates = get_coordinates(location)
        self.marker = map_widget.set_marker(*self.coordinates, text=name)

class Employee:
    def __init__(self, name, location, archive):
        self.name = name
        self.location = location
        self.archive = archive
        self.coordinates = get_coordinates(location)
        self.marker = map_widget.set_marker(*self.coordinates, text=name)
class Client:
    def __init__(self, name, location, archive):
        self.name = name
        self.location = location
        self.archive = archive
        self.coordinates = get_coordinates(location)
        self.marker = map_widget.set_marker(*self.coordinates, text=name)
def get_coordinates(location):
    import requests
    from bs4 import BeautifulSoup
    import re

    def dms_to_dd(dms_str):
        parts = re.split('[°′″]', dms_str)
        degrees = float(parts[0])
        minutes = float(parts[1])
        seconds = float(parts[2])
        direction = dms_str[-1]
        dd = degrees + minutes / 60 + seconds / 3600
        if direction in ['S', 'W']:
            dd *= -1
        return dd

    url = f'https://pl.wikipedia.org/wiki/{location}'
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')
    lat_str = soup.select_one('.latitude').text
    lon_str = soup.select_one('.longitude').text
    return dms_to_dd(lat_str), dms_to_dd(lon_str)
archives = []
employees = []
clients = []
