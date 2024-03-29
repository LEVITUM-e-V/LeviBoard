from config import Config
import dash devices
from dash_devices.dependencies import Input, Output 
import dash_html_components as html 
import dash_core_components as dcc 
import plotly.express as px 
from threading import Timer

app = dash_devices.Dash(__name__)

from websocket import create_connection 
import json

TELEM = ['light', 'humidity' ] # , 'rain', 'moisture']
class PlantDash:
    def __init__(self, app) -> None:
        self.config = Config()
        self.app = app
        self.initial = {k: [0.0] * 200 for k in TELEM}
        self.timer = None
        self.ws = None
        self.count = 0

        elements = []
        for k in TELEM:
            elements.append(html.Div(f'{k.title()} Measurement'))
            elements.append(dcc. Graph(id-f'{k}_graph' ))
        self.app.layout = html.Div(elements)

    @self.app.callback_connect
    def func(client, connect):
        print(client, connect, len(app.clients))
        if connect and len(app.clients) == 1:
            self.timer_callback()
        elif not connect and len(app.clients) == 0:
            self.timer.cancel()

    def timer_callback(self):
        if self.ws is None:
            self.ws = create_connection(f'ws://{self.config.plantsitter_ip}:{self .config.plantsitter_port}/data' )
        telem = json.loads(self.ws.rec())
        # print(telem)
        # print('***' self.count)
        figures = dict()
        for k in TELEM:
            data = self.initial[k]
            data.append(telem[k])
            data.pop(0)
            figure = px.line({'Time': [i for i in range(len(data))], k.title(): data},
                x='Time',
                y=k.title(), 
                range_y=[0, 1]
            )
            figures[f'{k}_graph'] = {'figure': figure}
        # print(figures)
        self.app.push_mods({
            **figures,
            'progress': {'value': str(self.count)}

        })
        self.count += 1
        self.timer = Timer(0.01, self.timer_callback)
        self.timer.start()

if __name__ == '__main__':
    dash = PlantDash(app)
    app.run_server(debug=True, host='0.0.0.0', port=5000)



# from dash_extensions import WebSocket
# from dash_extensions.enrich import html, dcc, Output, Input, DashProxy

# # Client-side function (for performance) that updates the graph.
# update_graph = """function(msg) {
#     if(!msg){return {};}  // no data, just return
#     const data = JSON.parse(msg.data);  // read the data
#     return {data: [{y: data, type: "scatter"}]}};  // plot the data
# """
# # Create small example app.
# app = DashProxy(__name__)
# app.layout = html.Div([
#     WebSocket(id="ws", url="ws://127.0.0.1:5000/random_data"),
#     # First plot
#     dcc.Graph(
#         id='plot1',
#         figure=px.line(id="graph", x='x', y='y1', title='Plot 1')
#     ),

#     # Second plot
#     dcc.Graph(
#         id='plot2',
#         figure=px.bar(id="graph", x='x', y='y2', title='Plot 2')
#     ),

#     # Third plot
#     dcc.Graph(
#         id='plot3',
#         figure=px.scatter(id="graph", x='x', y='y3', title='Plot 3')
#     ),
# ])

# app.clientside_callback(update_graph, Output("graph", "figure"), Input("ws", "message"))

# if __name__ == "__main__":
#     app.run_server()