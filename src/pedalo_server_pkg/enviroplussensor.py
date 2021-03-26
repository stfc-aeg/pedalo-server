"""enviroplussensor sensor class that can read:
humidity, temperature, pressure, light, oxidised, reduced, nh3

Raises:
    sensor_not_found: expection if sensor is not connected
"""
from sensorInterface import Sensor, sensor_not_found
from bme280 import BME280
from ltr559 import LTR559
from enviroplus import gas

class enviroplussensor(Sensor):
    """enviroplus sensor class

    Args:
        Sensor (Sensor): Sensor interface
    """
    def __init__(self) -> None:
        # TODO docstring
        super().__init__()
        try:
            self.bme280 = BME280()
            self.ltr559 = LTR559()
            self.gas = gas
        except:
            raise sensor_not_found
        self.data = {
            "Temperature": 0,
             "Pressure": 1000,
             "Humidity": 0,
             "Light" : 0,
             "Oxidised": 0,
             "Reduced": 0,
             "Nh3": 0
        }

    def pull_data(self):
        """Get data from sensor and save to to dictionary
        """
        self.data["Temperature"] = self.bme280.get_temperature()
        self.data["Pressure"] = self.bme280.get_pressure()
        self.data["Humidity"] = self.bme280.get_humidity()
        self.data["Light"] = self.ltr559.get_lux()
        self.data["Oxidised"] = self.gas.read_oxidising()
        self.data["Reduced"] = self.gas.read_reducing()
        self.data["Nh3"] = self.gas.read_nh3()
