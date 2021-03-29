"""ds18b20sensor sensor class that can read:
humidity and it is waterproof

Raises:
    sensor_not_found: expection if sensor is not connected
"""
from w1thermsensor import W1ThermSensor
from sensorInterface import Sensor, sensor_not_found

class ds18b20sensor(Sensor):
    """ds18b20 sensor class

    Args:
        Sensor (Sensor): Sensor interface
    """
    def __init__(self) -> None:
        # TODO docstring
        super().__init__()
        try:
            self.me = W1ThermSensor()
        except:
            raise sensor_not_found
        self.data = {
            "Temperature": 0
        }

    def pull_data(self):
        """Get data from sensor and save to to dictionary
        """
        self.data["Temperature"] = self.me.get_temperature()
