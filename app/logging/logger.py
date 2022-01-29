import logging

import datetime
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root


class Logger:
    date_time_format: str

    def __init__(self, date_time_format: str, log_name: str, log_level: int) -> None:
        self.date_time_format = date_time_format
        path = os.path.join(ROOT_DIR, "logs")
        # Create a new folder if it doesn't exist, called "logs"
        if not os.path.exists(path):
            os.mkdir(path)

        # Get a file path to this directory and append the given name for that particular log file
        file_path = path + "\\" + log_name + ".log"
        self.init_logging(file_path, log_level)

    def init_logging(self, file_path: str, log_level: int):
        logging.basicConfig(
            filename=file_path,
            filemode="a",
            format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
            datefmt=self.date_time_format,
            level=log_level,
        )

    def log_info(self, message):
        logging.info(message + " : " + self._current_dt())

    def _current_dt(self) -> str:
        return datetime.datetime.now().strftime(self.date_time_format)

    def log_trade(self, instruction):
        self.log_info(instruction.symbol + " @ " + instruction.weight)
