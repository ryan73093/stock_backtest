from stock_backtest.analysis_method.call_method import dict_method
from .step import Step


class Analysis(Step):
    def process(self, data, inputs, utils):
        method = dict_method[inputs['METHOD']]
        method.analysis_info(data, inputs, utils)
        print(method.analysis(data, inputs, utils))
        print(method.revenue(data, inputs, utils))
        pass
