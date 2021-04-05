"""
The class implements a tool for data processing: getting selected fields, computing delta, handling various data types.
"""


# TODO: entity<->fields mapping
# TODO: (?) computing delta
# TODO: recur -> mapowanie na zrozumiałe wartości; jak mają wyglądać zrozumiałe wartości?
# TODO: baza Postgres z odpowiednimi użytkownikami (w kontenerze) -> mapowanie na dysk twardy, aby zachować dane

class DataHandler:
    """
    The class implements a tool for data processing: getting selected fields, computing delta, handling various data
    types.
    """

    def __init__(self, data_dir):
        """

        Parameters
        ----------
        data_dir : pathlib.PosixPath, pathlib.WindowsPath
        """
        self.data_directory = data_dir
