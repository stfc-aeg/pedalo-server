"""BME280 sensor class that can read:
humidity, temperature, pressure.

Raises:
    sensor_not_found: expection if sensor is not connected
"""
import datetime
from .sensor import Sensor, sensor_not_found
from bme280 import BME280


class bme280sensor(Sensor):
    """bme280 class

    Args:
        Sensor (Sensor): Sensor interface
    """
    def __init__(self) -> None:
        """Initiate sensor object

        This is initiate method which creates sensor object
        and creates a list of channels that the sensor will use

        Raises:
            sensor_not_found: raised when sensor cannot be found
        """
        super().__init__()
        try:
            self.me = BME280()
            self.me.update_sensor()
        except RuntimeError:
            raise sensor_not_found
        self.data = {
            "Time" : 0,
            "Temperature": 0,
            "Humidity": 0,
            "Pressure": 100
        }

    def pull_data(self):
        """Get data from sensor and save to to dictionary
        """
        self.data["Time"] = datetime.datetime.now().strftime("%H:%M:%S")
        self.data["Temperature"] = self.me.get_temperature()
        self.data["Humidity"] = self.me.get_humidity()
        self.data["Pressure"] = self.me.get_pressure()