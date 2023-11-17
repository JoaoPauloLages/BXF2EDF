import PySimpleGUI as sg
from PySimpleGUI import Canvas

from EventListener import EventListener
from GuiKeys import GuiKeys
from LayoutCreator import LayoutCreator


def main():

    sg.theme('DarkGrey3')

    layout = LayoutCreator.create_window_layout()

    window: sg.Window = sg.Window('Window Title', layout, margins=(10, 5), resizable=True)
    window.Finalize()

    canvas: Canvas = window[GuiKeys.CANVAS]
    canvas.metadata.initiate_plot_with_canvas(canvas)

    while True:
        event, values = window.read()
        close_window: bool = EventListener.list_to_events(event, values, window)

        if close_window:
            window.close()
            break


if __name__ == '__main__':
    main()
