"""BME680 sensor class that can read:
humidity, temperature, pressure, gas resistance

Raises:
    sensor_not_found: expection if sensor is not connected
"""
import datetime
from bme680 import BME680
from .sensor import Sensor, sensor_not_found


class bme680sensor(Sensor):
    """bme680 class

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
            self.me = BME680()
        except RuntimeError:
            raise sensor_not_found
        except OSError:
            raise sensor_not_found
        self.data = {
            "Time": 0,
            "Temperature": 0,
            "Humidity": 0,
            "Pressure": 1000
        }

    def pull_data(self):
        """Get data from sensor and save to to dictionary
        """
        if (self.me.get_sensor_data()):
            self.data["Time"] = datetime.datetime.now().strftime("%H:%M:%S")
            self.data["Temperature"] = self.me.data.temperature
            self.data["Humidity"] = self.me.data.humidity
            self.data["Pressure"] = self.me.data.pressure
            self.data["Gas resistance"] = self.me.data.gas_resistance
        else:
            pass
