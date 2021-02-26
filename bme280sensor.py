from sensorInterface import Sensor
import bme280
from smbus import SMBus


class bme280sensor(Sensor):
    def __init__(self) -> None:
        super().__init__()
        try:
            self.me = bme280.BME280(i2c_dev=SMBus(1))
            self.me.update_sensor()
        except RuntimeError:
            raise bme280_not_found
        self.data = {
            "Temperature": 0,
            "Humidity": 0,
            "Pressure": 100
        }

    def pull_data(self):
        self.data["Temperature"] = self.me.get_temperature()
        self.data["Humidity"] = self.me.get_humidity()
        self.data["Pressure"] = self.me.get_pressure()


class bme280_not_found(Exception):
    pass
