import json
from collections import defaultdict

from beautifultable import BeautifulTable
from pydantic import ValidationError

from models import NO_DATA, City, ParksAndRecreations, Traffic, \
    TrafficPeakTime


def get_cities(data, traffic_objects, parks_and_recreations_objects):
    cities = []
    for city in data:
        city_name = city.get('city', NO_DATA).capitalize()

        try:
            cities.append(City(
                city_name=city_name,
                country=city.get('country', NO_DATA),
                voivodeship=city.get('voivodeship', NO_DATA),
                area=city.get('area', NO_DATA),
                population=city.get('population', NO_DATA),
                population_density=city.get('population_density', NO_DATA),
                recreations=parks_and_recreations_objects.get(city_name, NO_DATA),
                traffic_details=traffic_objects.get(city_name, NO_DATA)))
        except ValidationError as e:
            print(f"[{city_name}] Spotted data corrpution: {e}")

    return cities


def get_parks_and_recreations(data):
    parks_and_recreations = defaultdict(ParksAndRecreations)
    for city in data:
        city_name = city.get('city', NO_DATA).capitalize()

        try:
            parks_and_recreations[city_name] = ParksAndRecreations(
                city_name=city_name,
                parks=city.get('recreations', NO_DATA).get('parks', NO_DATA),
                woods=city.get('recreations', NO_DATA).get('woods', NO_DATA))
        except ValidationError as e:
            print(f"[{city_name}]Spotted data corrpution: {e}")

    return parks_and_recreations


def get_traffic(data):
    traffic_info = defaultdict(Traffic)
    for city in data:
        city_name = city.get('city', NO_DATA).capitalize()

        try:
            traffic_peak_time_data = city.get('traffic_details', NO_DATA).get(
                'traffic_peak_time', NO_DATA)
            traffic_peak_start = traffic_peak_time_data.get('start', NO_DATA)
            traffic_peak_end = traffic_peak_time_data.get('end', NO_DATA)
            traffic_peak_time = TrafficPeakTime(city_name=city_name,
                                                start=traffic_peak_start,
                                                end=traffic_peak_end)
            traffic_info[city_name] = Traffic(
                city_name=city_name,
                traffic_peak_time=traffic_peak_time,
                average_speed=city.get('traffic_details', NO_DATA).get(
                    'average_speed', NO_DATA))
        except ValidationError as e:
            print(f"[{city_name}]Spotted data corrpution: {e}")

    return traffic_info


def get_data_from_json(filepath):
    with open(f'{filepath}') as f:
        data = json.load(f).get('cities')
    return data


def show_data(data):
    table = BeautifulTable(max_width=200)
    table.column_headers = [name for name in City.__annotations__]

    for city in data:
        row = [city.city_name, city.country, city.voivodeship, city.area,
               city.population, city.population_density, city.recreations,
               city.traffic_details]
        table.append_row(row)

    table.set_style(BeautifulTable.STYLE_BOX_ROUNDED)
    print(table)


def main():
    json_data_files = ('cities.json',
                       'parks_and_recreations_info.json',
                       'traffic_info.json')

    json_data = defaultdict(dict)

    for filepath in json_data_files:
        filename, _ = filepath.split('.')
        json_data[filename] = get_data_from_json(filepath)

    traffic_objects = get_traffic(data=json_data['traffic_info'])
    parks_and_recreations_objects = get_parks_and_recreations(
        data=json_data['parks_and_recreations_info'])
    cities_objects = get_cities(
        data=json_data['cities'],
        traffic_objects=traffic_objects,
        parks_and_recreations_objects=parks_and_recreations_objects)

    show_data(cities_objects)


if __name__ == '__main__':
    main()
