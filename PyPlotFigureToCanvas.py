import matplotlib.pyplot as plt
from PySimpleGUI import Canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Chart import Chart
from DataSet import DataSet


class PyPlotFigureToCanvas:
    def __init__(self):
        self._figure: Figure = plt.Figure()
        self._figure_agg = None

    def initiate_plot_with_canvas(self, canvas: Canvas):
        self._figure_agg = self._draw_figure(self._figure, canvas)

    @staticmethod
    def _draw_figure(figure, canvas) -> FigureCanvasTkAgg:
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas.TKCanvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

    def _check_initialization(self) -> None:
        if self._figure_agg is None:
            raise Exception('PyPlotFigureToCanvas was not initialized')

    def clean_figure(self) -> None:
        self._figure.clear()

    def draw_figure(self, data_set: DataSet) -> None:
        self._check_initialization()
        Chart.draw_matplotlib_figure(self._figure, data_set)
        self._figure_agg.draw()
