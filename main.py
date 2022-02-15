import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, \
    QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtCore
import pyqtgraph as pg
import random


class Plotter(QMainWindow):
    def __init__(self):
        super(Plotter, self).__init__()

        # Declare and initialize the variables or fields for this class.
        self.showAxisXGrid = True
        self.showAxisYGrid = True
        self.setAxisXLogMode = False
        self.setAxisYLogMode = False
        self.useOpenGL = True
        self.x_axis_label = 'Time in milli-seconds'
        self.x_axis_units = ''
        self.y_axis_label = 'Amplitude'
        self.y_axis_units = ''
        self.curve_title = 'Sine Wave'
        self.axis_x_value = 0
        self.axis_y_value = 0
        self.axis_x_list = list()
        self.axis_y_list = list()

        # Set the global configuration options for PyQTGraph.
        # For more details visit the following link:
        # https://pyqtgraph.readthedocs.io/en/latest/config_options.html
        pg.setConfigOption('useOpenGL', True)
        # Enable anti-aliasing for prettier plots.
        # Enabling antialiasing causes lines to be drawn with smooth edges at the cost of reduced performance.
        pg.setConfigOptions(antialias=True)
        # Set background color to white. 'w'=white,'b'=blue,'r'=red,'k'=black
        pg.setConfigOption('background', 'w')
        # Set foreground color to white.
        pg.setConfigOption('foreground', 'd')
        # If false, dragging with the left button won't pan the scene.
        pg.setConfigOption('leftButtonPan', True)

        # Create an instance of the class pg.PlotWidget().
        self._plotWidget = pg.PlotWidget()
        # Hide context menu.
        self._plotWidget.getPlotItem().setMenuEnabled(False)
        # Use OpenGL.
        self._plotWidget.useOpenGL(True)
        # Set log mode for both axis.
        self._plotWidget.setLogMode(x=self.setAxisXLogMode, y=self.setAxisYLogMode)
        # Show vertical and horizontal grid.
        self._plotWidget.showGrid(x=self.showAxisXGrid, y=self.showAxisYGrid, alpha=1.0)
        # Use html to style the curve title.
        title = "<h1 style=\'color: #505050;\'>" + self.curve_title + "</h1>"
        # Set the curve title.
        self._plotWidget.setTitle(title)
        # Set style for labels.
        self.label_style = {'color': '#555', 'font-size': '14pt'}
        # Set graph Y axis label.
        self._plotWidget.setLabel('left', self.y_axis_label, units=self.y_axis_units, **self.label_style)
        # Set graph X axis label.
        self._plotWidget.setLabel('bottom', self.x_axis_label, units=self.x_axis_units, **self.label_style)
        # Create an instance of a pg.PlotCurveItem to show a curve.
        self._plotCurveItem = pg.PlotCurveItem(None, None,
                                               pen=pg.mkPen(color=(0, 0, 255), width=1, style=Qt.SolidLine))
        # Add the curve to the plot widget
        self._plotWidget.addItem(self._plotCurveItem)

        # Create an instance of a QPushButton and set it up.
        self.button = QPushButton("Pause")
        self.button.setFixedSize(QSize(65, 25))
        self.button.clicked.connect(self.Pause)

        # Create an instance of a QHBoxLayout.
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.button, alignment=Qt.AlignCenter)

        # Create an instance of a QVBoxLayout.
        vertical_layout = QVBoxLayout()
        vertical_layout.setContentsMargins(5, 5, 5, 5)
        vertical_layout.addWidget(self._plotWidget)
        vertical_layout.addLayout(horizontal_layout)

        # Create an instance of a QWidget and set it up.
        widget = QWidget(self)
        palette = widget.palette()
        palette.setColor(widget.backgroundRole(), Qt.white)
        widget.setPalette(palette)
        # It is necessary to setAutoFillBackground(True) on the widget.
        # By default, a QWidget doesn't fill its background.
        widget.setAutoFillBackground(True)
        widget.setLayout(vertical_layout)

        # Sets the given widget to be the main window's central widget.
        # self.setCentralWidget(self._plotWidget)
        self.setCentralWidget(widget)
        # Set the window title.
        self.setWindowTitle("Curve Plotter")
        #
        self.setWindowIcon(QIcon(QPixmap("plot curve icon.png")))

        # To test the method UpdateCurveValues.
        self.timer = QTimer()
        self.timer.timeout.connect(self.PlotSineWaveCurveShowingRangeValues)
        self.timer.start(1)

    @QtCore.pyqtSlot()
    def PlotCurveWithRandomValues(self) -> None:
        # Increment the X axis value.
        self.axis_x_value += 1
        # Create a random value between 1 and 5.
        self.axis_y_value = random.randrange(1, 5, 1)
        # Add new axis X value to list.
        self.axis_x_list.append(self.axis_x_value)
        # Add new axis Y value to list.
        self.axis_y_list.append(self.axis_y_value)
        # Set the data to show.
        self._plotCurveItem.setData(self.axis_x_list, self.axis_y_list)
        # Update the X axis range to be between its minimum and maximum values.
        self._plotWidget.setXRange(min(self.axis_x_list), max(self.axis_x_list))
        # Update the Y axis range to be between its minimum and maximum values.
        self._plotWidget.setYRange(min(self.axis_y_list), max(self.axis_y_list))

    @QtCore.pyqtSlot()
    def PlotCurveWithPassedValues(self, axis_x_value: int, axis_y_value: int) -> None:
        # Add new axis X value to list.
        self.axis_x_list.append(axis_x_value)
        # Add new axis Y value to list.
        self.axis_y_list.append(axis_y_value)
        # Set the data to show.
        self._plotCurveItem.setData(self.axis_x_list, self.axis_y_list)
        # Update the X axis range to be between its minimum and maximum values.
        self._plotWidget.setXRange(min(self.axis_x_list), max(self.axis_x_list))
        # Update the Y axis range to be between its minimum and maximum values.
        self._plotWidget.setYRange(min(self.axis_y_list), max(self.axis_y_list))

    @QtCore.pyqtSlot()
    def PlotSineWaveCurveShowingAllValues(self) -> None:
        # If the angle is greater than 360 deg.
        if self.axis_x_value > 360:
            num_of_times_360_fit_in_number = round(self.axis_x_value / 360)
            axis_x_value_in_0_360_range = self.axis_x_value - (num_of_times_360_fit_in_number * 360)
        else:
            axis_x_value_in_0_360_range = self.axis_x_value
        # Calculate the sin value for an angle between 0-360 deg
        self.axis_y_value = math.sin(math.radians(axis_x_value_in_0_360_range))
        # Add new axis X value to list.
        self.axis_x_list.append(self.axis_x_value)
        # Add new axis Y value to list.
        self.axis_y_list.append(self.axis_y_value)
        # Set the data to show.
        self._plotCurveItem.setData(self.axis_x_list, self.axis_y_list)
        # Update the X axis range to be between its minimum and maximum values.
        self._plotWidget.setXRange(min(self.axis_x_list), max(self.axis_x_list))
        # Set the Y axis range to be between -1 and 1.
        self._plotWidget.setYRange(-1, 1)
        # Increment the x axis value.
        self.axis_x_value += 1

    @QtCore.pyqtSlot()
    def PlotSineWaveCurveShowingRangeValues(self) -> None:
        # If the angle is greater than 360 deg.
        if self.axis_x_value > 360:
            num_of_times_360_fit_in_number = round(self.axis_x_value / 360)
            axis_x_value_in_0_360_range = self.axis_x_value - (num_of_times_360_fit_in_number * 360)
        else:
            axis_x_value_in_0_360_range = self.axis_x_value
        # Calculate the sin value for an angle between 0-360 deg
        self.axis_y_value = math.sin(math.radians(axis_x_value_in_0_360_range))
        # Add new axis X value to list.
        self.axis_x_list.append(self.axis_x_value)
        # Add new axis Y value to list.
        self.axis_y_list.append(self.axis_y_value)
        # Set the data to show.
        self._plotCurveItem.setData(self.axis_x_list, self.axis_y_list)
        # Get the length of the axix x list.
        axis_x_list_length = len(self.axis_x_list)
        if axis_x_list_length > 1000:
            # Update the X axis range to be between its minimum and maximum values.
            self._plotWidget.setXRange(self.axis_x_list[axis_x_list_length - 1000],
                                       self.axis_x_list[axis_x_list_length - 1])
        # Set the Y axis range to be between -1 and 1.
        self._plotWidget.setYRange(-1, 1)
        # Increment the x axis value.
        self.axis_x_value += 1

    @QtCore.pyqtSlot()
    def Pause(self) -> None:
        if self.timer.isActive():
            self.timer.stop()
            self.button.setText("Plot")
        else:
            self.timer.start(1)
            self.button.setText("Pause")


def main():
    # Create a QApplication object. It manages the GUI application's control flow and main settings.
    # It handles widget specific initialization, finalization.
    # For any GUI application using Qt, there is precisely one QApplication object
    app = QApplication(sys.argv)
    # Create an instance of the class MainWindow.
    plotter = Plotter()
    # Show the window.
    plotter.show()
    # Start Qt event loop.
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
