# import bme280sensor
# import bme680sensor
# import time

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

# def main():
#     # test = bme680sensor("bme680")
#     test2 = bme280sensor.bme280sensor("bme280")
#     while True:
#         test2.pull_data()
#         print(test2.data["Temperature"])
#         time.sleep(0.5)

# if __name__ == "__main__":
#     main()