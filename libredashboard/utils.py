import plotly
import plotly.graph_objs as go

def get_plot(df, x_axis):
    data = []
    for column in df.columns:
        if column == x_axis:
            continue
        plot = go.Bar(
                x=df[x_axis], # assign x as the dataframe column 'x'
                y=df[column]
            )
        data.append(plot)
    return json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)