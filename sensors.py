import bme680
import bme280
from smbus import SMBus
import time

class sensor():
    def __init__(self,type) -> None:
        self.type = type
        self.data = {
            "Temperature" : 0,
            "Humidity" : 0,
            "Pressure" : 1000
        }

    def get_type(self):
        return self.type


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



class bme280sensor(sensor):
    def __init__(self,type) -> None:
        super().__init__(type)
        try:
            self.me = bme280.BME280(i2c_dev = SMBus(1))
            self.me.update_sensor()
        except:
            raise bme280_not_found

    def pull_data(self):
        self.data["Temperature"] = self.me.get_temperature()
        self.data["Humidity"] = self.me.get_humidity()
        self.data["Pressure"] = self.me.get_pressure()


    def get_temperature(self):
        self.pull_data()
        return self.data["Temperature"]

class bme680_not_found(Exception):
    pass

class bme280_not_found(Exception):
    pass

def main():
    # test = bme680sensor("bme680")
    test2 = bme280sensor("bme280")
    while True:
        test2.pull_data()
        print(test2.data["Temperature"])
        time.sleep(0.5)

if __name__ == "__main__":
    main()