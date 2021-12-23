import logging

import datetime


class Logger:
    date_time_format: str

    def __init__(self, date_time_format: str, log_location: str, log_level: int) -> None:
        self.date_time_format = date_time_format
        logging.basicConfig(filename=log_location,
                            filemode='a',
                            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                            datefmt=date_time_format,
                            level=log_level)

    def log_info(self, message):
        logging.info(message + " : " + self._current_dt())

    def _current_dt(self) -> str:
        return datetime.datetime.now().strftime(self.date_time_format)
