class PlotlyFigure:
    def __init__(self, fig):
        self.fig = fig
        self.show = False

    def set_color(self, color):
        for it in self.fig.data:
            it.line.color = color
        if self.show:
            self.fig.show()

    def show(self):
        self.fig.show()
        

import plotly.graph_objects as go

def plot(x, y, color='blue', dash='solid', legend='', title='Untitled', xaxis_title='x', yaxis_title='y', show=True):
    # Create a Plotly figure
    fig = go.Figure()
    pfig = PlotlyFigure(fig)

    # Add the scatter plot
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name=legend,
        line=dict(color=color, dash=dash)
    ))

    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        showlegend=True if len(legend) > 0 else False
    )
    if show: fig.show()
    return pfig

def scatter(x, y, color='blue', marker_symbol='circle', legend='', title='Untitled', xaxis_title='x', yaxis_title='y', show=True, classes=None):
    # Create a Plotly figure
    fig = go.Figure()
    pfig = PlotlyFigure(fig)

    # Add the scatter plot
    if classes is not None and len(classes) == len(x):
        # If classes are provided and match the length of x and y, plot each class with a different color
        for cls in set(classes):
            idx = [i for i, c in enumerate(classes) if c == cls]
            fig.add_trace(go.Scatter(
                x=[x[i] for i in idx],
                y=[y[i] for i in idx],
                mode='markers',
                name=f'{legend} {cls}',
                marker=dict(symbol=marker_symbol)
            ))
    else:
        # If classes are not provided or don't match in length, plot all points with the default color
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='markers',
            name=legend,
            marker=dict(color=color, symbol=marker_symbol)
        ))


    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        showlegend=True if len(legend) > 0 else False
    )
    if show: fig.show()
    return pfig
