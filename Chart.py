from datetime import datetime
from typing import List

import numpy as np
from matplotlib.figure import Figure

from Data import Data
from DataSet import DataSet


class Chart:

    @classmethod
    def draw_matplotlib_figure(cls, figure: Figure, data_set: DataSet) -> None:
        number_of_charts = data_set.get_number_of_files() + 1

        cls._add_data_charts(number_of_charts, data_set, figure)
        cls._add_legend_chart(number_of_charts, data_set, figure)

    @classmethod
    def _add_data_charts(cls, number_of_charts: int, data_set: DataSet, figure: Figure):
        i = 1
        for key in data_set.get_data_keys():
            data: Data = data_set.get_data(key)
            axis = figure.add_subplot(number_of_charts, 1, i)

            axis.set_title(data.file_title)

            x_start = cls._get_x_start_time(data_set)
            axis.set_xlim([x_start, data_set.get_final_time()])

            labels = cls._get_labels_to_plot(data.data_label)
            for label in labels:
                values = data.data_dict[label]
                axis.plot(data.time, values, label=label)

            cls._add_cut_region_to_axis(axis, data_set, x_start)
            cls._add_reference_time_line(axis, data_set)

            axis.set(xticks=[])
            axis.grid()

            i += 1

    @classmethod
    def _add_legend_chart(cls, number_of_charts: int, data_set: DataSet, figure: Figure) -> None:

        if len(data_set.get_data_keys()) == 0:
            return

        files_name = []
        start_time = []
        final_time = []

        for key in data_set.get_data_keys():
            data: Data = data_set.get_data(key)
            files_name.append(data.file_title)
            start_time.append(data.start_datetime)
            final_time.append(data.final_datetime - start_time[-1])

        axis = figure.add_subplot(number_of_charts, 1, number_of_charts)

        y_pos = np.arange(len(files_name))
        axis.barh(y_pos, final_time, left=start_time)

        for i in range(len(files_name)):
            axis.text(start_time[i], y_pos[i], files_name[i])

        x_start = cls._get_x_start_time(data_set)
        axis.set_xlim([x_start, data_set.get_final_time()])

        cls._add_cut_region_to_axis(axis, data_set, x_start)
        cls._add_reference_time_line(axis, data_set)

    @classmethod
    def _get_x_start_time(cls, data_set) -> datetime:
        if data_set.get_reference_time() is None:
            return data_set.get_start_time()

        elif data_set.get_start_time() > data_set.get_reference_time():
            return data_set.get_reference_time()

        else:
            return data_set.get_start_time()

    @classmethod
    def _add_cut_region_to_axis(cls, axis, data_set: DataSet, x_start: datetime) -> None:
        if data_set.cut_time_is_consistent():
            start_cut_time: datetime = data_set.get_cut_start_datetime()
            final_cut_time: datetime = data_set.get_cut_final_datetime()

            axis.axvspan(x_start, start_cut_time, alpha=0.5, color='red')
            axis.axvspan(final_cut_time, data_set.get_final_time(), alpha=0.5, color='red')

    @classmethod
    def _add_reference_time_line(cls, axis, data_set: DataSet) -> None:
        if data_set.get_reference_time() is None:
            return

        axis.axvline(data_set.get_reference_time(), color='lime')

    @classmethod
    def _get_labels_to_plot(cls, labels: List[str]) -> List[str]:
        if len(labels) <= 2:
            return labels

        sub_labels: List[str] = []
        if 'Alpha_AF7' in labels:
            sub_labels.append('Alpha_AF7')

        if 'Alpha_AF8' in labels:
            sub_labels.append('Alpha_AF8')

        if len(sub_labels) == 2:
            return sub_labels

        if not sub_labels:
            return labels[1:3]

        sub_labels.append(labels[1])
        return sub_labels


