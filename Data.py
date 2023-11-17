import _csv
import csv
import os
import subprocess
from datetime import datetime, time, timedelta
from typing import List, Dict, Final

import numpy as np
import pyedflib
from pyedflib import EdfReader

from Constants import Constants


class Data:

    def __init__(self, file_path: str, file_key: str, bsx_converter_path: str):

        self.file_title: Final[str] = file_path.split('/')[-1]
        self.file_path: Final[str]  = file_key

        self.start_datetime: datetime
        self.final_datetime: datetime
        self.number_of_samples: int

        self.time: List[datetime]
        self.data_dict: Dict[str, List[float]] = {}
        self.data_label: List[str] = []

        if file_path.endswith(Constants.EDF_FILE_END):
            self._call_edf_constructor(file_path)

        elif file_path.endswith(Constants.CSV_FILE_END):
            self._call_csv_constructor(file_path)

        elif file_path.endswith(Constants.BXS_FILE_END):
            self._call_bsx_constructor(file_path, bsx_converter_path)

        else:
            raise Exception('Not a valid file')

    def _call_bsx_constructor(self, file_path: str, bsx_converter_path: str) -> None:
        executable = bsx_converter_path + '/' + Constants.BXS_EXECUTABLE_NAME

        subprocess.call([executable, file_path])

        self._call_edf_constructor(file_path.replace(Constants.BXS_FILE_END, Constants.EDF_FILE_END))

    def _call_edf_constructor(self, file_path: str) -> None:
        edf_reader: EdfReader = pyedflib.EdfReader(file_path)
        signals_labels = edf_reader.getSignalLabels()

        number_of_signals = edf_reader.signals_in_file
        signals_bufs = np.zeros((number_of_signals, edf_reader.getNSamples()[0]))

        self.start_datetime = edf_reader.getStartdatetime()
        self.number_of_samples = edf_reader.getNSamples()[0]

        period = 1 / edf_reader.getSampleFrequency(0)
        delta_time = self.number_of_samples * period
        self.final_datetime = self.start_datetime + timedelta(seconds=delta_time)

        self.time  = [self.start_datetime + timedelta(seconds=(x * period)) for x in range(self.number_of_samples)]

        for i in np.arange(number_of_signals):
            signals_bufs[i, :] = edf_reader.readSignal(i)

            label = signals_labels[i]
            self.data_label.append(label)
            self.data_dict[label] = signals_bufs[i]

        edf_reader.close()

    def _call_csv_constructor(self, file_path: str) -> None:
        file = open(file_path, 'r')
        csv_reader = csv.reader(file)
        file: List[str] = Data._get_file_as_list_of_strings(csv_reader)

        self.start_datetime = datetime.fromisoformat(file[2][0])
        self.final_datetime = datetime.fromisoformat(file[-1][0])

        self.number_of_samples = len(file) - 2
        self.data_label = file[0][1:-1]

        for label in self.data_label:
            self.data_dict[label] = []

        self.time = []

        for row in file[2:]:
            if len(row) > len(self.data_label) + 1:
                continue

            date_time = datetime.fromisoformat(row[0])
            self.time.append(date_time)

            i: int = 1
            for label in self.data_label:
                self.data_dict[label].append(float(row[i]))
                i += 1

    @staticmethod
    def _get_file_as_list_of_strings(csv_reader) -> List[str]:
        file: List[str] = []

        for row in csv_reader:
            file.append(row)

        return file

    @classmethod
    def is_a_valid_path(cls, path: str) -> bool:
        valid  = path.endswith(Constants.CSV_FILE_END)
        valid |= path.endswith(Constants.EDF_FILE_END)
        valid |= path.endswith(Constants.BXS_FILE_END)
        valid &= os.path.exists(path)

        return valid
