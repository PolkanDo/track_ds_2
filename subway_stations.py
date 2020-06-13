import csv
import json

from math import radians, cos, sin, asin, sqrt


def havering(lat1, lon1, lat2, lon2):
    """
    The function calculates the distance in kilometers between two points,
    taking into account the circumference of the Earth.
    https://en.wikipedia.org/wiki/Haversine_formula
    """

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, (lon1, lat1, lon2, lat2))

    # havering formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


def bus_stations_coordinates(file_name):
    """
    The function creates a list of Bus station coordinates from the specified file.
    """
    with open(file_name, 'r', encoding='cp1251') as f:
        reader = csv.DictReader(f, delimiter=';')
        b_st_coordinates = []
        for row in reader:
            b_st_coordinates.append([float(row['Longitude_WGS84']), float(row['Latitude_WGS84'])])
    return b_st_coordinates


def subway_stations_coordinates(file_name):
    """
     The function creates a dictionary of Subway station coordinates from the specified file.
     """
    with open(file_name) as f:
        sb_stations = json.load(f)
        sb_st_coordinates = {}
        for station in sb_stations:
            #print(station)
            if station['NameOfStation'] not in sb_st_coordinates:
                sb_st_coordinates[station['NameOfStation']] = \
                    [float(station['Longitude_WGS84']), float(station['Latitude_WGS84'])]
            else:
                pass
    return sb_st_coordinates


def main_function(bs_coords, subs_coords):
    """
    The function creates a dictionary of subway stations and number bus stations near it.
    """
    num_s_dictionary = {}
    for sub_station, coordinates in subs_coords.items():
        for i in bs_coords:
            if havering(i[0], i[1], coordinates[0], coordinates[1]) <= 0.5:
                if sub_station in num_s_dictionary:
                    num_s_dictionary[sub_station] += 1
                else:
                    num_s_dictionary[sub_station] = 1
    return sorted(num_s_dictionary.items(), key=lambda item: item[1], reverse=True)


bus_stations = bus_stations_coordinates('bus_stations.csv')
subway_stations = subway_stations_coordinates('subway_stations.json')
print(main_function(bus_stations, subway_stations))
