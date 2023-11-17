import csv
from datetime import datetime, time
from typing import List

from Constants import Constants
from Data import Data
from DataSet import DataSet


class FileExporter:

    @staticmethod
    def get_suggested_file_name(data_set: DataSet) -> str:
        name = ''
        for key in data_set.get_data_keys():
            data: Data = data_set.get_data(key)
            name += data.file_title + "_"

        start_time = str(data_set.get_cut_start_datetime().time())
        final_time = str(data_set.get_cut_final_datetime().time())

        name += start_time + "_" + final_time

        return name.replace('.', '_').replace(':', '-') + Constants.CSV_FILE_END

    @classmethod
    def export_data_set(cls, data_set: DataSet, file_full_name: str) -> None:
        csv_data: List[List[str]] = cls._get_csv_filtered_data(data_set)
        with open(file_full_name, 'w', newline='', encoding='UTF8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')#, quotechar='', quoting=csv.QUOTE_MINIMAL)
            for row in csv_data:
                csv_writer.writerow(row)

    @classmethod
    def _get_csv_filtered_data(cls, data_set: DataSet) -> List[List[str]]:
        filtered_data = [[]]
        first_key = True
        for key in data_set.get_data_keys():

            data: Data = data_set.get_data(key)
            start_i, final_i = cls._get_index(data, data_set)

            filtered_data[0].append('time stamp')
            times: List[datetime] = data.time
            for i in range(0, final_i - start_i):

                if len(filtered_data) - 1 == i:
                    filtered_data.append([])

                if not first_key and len(filtered_data[i + 1]) + 1 < len(filtered_data[i]):
                    for j in range(len(filtered_data[i]) - len(filtered_data[i + 1]) - 1):
                        filtered_data[i + 1].append('')

                filtered_data[i + 1].append(str(times[i + start_i]))

            for label in data.data_label:

                filtered_data[0].append(label)
                list_of_values: List[float] = data.data_dict[label]

                for i in range(0, final_i - start_i):
                    filtered_data[i + 1].append(str(list_of_values[i + start_i]))

            first_key = False

        return filtered_data

    @classmethod
    def _get_index(cls, data, data_set):
        start_time: datetime = data_set.get_cut_start_datetime()
        final_time: datetime = data_set.get_cut_final_datetime()

        times: List[datetime] = data.time
        start_index = cls._get_index_of_closest_value(start_time, times)
        final_index = cls._get_index_of_closest_value(final_time, times)

        return start_index, final_index

    @classmethod
    def _get_index_of_closest_value(cls, target_time: datetime, times: List[datetime]) -> int:

        high_index = len(times) - 1
        low_index  = 0

        while low_index < high_index:
            middle_index = low_index + (high_index - low_index + 1) // 2
            if times[middle_index].time() <= target_time.time():
                low_index = middle_index
            else:
                high_index = middle_index - 1

        return high_index






