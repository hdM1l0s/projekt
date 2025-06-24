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
