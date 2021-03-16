class Sensor():
    def __init__(self) -> None:
        self.data = {}

    def pull_data(self):
        pass


class sensor_not_found(Exception):
    pass