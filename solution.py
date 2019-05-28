import datetime
import json
import re
from dataclasses import field

from pydantic import ValidationError
from pydantic.dataclasses import dataclass

NO_DATA = 'no valid data found'


@dataclass
class ParksAndRecreations:
    city_name: str = field(repr=False)
    parks: int = field(metadata={'units': '%'})
    woods: int = field(metadata={'units': '%'})


@dataclass
class TrafficPeakTime:
    city_name: str = field(repr=False)
    start: str
    end: str
    time: str = None

    def __post_init__(self):
        if re.match("^((\\d\\d)|\\d):\\d\\d$", self.start):
            try:
                hour, minutes = self.start.split(":")
                datetime.time(int(hour), int(minutes))
            except ValueError:
                self.start = NO_DATA
        else:
            self.start = NO_DATA
        if re.match("^((\\d\\d)|\\d):\\d\\d$", self.time):
            try:
                hour, minutes = self.time.split(":")
                datetime.time(int(hour), int(minutes))
            except ValueError:
                self.time = NO_DATA
        else:
            self.time = NO_DATA
        # tu obliczyć jakoś TIMEEEEE


@dataclass
class Traffic:
    city_name: str = field(repr=False)
    traffic_peak_time: TrafficPeakTime
    average_speed: float = field(metadata={'units': 'km/h'})


@dataclass(order=True, unsafe_hash=True)
class City:
    city_name: str
    country: str
    voivodeship: str
    area: int = field(metadata={'units': 'km^2'})
    population: int
    population_density: int = field(metadata={'units': 'person/km^2'})
    recreations: ParksAndRecreations
    traffic_details: Traffic


json_data_files = ('cities.json', 'parks_and_recreations_info.json', 'traffic_info.json')


def get_data_from_json(filepath):
    with open(f'{filepath}') as f:
        data = json.load(f).get('cities')
    return data


def get_cities(data):
    cities = []
    for city in data:
        try:
            cities.append(City(city_name=city.get('city', NO_DATA),
                               country=,
                               voivodeship=,
                               area=,
                               population=,
                               population_density=,
                               recreations= None, #tu jakiś łatwy dostęp, może recreations trzymać w słowniku a nie w liście i dostać się po kluczu,
                               traffic_details= None # komentarze jak wyżej))
        except ValidationError as e:
            print(f"Spotted data corrpution: {e}")
    return cities


def get_parks_and_recreations(data):
    parks_and_recreations = [] # może słownik? i sprawdzenie czy się nie dublują
    for city in data:
        try:
            parks_and_recreations.append(ParksAndRecreations(
                city_name=city.get('city', NO_DATA),
                parks=city.get('recreations', NO_DATA).get('parks', NO_DATA),
                woods=city.get('recreations', NO_DATA).get('parks', NO_DATA)))
        except ValidationError as e:
            print(f"Spotted data corrpution: {e}")
    return parks_and_recreations


def get_traffic_info(data):
    traffic_info = []
    for city in data:
        try:
            traffic_peak_time_data = city.get('traffic_details', NO_DATA).get("traffic_peak_time", NO_DATA)
            traffic_peak_start = traffic_peak_time_data.get("start", NO_DATA)
            traffic_peak_end = traffic_peak_time_data.get("end", NO_DATA)
            traffic_peak_time = TrafficPeakTime(city_name=city.get('city', NO_DATA),
                                                start=traffic_peak_start,
                                                end=traffic_peak_end)
            traffic_info.append(Traffic(
                city_name=city.get('city', NO_DATA),
                traffic_peak_time=traffic_peak_time,
                average_speed=city.get('traffic_details', NO_DATA).get("average_speed", NO_DATA)))
        except ValidationError as e:
            print(f"Spotted data corrpution: {e}")
    return traffic_info


