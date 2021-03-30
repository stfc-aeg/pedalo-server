class Sensor():
    """Sensor interface
    """
    def __init__(self) -> None:
        self.data = {}

    def pull_data(self):
        """Method prototype to pull data from sensor
        """
        pass


class sensor_not_found(Exception):
    """Exception to be raised when no sensor is found

    Args:
        Exception (Exception): Python base exception
    """
    pass