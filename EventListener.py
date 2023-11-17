import os.path
from copy import copy
from datetime import datetime

import PySimpleGUI as sg
from PySimpleGUI import Canvas, Text

from Constants import Constants
from Data import Data
from DataSet import DataSet
from FileExporter import FileExporter
from GuiKeys import GuiKeys
from LayoutCreator import LayoutCreator
from PyPlotFigureToCanvas import PyPlotFigureToCanvas


class EventListener:

    data_set: DataSet = DataSet()

    @classmethod
    def list_to_events(cls, event, values, window: sg.Window) -> bool:

        if event == sg.WIN_CLOSED:
            return True

        elif event == GuiKeys.BROWSER_FILE:
            cls._try_to_read_file_and_add_new_data(values, window)

        elif cls._is_remove_button_event(event):
            cls._remove_data_sub_set(event, window)

        elif event.find(GuiKeys.COMMON_SPIN) != -1:
            cls._spin_input(event, values, window)

        elif event  == GuiKeys.SUBMIT_TIME:
            cls._input_new_reference_time(values, window)

        elif event == GuiKeys.EXPORT_DATA:
            cls._call_export_data_set(values)

        return False

    @classmethod
    def _try_to_read_file_and_add_new_data(cls, values, window) -> None:
        file_path = values[GuiKeys.BROWSER_FILE]
        bsx_converter_path = values[GuiKeys.BROWSER_FOLDER]

        if not Data.is_a_valid_path(file_path):
            sg.popup_error(f'Not a valid file: \n {file_path}')
            return

        file_key = cls._get_file_key(file_path)

        if cls.data_set.get_data(file_path) is not None:
            sg.popup_error(f'File already opened: \n {file_path}')
            return

        if not os.path.exists(bsx_converter_path):
            sg.popup_error(f'Bsx converter path does not exist: {bsx_converter_path}')
            return

        data = cls._create_new_data_from_file_reader(file_path, file_key, bsx_converter_path)

        if data is None:
            return

        cls.data_set.add_new_data(data)

        file_layout = LayoutCreator.get_file_in_list_layout(file_key)
        file_list = window[GuiKeys.FILE_LIST]
        window.extend_layout(file_list, file_layout)

        cls._update_data_addition_or_removal(window)

    @classmethod
    def _remove_data_sub_set(cls, event, window):
        element: str = copy(event)
        while True:
            if element.endswith('.edf') or element.endswith('.csv') or element.endswith('.bxs'):
                break
            element = element[0: -1]
        cls.data_set.remove_data(element)
        window[event].Widget.master.pack_forget()
        window[element].Widget.master.pack_forget()
        window.AllKeysDict.pop(event)
        window.AllKeysDict.pop(element)
        cls._update_data_addition_or_removal(window)

    @classmethod
    def _create_new_data_from_file_reader(cls, file_path: str, file_key, bsx_converter_path: str) -> Data or None:
        try:
            data: Data = Data(file_path, file_key, bsx_converter_path)
        except Exception as exception:
            sg.popup_error(f'Could not read file: {file_path}'
                           f'\n\n'
                           f'{exception}')
            return None
        return data

    @classmethod
    def _is_remove_button_event(cls, event) -> bool:
        if not isinstance(event, str):
            return False

        return event.find(GuiKeys.REMOVE_BUTTON) != -1

    @classmethod
    def _update_text_time(cls, test_time: Text, new_time: datetime):
        if new_time is None:
            test_time.update(Constants.EMPTY_TIME)
        else:
            test_time.update(str(new_time))

    @classmethod
    def _spin_input(cls, event, values, window):
        if event == GuiKeys.START_SPIN_MIN_TEN:
            cls.data_set.cut_start_min_ten = values[GuiKeys.START_SPIN_MIN_TEN]

        elif event == GuiKeys.START_SPIN_MIN_UNI:
            cls.data_set.cut_start_min_uni = values[GuiKeys.START_SPIN_MIN_UNI]

        elif event == GuiKeys.START_SPIN_SEC_TEN:
            cls.data_set.cut_start_sec_ten = values[GuiKeys.START_SPIN_SEC_TEN]

        elif event == GuiKeys.START_SPIN_SEC_UNI:
            cls.data_set.cut_start_sec_uni = values[GuiKeys.START_SPIN_SEC_UNI]

        elif event == GuiKeys.FINAL_SPIN_MIN_TEN:
            cls.data_set.cut_final_min_ten = values[GuiKeys.FINAL_SPIN_MIN_TEN]

        elif event == GuiKeys.FINAL_SPIN_MIN_UNI:
            cls.data_set.cut_final_min_uni = values[GuiKeys.FINAL_SPIN_MIN_UNI]

        elif event == GuiKeys.FINAL_SPIN_SEC_TEN:
            cls.data_set.cut_final_sec_ten = values[GuiKeys.FINAL_SPIN_SEC_TEN]

        elif event == GuiKeys.FINAL_SPIN_SEC_UNI:
            cls.data_set.cut_final_sec_uni = values[GuiKeys.FINAL_SPIN_SEC_UNI]

        cls._update_data_addition_or_removal(window)


    @classmethod
    def _input_new_reference_time(cls, values, window: sg.Window):
        time_str: str = values[GuiKeys.REFERENCE_TIME]

        time = None
        try:
            time = datetime.strptime(time_str, Constants.TIME_REGEX_FORMAT)
        except:
            sg.popup_error(f'"{time_str}" does not match format: {Constants.TIME_FORMAT}')

        cls.data_set.update_reference_time(time)
        cls._update_data_addition_or_removal(window)

    @classmethod
    def _update_data_addition_or_removal(cls, window):
        start_time: Text = window[GuiKeys.START_TIME]
        cls._update_text_time(start_time, cls.data_set.get_start_time())

        final_time: Text = window[GuiKeys.FINAL_TIME]
        cls._update_text_time(final_time, cls.data_set.get_final_time())

        canvas: Canvas = window[GuiKeys.CANVAS]
        figure_to_canvas: PyPlotFigureToCanvas = canvas.metadata
        figure_to_canvas.clean_figure()
        figure_to_canvas.draw_figure(cls.data_set)

    @classmethod
    def _call_export_data_set(cls, values):
        if cls.data_set.get_number_of_files() == 0:
            sg.popup_error('No file opened. First open any file')
            return

        if cls.data_set.get_reference_time() is None:
            answer = sg.popup_yes_no('No reference time. Start time will be used. Do you want to continue?')

            if answer == 'No':
                return
            elif answer is None:
                sg.popup_error('Export process was canceled')
                return

        if not cls.data_set.cut_time_is_consistent():
            sg.popup_error('Cut time is inconsistent.'
                           '\n\n'
                           '(Start Cut Time must be shorter than End Cut Time)')
            return

        suggested_name = FileExporter.get_suggested_file_name(cls.data_set)
        file_name = sg.popup_get_text('Enter file name', default_text=suggested_name, title="FileName")
        if not file_name.endswith(Constants.CSV_FILE_END):
            file_name += Constants.CSV_FILE_END

        out_folder: str = values[GuiKeys.BROWSER_FOLDER_OUTPUT]
        FileExporter.export_data_set(cls.data_set, out_folder + '/' + file_name)

    @classmethod
    def _get_file_key(cls, file_path: str) -> str:
        if file_path.endswith(Constants.CSV_FILE_END):
            return file_path

        if file_path.endswith(Constants.EDF_FILE_END):
            return file_path

        return file_path.replace(Constants.BXS_FILE_END, Constants.EDF_FILE_END)
