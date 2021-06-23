from .step import Step


class DataIntegrate(Step):
    def process(self, data, inputs, utils):
        data = utils.average_price(data)
        return data
