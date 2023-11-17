from datetime import datetime, time, timedelta
from typing import Final

from Data import Data


class DataSet:

    def __init__(self):
        self._data_dictionary: Final[dict[str, Data]] = {}

        self._reference_time: datetime or None = None

        self._start_time: datetime or None = None
        self._final_time: datetime or None = None

        self.cut_start_min_ten: int = 0
        self.cut_start_min_uni: int = 0
        self.cut_start_sec_ten: int = 0
        self.cut_start_sec_uni: int = 0

        self.cut_final_min_ten: int = 0
        self.cut_final_min_uni: int = 0
        self.cut_final_sec_ten: int = 0
        self.cut_final_sec_uni: int = 0

    def add_new_data(self, data: Data) -> None:
        self._data_dictionary[data.file_path] = data

        self._test_new_start_time(data.start_datetime)
        self._test_new_final_time(data.final_datetime)

    def _test_new_start_time(self, new_start_datetime: datetime) -> None:
        if self._start_time is None:
            self._start_time = new_start_datetime

        elif self._start_time > new_start_datetime:
            self._start_time = new_start_datetime

        self.update_reference_time(self._reference_time)

    def _test_new_final_time(self, final_datetime: datetime) -> None:
        if self._final_time is None:
            self._final_time = final_datetime

        elif self._final_time < final_datetime:
            self._final_time = final_datetime

    def remove_data(self, data_path: str) -> None:
        self._remove_start_time(data_path)
        self._remove_final_time(data_path)

        self._data_dictionary.pop(data_path)

    def _remove_start_time(self, data_path):
        data: Data = self._data_dictionary[data_path]

        if data.start_datetime > self._start_time:
            return

        self._redefine_start_time_excluding_data(data_path)

    def _redefine_start_time_excluding_data(self, data_path):
        self._start_time = None
        if len(self._data_dictionary) == 1:
            return

        filtered_keys = filter(lambda k: k != data_path, self._data_dictionary.keys())
        for key in filtered_keys:
            data: Data = self._data_dictionary[key]
            self._test_new_start_time(data.start_datetime)

    def _remove_final_time(self, data_path):
        data: Data = self._data_dictionary[data_path]

        if data.final_datetime < self._final_time:
            return

        self._redefine_final_time_excluding_data(data_path)

    def _redefine_final_time_excluding_data(self, data_path):
        self._final_time = None
        if len(self._data_dictionary) == 1:
            return

        filtered_keys = filter(lambda k: k != data_path, self._data_dictionary.keys())
        for key in filtered_keys:
            data: Data = self._data_dictionary[key]
            self._test_new_final_time(data.final_datetime)

    def get_number_of_files(self) -> int:
        return len(self._data_dictionary)

    def get_data_keys(self):
        return self._data_dictionary.keys()

    def get_data(self, data_path: str) -> Data:
        if data_path in self._data_dictionary:
            return self._data_dictionary[data_path]
        else:
            return None

    def get_start_time(self) -> time:
        return self._start_time

    def get_final_time(self) -> time:
        return self._final_time

    def update_reference_time(self, reference_time: datetime) -> None:
        if reference_time is None:
            return

        if self._start_time is None:
            self._reference_time = reference_time
            return

        date: datetime = self._start_time.date()
        self._reference_time = reference_time.replace(year=date.year, month=date.month, day=date.day)

    def get_reference_time(self):
        return self._reference_time

    def cut_time_is_consistent(self) -> bool:
        start_time: int = self.cut_start_min_ten * 1000 + self.cut_start_min_uni * 100 \
                          + self.cut_start_sec_ten * 10 + self.cut_start_sec_uni

        final_time: int = self.cut_final_min_ten * 1000 + self.cut_final_min_uni * 100 \
                          + self.cut_final_sec_ten * 10 + self.cut_final_sec_uni

        return start_time < final_time

    def get_cut_start_datetime(self) -> datetime:
        minutes: int = self.cut_start_min_ten * 10 + self.cut_start_min_uni
        seconds: int = self.cut_start_sec_ten * 10 + self.cut_start_sec_uni

        time_reference = self._start_time
        if self._reference_time is not None:
            time_reference = self._reference_time

        return time_reference + timedelta(minutes=minutes, seconds=seconds)

    def get_cut_final_datetime(self) -> datetime:
        minutes: int = self.cut_final_min_ten * 10 + self.cut_final_min_uni
        seconds: int = self.cut_final_sec_ten * 10 + self.cut_final_sec_uni

        time_reference = self._start_time
        if self._reference_time is not None:
            time_reference = self._reference_time

        return time_reference + timedelta(minutes=minutes, seconds=seconds)
