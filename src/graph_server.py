import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from datetime import timedelta
from slugify import slugify

def calc_percentage(num, den):
    if den == 0:
        return 0
    return 100.0 * num / den

class GraphServer(object):
    def __init__(self, calls):
        self._calls = calls
        self._app = self._create_app()

    def _create_app(self):
        app = dash.Dash()

        by_time_graphs = self._create_calls_by_time_graphs()
        by_day_graphs = self._create_calls_by_day_graphs()

        app.layout = html.Div([
            html.H1('Cold calls'),
        ] + by_time_graphs + by_day_graphs)

        return app

    def _create_calls_by_day_graphs(self):
        calls_by_day = self._calls.grouped_by_day()
        return self._create_grouped_calls_graphs(
            grouped_calls=calls_by_day,
            name='By day',
        )

    def _create_calls_by_time_graphs(self):
        calls_by_time = self._calls.grouped_by_time(delta=timedelta(minutes=30))
        return self._create_grouped_calls_graphs(
            grouped_calls=calls_by_time,
            name='By time',
        )

    def _create_grouped_calls_graphs(self, grouped_calls, name):
        times = []
        total_count = []
        picked_up_count = []
        meetings_count = []
        slug = slugify(name)

        for time, calls in grouped_calls.items():
            times.append(time)
            total_count.append(calls.count())
            picked_up_count.append(calls.picked_up_count())
            meetings_count.append(calls.meetings_count())

        calls_graph = dcc.Graph(
            id='%s-calls' % slug,
            figure=go.Figure(
                layout=go.Layout(
                    title='%s: # calls' % name,
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
            id='%s-success-rate' % slug,
            figure=go.Figure(
                layout=go.Layout(
                    title='%s: success rates' % name,
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
