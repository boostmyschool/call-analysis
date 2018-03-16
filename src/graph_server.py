import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from datetime import timedelta

def calc_percentage(num, den):
    if den == 0:
        return 0
    return 100.0 * num / den

class GraphServer(object):
    def __init__(self, calls):
        self._calls = calls
        self._app = self._init_app()

    def _init_app(self):
        app = dash.Dash()

        by_time_graphs = self._init_calls_by_time_graphs()

        app.layout = html.Div([
            html.H1('Cold calls'),
        ] + by_time_graphs)

        return app

    def _init_calls_by_time_graphs(self):
        times = []
        total_count = []
        picked_up_count = []
        meetings_count = []
        calls_by_time = self._calls.grouped_by_time(delta=timedelta(minutes=30))

        for time, calls in calls_by_time.items():
            times.append(time)
            total_count.append(calls.count())
            picked_up_count.append(calls.picked_up_count())
            meetings_count.append(calls.meetings_count())

        calls_graph = dcc.Graph(
            id='calls-by-time',
            figure=go.Figure(
                layout=go.Layout(
                    title='Calls by time',
                ),
                data=[
                    go.Bar(
                        name='# calls',
                        x=times,
                        y=total_count,
                    ),
                    go.Bar(
                        name='# picked up',
                        x=times,
                        y=picked_up_count,
                    ),
                    go.Bar(
                        name='# meetings',
                        x=times,
                        y=meetings_count,
                    ),
                ],
            ),
        )

        success_rate_graph = dcc.Graph(
            id='success-rate-by-time',
            figure=go.Figure(
                layout=go.Layout(
                    title='Success rate by time',
                ),
                data=[
                    go.Bar(
                        name='% picked up',
                        x=times,
                        y=[calc_percentage(num, den) for den, num in zip(total_count, picked_up_count)],
                    ),
                    go.Bar(
                        name='% meeting',
                        x=times,
                        y=[calc_percentage(num, den) for den, num in zip(total_count, meetings_count)],
                    ),
                    go.Bar(
                        name='% meeting if picked up',
                        x=times,
                        y=[calc_percentage(num, den) for den, num in zip(picked_up_count, meetings_count)],
                    ),
                ],
            ),
        )

        return [calls_graph, success_rate_graph]

    def run_server(self):
        self._app.run_server()
