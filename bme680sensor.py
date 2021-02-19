import bme680
from sensorInterface import sensor
from smbus import SMBus

class bme680sensor(sensor):
    def __init__(self,type) -> None:
        super().__init__(type)
        try:
            self.me = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except RuntimeError:
            raise bme680_not_found
        except OSError:
            raise bme680_not_found

    def pull_data(self):
        if (self.me.get_sensor_data()):
            self.data["Temperature"] = self.me.data.temperature
            self.data["Humidity"] = self.me.data.humidity
            self.data["Pressure"] = self.me.data.pressure
        else:
            pass


    def get_temperature(self):
        self.pull_data()
        return self.data["Temperature"]

class bme680_not_found(Exception):
    pass