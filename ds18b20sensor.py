from w1thermsensor import W1ThermSensor
from sensorInterface import Sensor, sensor_not_found

class ds18b20sensor(Sensor):
    def __init__(self) -> None:
        super().__init__()
        try:
            self.me = W1ThermSensor()
        except:
            raise sensor_not_found
        self.data = {
            "Temperature": 0
        }

    def pull_data(self):
        self.data["Temperature"] = self.me.get_temperature()
