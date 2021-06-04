"""Graph - class for producing and returning graph as an image

This module implements graph functionality. It allows to plot a graph
and return it to the wegbrequest handler as an image so it can be
displayed in broweser.
"""
import matplotlib
from datetime import datetime
import matplotlib.pyplot as plt
import io

class Graphplot():
    """Class to plot graph
    """

    def __init__(self, server) -> None:
        self.server = server
    def plotgraph(self,data):
        """Plot graph

        This method will plot a graph from data and return it as an image
        Args:
            data (Queue): In memory data to contsruct a graph

        Returns:
            io.ButesIO: Graph as an image
        """
        plt.close("all")
        x = []
        y = []
        for row in list(data):
            time = row["Time"]
            x.append(datetime.strptime(time,"%H:%M:%S"))
            y.append(float(row[self.server.reading]))
        plt.plot(x,y)
        plt.gcf().autofmt_xdate()
        plt.autoscale(True,'y')
        plt.ylabel(self.server.reading)
        plt.xlabel('Time')
        memdata = io.BytesIO()
        plt.savefig(memdata, format = 'png')
        image = memdata.getvalue()
        return image