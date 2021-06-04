"""ds18b20sensor sensor class that can read:
humidity and it is waterproof

Raises:
    sensor_not_found: expection if sensor is not connected
"""
import datetime
from w1thermsensor import W1ThermSensor
from .sensor import Sensor, sensor_not_found

class ds18b20sensor(Sensor):
    """ds18b20 sensor class

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
            self.me = W1ThermSensor()
        except:
            raise sensor_not_found
        self.data = {
            "Time": 0,
            "Temperature": 0
        }

    def pull_data(self):
        """Get data from sensor and save to to dictionary
        """
        self.data["Time"] = datetime.datetime.now().strftime("%H:%M:%S")
        self.data["Temperature"] = self.me.get_temperature()
