import re
import typing
from dataclasses import field

from nptime import nptime
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
    end: str = field(repr=False)
    time: str = None

    def __post_init__(self):
        if not re.match('^((\\d\\d)|\\d):\\d\\d$', self.start):
            self.start = NO_DATA
        if not re.match('^((\\d\\d)|\\d):\\d\\d$', self.end):
            self.end = NO_DATA

        try:
            start_hour, start_minutes = self.start.split(':')
            end_hour, end_minutes = self.end.split(':')
            start = nptime(hour=int(start_hour), minute=int(start_minutes))
            end = nptime(hour=int(end_hour), minute=int(end_minutes))
            assert end > start
            peak_duration = end - start
            self.time = ':'.join(str(peak_duration).split(':')[:2])
        except (ValueError, TypeError, AssertionError):
            self.time = NO_DATA


@dataclass
class Traffic:
    city_name: str = field(repr=False)
    traffic_peak_time: typing.Any = field()
    average_speed: float = field(metadata={'units': 'km/h'})


@dataclass(order=True)
class City:
    city_name: str
    country: str
    voivodeship: str
    area: int = field(metadata={'units': 'km^2'})
    population: int
    population_density: int = field(metadata={'units': 'person/km^2'})
    recreations: typing.Any = field()
    traffic_details: typing.Any = field()
