from abc import ABC
from abc import abstractmethod


class AnalysisMethod(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def analysis_info(self, data, inputs, utils):
        pass

    @abstractmethod
    def analysis(self, data, inputs, utils):
        pass

    @abstractmethod
    def revenue(self):
        pass

    @abstractmethod
    def plot_graph(self, data, inputs, utils):
        pass
