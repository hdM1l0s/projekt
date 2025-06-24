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

def update_archive_option_menu():
    menu = archive_option_menu['menu']
    menu.delete(0, 'end')
    for i, a in enumerate(archives):
        menu.add_command(label=f"{a.name}", command=lambda value=i: archive_option_menu_var.set(str(value)))
    if archives:
        archive_option_menu_var.set("0")
    else:
        archive_option_menu_var.set("")

def fill_fields(listbox, data_list, entry_name, entry_location, obj_type):
    idx = listbox.curselection()
    if not idx: return
    index = idx[0]
    item = data_list[index]
    entry_name.delete(0, END)
    entry_name.insert(0, item.name)
    entry_location.delete(0, END)
    entry_location.insert(0, item.location)
    global selected_archive_index, selected_employee_index, selected_client_index
    if obj_type == "archive": selected_archive_index = index
    elif obj_type == "employee":
        selected_employee_index = index
        archive_option_menu_var.set(str(archives.index(item.archive)))
    elif obj_type == "client":
        selected_client_index = index
        archive_option_menu_var.set(str(archives.index(item.archive)))

def add_archive():
    name = entry_archive_name.get()
    location = entry_archive_location.get()
    a = Archive(name, location)
    archives.append(a)
    listbox_archives.insert(END, f"{name} - {location}")
    update_archive_option_menu()

def edit_archive():
    global selected_archive_index
    if selected_archive_index is None: return
    name = entry_archive_name.get()
    location = entry_archive_location.get()
    archive = archives[selected_archive_index]
    archive.name = name
    archive.location = location
    archive.coordinates = get_coordinates(location)
    archive.marker = map_widget.set_marker(*archive.coordinates, text=name)
    listbox_archives.delete(selected_archive_index)
    listbox_archives.insert(selected_archive_index, f"{name} - {location}")
    update_archive_option_menu()

def delete_archive():
    global selected_archive_index
    if selected_archive_index is None: return
    archive = archives.pop(selected_archive_index)
    archive.marker.delete()
    listbox_archives.delete(selected_archive_index)
    selected_archive_index = None
    update_archive_option_menu()

def add_employee():
    if not archives: return
    name = entry_employee_name.get()
    location = entry_employee_location.get()
    if archive_option_menu_var.get() == "": return
    archive = archives[int(archive_option_menu_var.get())]
    e = Employee(name, location, archive)
    employees.append(e)
    listbox_employees.insert(END, f"{name} - {location} ({archive.name})")

def edit_employee():
    global selected_employee_index
    if selected_employee_index is None: return
    name = entry_employee_name.get()
    location = entry_employee_location.get()
    archive_index = archive_option_menu_var.get()
    if archive_index == "" or not archive_index.isdigit(): return
    new_archive = archives[int(archive_index)]
    emp = employees[selected_employee_index]
    emp.name = name
    emp.location = location
    emp.archive = new_archive
    emp.coordinates = get_coordinates(location)
    emp.marker = map_widget.set_marker(*emp.coordinates, text=name)
    listbox_employees.delete(selected_employee_index)
    listbox_employees.insert(selected_employee_index, f"{name} - {location} ({new_archive.name})")

def delete_employee():
    global selected_employee_index
    if selected_employee_index is None: return
    emp = employees.pop(selected_employee_index)
    emp.marker.delete()
    listbox_employees.delete(selected_employee_index)
    selected_employee_index = None

def add_client():
    if not archives: return
    name = entry_client_name.get()
    location = entry_client_location.get()
    if archive_option_menu_var.get() == "": return
    archive = archives[int(archive_option_menu_var.get())]
    c = Client(name, location, archive)
    clients.append(c)
    listbox_clients.insert(END, f"{name} - {location} ({archive.name})")

def edit_client():
    global selected_client_index
    if selected_client_index is None: return
    name = entry_client_name.get()
    location = entry_client_location.get()
    archive_index = archive_option_menu_var.get()
    if archive_index == "" or not archive_index.isdigit(): return
    new_archive = archives[int(archive_index)]
    client = clients[selected_client_index]
    client.name = name
    client.location = location
    client.archive = new_archive
    client.coordinates = get_coordinates(location)
    client.marker = map_widget.set_marker(*client.coordinates, text=name)
    listbox_clients.delete(selected_client_index)
    listbox_clients.insert(selected_client_index, f"{name} - {location} ({new_archive.name})")

def delete_client():
    global selected_client_index
    if selected_client_index is None: return
    client = clients.pop(selected_client_index)
    client.marker.delete()
    listbox_clients.delete(selected_client_index)
    selected_client_index = None

def show_all_archives():
    map_widget.delete_all_marker()
    for a in archives:
        a.marker = map_widget.set_marker(*a.coordinates, text=a.name)

def show_all_employees():
    map_widget.delete_all_marker()
    for e in employees:
        e.marker = map_widget.set_marker(*e.coordinates, text=e.name)

def show_clients_for_selected_archive():
    if selected_archive_index is None: return
    map_widget.delete_all_marker()
    archive = archives[selected_archive_index]
    for c in clients:
        if c.archive == archive:
            c.marker = map_widget.set_marker(*c.coordinates, text=c.name)
def show_employees_for_selected_archive():
    if selected_archive_index is None: return
    map_widget.delete_all_marker()
    archive = archives[selected_archive_index]
    for e in employees:
        if e.archive == archive:
            e.marker = map_widget.set_marker(*e.coordinates, text=e.name)

root = Tk()
root.geometry("1200x800")
root.title("System zarzadzania archiwami")

