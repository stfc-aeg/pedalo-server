import bme680

class sensor():
    def __init__(self,type) -> None:
        self.type = type

    def get_type(self):
        return self.type


class bme680sensor(sensor):
    def __init__(self,type) -> None:
        super().__init__(type)
        self.me = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        self.data = {
            "Temperature" : 0,
            "Humidity" : 0,
            "Pressure" : 1000
        }

    def get_temperature(self):
        return self.data["Temperature"]

test = bme680sensor("bme680")

print(test.get_type())
print(test.get_temperature())