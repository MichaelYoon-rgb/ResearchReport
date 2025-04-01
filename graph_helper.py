from PIL import Image
import io
import plotly.express as px
import pandas


class GraphHelper:
    def __init__(self, title, y_label, x_label):
        self.title = title
        self.y_label = y_label
        self.x_label = x_label
        self.parsed_data = pandas.DataFrame([])

    def generate_graph(self, file_name, save=False):
        self.data = []
        
        fig = px.line(self.parsed_data, x=self.x_label, y=self.y_label, title=self.title)
        
        if (save):
            self.save_graph(fig, file_name)
        image = Image.open(io.BytesIO(fig.to_image(format="png", engine="kaleido")))
        img_buffer = io.BytesIO()
        image.save(img_buffer, format="PNG")
        return img_buffer.getvalue()

    def parse_data(self, yearly_data, plotted_metric):
        y_values = []
        for value in yearly_data.values():
            if (plotted_metric in value):
                y_values.append(value[plotted_metric])
            else:
                y_values.append(None)

        df = pandas.DataFrame({
            self.x_label: yearly_data.keys(),
            self.y_label: y_values
        })
        self.parsed_data = df
        return df
    
    def save_graph(self, fig, file_name):
        fig.write_image(file_name)