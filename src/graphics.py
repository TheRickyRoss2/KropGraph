__author__ = "Your name"
__email__ = "Your email"

from collections import deque
from queue import Queue
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

import battery
from backend_kivyagg import FigureCanvasKivyAgg
from gpio_control import GpioControl
from seads_core import SeadsCore
from ups_streamer import UpsStreamer


class Graphics(App):
    data_points = deque([])

    def my_callback(self, dt):
        self.plot_data(self.core.get_power())
        """    
        for appliance in self.core.get_appliances():
            data = appliance.get_data()
            self.plot_data(data)
        """

    def battery_callback(self, dt):
        if not self.ups_queue.empty():
            percent = self.ups_queue.get()
            plt.figure(2)
            self.box2.clear_widgets()
            plt.clf()
            battery.draw_battery(self.box2, percent)

    def plot_data(self, data):
        if data == -1:
            return
        else:
            if (len(self.data_points) == 60):
                test = self.data_points.popleft()
                pass
            self.data_points.append(data)
        plt.figure(1)
        self.box.clear_widgets()
        plt.clf()
        values, timestamps = zip(*self.data_points)
        plt.plot(timestamps, values, color='green')
        ax = plt.gca()
        max_yticks = 5
        yloc = plt.MaxNLocator(max_yticks)
        ax.xaxis.set_major_locator(yloc)
        import matplotlib.dates as mdates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.ylabel('Wh')
        plt.xlabel('Time')

        self.box.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def build(self):
        battery_temp = 1  ##temporary for demonstration purposes
        battery_temp2 = .5  ##temporary for demonstration purposes
        self.core = SeadsCore(['master', 'ttest', 'tttest', 'est'])
        Builder.load_file('./kvlayouts/container.kv')
        graphics = Graphics()
        containerlayout = graphics.build_layout()
        Clock.schedule_interval(self.my_callback, 1)
        graph_widget = containerlayout.ids['graph_widget']
        battery_widget = containerlayout.ids['battery_widget']
        self.box = graph_widget.ids['boxlayout_h']
        plt.style.use("dark_background")
        self.box2 = battery_widget.ids['boxlayout_h']
        Clock.schedule_interval(self.battery_callback, 0.25)

        self.ups_queue = Queue()
        self.ups = UpsStreamer(self.ups_queue)
        self.battery_callback(0)

        # Clock.schedule_once(self.my_callback, 5)
        # Clock.schedule_once(self.my_callback, 5)
        # Clock.schedule_interval(partial(self.battery_callback,battery_temp2), 5)
        return containerlayout

    def build_graph(self):
        """
        returns a widget containing the graph
        """
        # print("test")
        # return Label(text='Hello World')
        # return GraphWidget()

    def build_buttons(self):
        """
        returns a widget containing the buttons
        """
        return ButtonsWidget()

    def build_battery(self):
        return BatteryWidget()

    def build_layout(self):
        """
        returns a layout containing all the other elements
        this should be called
        """
        return ContainerLayout()


class GraphWidget(Widget):
    def __init__(self, **kwargs):
        super(GraphWidget, self).__init__(**kwargs)

class BatteryWidget(Widget):
    def __init__(self, **kwargs):
        super(BatteryWidget, self).__init__(**kwargs)

class ButtonsWidget(Widget):

    def __init__(self, **kwargs):
        super(ButtonsWidget, self).__init__(**kwargs)
        self.gpiocontrol = GpioControl()

    def callback(self, switch, value):
        """
        Callback function for buttons
        :param switch: Text of the switch that was toggled
        :param value: State of the button
        """
        print("%s changed state to %s" % (switch, value))
        if value == 'normal':
            self.gpiocontrol.pin_off(switch)
        elif value == 'down':
            self.gpiocontrol.pin_on(switch)


    def on_touch_down(self, touch):
        super(ButtonsWidget, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        super(ButtonsWidget, self).on_touch_up(touch)


class ContainerLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ContainerLayout, self).__init__(**kwargs)


class TestApp(App):
    data_points = deque([])
    def my_callback(self, dt):
        self.plot_data(self.core.get_power())
        """    
        for appliance in self.core.get_appliances():
            data = appliance.get_data()
            self.plot_data(data)
        """


    def battery_callback(self,percent,temp):
        self.box2.clear_widgets()
        plt.clf()
        battery.draw_battery(self.box2, percent)

    def plot_data(self, data):
        if data == -1:
            return
        else:
            if (len(self.data_points) == 60):
                test = self.data_points.popleft()
                pass
            self.data_points.append(data)
        self.box.clear_widgets()
        plt.clf()
        values, timestamps = zip(*self.data_points)
        plt.plot(timestamps, values, color='blue')
        ax = plt.gca()
        max_yticks = 5
        yloc = plt.MaxNLocator(max_yticks)
        ax.xaxis.set_major_locator(yloc)
        import matplotlib.dates as mdates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.ylabel('kWh')
        self.box.add_widget(FigureCanvasKivyAgg(plt.gcf()))


    def build(self):
        battery_temp = 1    ##temporary for demonstration purposes
        battery_temp2 = .5  ##temporary for demonstration purposes
        self.core = SeadsCore(['master', 'ttest', 'tttest', 'est'])
        Builder.load_file('./kvlayouts/container.kv')
        graphics = Graphics()
        containerlayout = graphics.build_layout()
        Clock.schedule_interval(self.my_callback, 1)
        graph_widget = containerlayout.ids['graph_widget']
        battery_widget = containerlayout.ids['battery_widget']
        self.box = graph_widget.ids['boxlayout_h']
        self.box2 = battery_widget.ids['boxlayout_h1']
        self.battery_callback(battery_temp, 1)
        # Clock.schedule_once(self.my_callback, 5)
        # Clock.schedule_interval(partial(self.battery_callback,battery_temp2), 5)
        return containerlayout


def main():
    # test = Graphics()
    # test.build_graph()

    TestApp().run()

if __name__ == "__main__":
    main()
