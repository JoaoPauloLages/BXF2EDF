from typing import List
import PySimpleGUI as sg

from Constants import Constants
from GuiKeys import GuiKeys
from PyPlotFigureToCanvas import PyPlotFigureToCanvas


class LayoutCreator:

    @classmethod
    def create_window_layout(cls) -> List:
        inner_layout = [sg.Column(cls._get_file_list_layout(), expand_x=True, expand_y=True),
                        sg.VerticalSeparator(),
                        sg.Column(cls._get_data_exporter_layout(), expand_x=True, expand_y=True)]

        layout = [
            sg.Column(
                [
                    [
                        sg.Text('Add bsx2edf.exe folder path: '),
                        sg.In(size=(25, 1),
                              enable_events=True,
                              key=GuiKeys.BROWSER_FOLDER,
                              readonly=True,
                              expand_x=True,
                              ),
                        sg.FolderBrowse()
                    ],
                    inner_layout
                ],
                expand_x=True,
                expand_y=True),
        ]
        return [layout]

    @classmethod
    def _get_file_list_layout(cls):
        file_list_column = [
            [
                sg.Text('Add new file: '),
                sg.In(size=(25, 1),
                      enable_events=True,
                      key=GuiKeys.BROWSER_FILE,
                      readonly=True,
                      expand_x=True,
                      ),
                sg.FileBrowse(),
            ],
            [
                sg.Column(
                    [[]],
                    size=(40, 20),
                    key=GuiKeys.FILE_LIST,
                    expand_x=True,
                    expand_y=True,
                    scrollable=True
                )
            ],
        ]

        return file_list_column

    @classmethod
    def _get_data_exporter_layout(cls):
        image_viewer_column = [
            cls._get_start_and_final_time(),
            [
                sg.Text('Reference Time: '),
                sg.InputText(size=20, key=GuiKeys.REFERENCE_TIME),
                sg.Button('Submit', key=GuiKeys.SUBMIT_TIME),
                sg.Text(f'(format: {Constants.TIME_FORMAT})')
            ],
            [
                sg.Graph((640, 480),
                         (0, 0),
                         (640, 480),
                         key="-CANVAS-",
                         expand_x=True,
                         expand_y=True,
                         metadata=PyPlotFigureToCanvas())
            ],
            cls._get_spin_cut_layout(),
            [
                sg.Text('Out put folder: ', expand_x=True),
                sg.In(size=(25, 1),
                      enable_events=True,
                      key=GuiKeys.BROWSER_FOLDER_OUTPUT,
                      readonly=True,
                      expand_x=True,
                      ),
                sg.FolderBrowse(),
                sg.Button('Export data', key=GuiKeys.EXPORT_DATA)
            ]
        ]

        return image_viewer_column

    @classmethod
    def get_file_in_list_layout(cls, file_name: str):
        file = [
            [sg.Text(file_name, expand_y=True, expand_x=True)],
            [sg.Button("Remove", key=(file_name + GuiKeys.REMOVE_BUTTON))],
            [sg.HorizontalSeparator()]
        ]

        return [[sg.Column(file, key=file_name)]]

    @classmethod
    def _get_start_and_final_time(cls):
        return [
            sg.Column([
                [sg.Text('Start Time:', expand_x=True, expand_y=True)],
                [sg.Text(Constants.EMPTY_TIME, expand_x=True, expand_y=True, key=GuiKeys.START_TIME)]
            ]),
            sg.VerticalSeparator(),
            sg.Column([
                [sg.Text('Final Time:', expand_x=True, expand_y=True)],
                [sg.Text(Constants.EMPTY_TIME, expand_x=True, expand_y=True, key=GuiKeys.FINAL_TIME)]
            ])
        ]

    @classmethod
    def _get_spin_cut_layout(cls):
        data_minutes = [x for x in range(10)]
        data_seconds_ten = [x for x in range(6)]
        data_seconds_uni = [x for x in range(10)]

        return [
            sg.Column([
                [sg.Text('Start Cut:', expand_x=True, expand_y=True)],
                [
                    sg.Spin(data_minutes, 0, readonly=True, enable_events=True, key=GuiKeys.START_SPIN_MIN_TEN),
                    sg.Spin(data_minutes, 0, readonly=True, enable_events=True, key=GuiKeys.START_SPIN_MIN_UNI),
                    sg.Text(':', expand_x=True, expand_y=True),
                    sg.Spin(data_seconds_ten, 0, readonly=True, enable_events=True, key=GuiKeys.START_SPIN_SEC_TEN),
                    sg.Spin(data_seconds_uni, 0, readonly=True, enable_events=True, key=GuiKeys.START_SPIN_SEC_UNI)
                ]
            ]),
            sg.VerticalSeparator(),
            sg.Column([
                [sg.Text('End Cut:', expand_x=True, expand_y=True)],
                [
                    sg.Spin(data_minutes, 0, readonly=True, enable_events=True, key=GuiKeys.FINAL_SPIN_MIN_TEN),
                    sg.Spin(data_minutes, 0, readonly=True, enable_events=True, key=GuiKeys.FINAL_SPIN_MIN_UNI),
                    sg.Text(':', expand_x=True, expand_y=True),
                    sg.Spin(data_seconds_ten, 0, readonly=True, enable_events=True, key=GuiKeys.FINAL_SPIN_SEC_TEN),
                    sg.Spin(data_seconds_uni, 0, readonly=True, enable_events=True, key=GuiKeys.FINAL_SPIN_SEC_UNI)
                ],
            ]),
        ]
