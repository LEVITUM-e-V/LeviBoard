from dash_extensions import WebSocket
from dash_extensions.enrich import html, dcc, Output, Input, DashProxy

# Client-side function (for performance) that updates the graph.
update_graph = """function(msg) {
    if(!msg){return {};}  // no data, just return
    const data = JSON.parse(msg.data);  // read the data
    return {data: [{y: data, type: "scatter"}]}};  // plot the data
"""
# Create small example app.
app = DashProxy(__name__)
app.layout = html.Div([
    WebSocket(id="ws", url="ws://127.0.0.1:5000/random_data"),
    # First plot
    dcc.Graph(
        id='plot1',
        figure=px.line(id="graph", x='x', y='y1', title='Plot 1')
    ),

    # Second plot
    dcc.Graph(
        id='plot2',
        figure=px.bar(id="graph", x='x', y='y2', title='Plot 2')
    ),

    # Third plot
    dcc.Graph(
        id='plot3',
        figure=px.scatter(id="graph", x='x', y='y3', title='Plot 3')
    ),
])

app.clientside_callback(update_graph, Output("graph", "figure"), Input("ws", "message"))

if __name__ == "__main__":
    app.run_server()