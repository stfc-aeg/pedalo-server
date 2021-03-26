"""BME280 sensor class that can read:
humidity, temperature, pressure.

Raises:
    sensor_not_found: expection if sensor is not connected
"""
from sensorInterface import Sensor, sensor_not_found
import bme280
from smbus import SMBus


class bme280sensor(Sensor):
    """bme280 class

    Args:
        Sensor (Sensor): Sensor interface
    """
    def __init__(self) -> None:
        # TODO docstring
        super().__init__()
        try:
            self.me = bme280.BME280(i2c_dev=SMBus(1))
            self.me.update_sensor()
        except RuntimeError:
            raise sensor_not_found
        self.data = {
            "Temperature": 0,
            "Humidity": 0,
            "Pressure": 100
        }

    def pull_data(self):
        """Get data from sensor and save to to dictionary
        """
        self.data["Temperature"] = self.me.get_temperature()
        self.data["Humidity"] = self.me.get_humidity()
        self.data["Pressure"] = self.me.get_pressure()