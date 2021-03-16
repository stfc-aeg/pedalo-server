import bme680
from sensorInterface import Sensor, sensor_not_found


class bme680sensor(Sensor):
    def __init__(self) -> None:
        super().__init__()
        try:
            self.me = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except RuntimeError:
            raise sensor_not_found
        except OSError:
            raise sensor_not_found
        self.data = {
            "Temperature": 0,
            "Humidity": 0,
            "Pressure": 1000
        }

    def pull_data(self):
        if (self.me.get_sensor_data()):
            self.data["Temperature"] = self.me.data.temperature
            self.data["Humidity"] = self.me.data.humidity
            self.data["Pressure"] = self.me.data.pressure
            self.data["Gas resistance"] = self.me.data.gas_resistance
        else:
            pass
