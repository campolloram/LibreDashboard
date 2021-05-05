from flask import Blueprint, render_template, request,session
from flask import current_app as app
from libredashboard.utils import get_plot
import pandas as pd
import plotly
import plotly.graph_objs as go
import numpy as np
import json
import sys
import os
from werkzeug.utils import secure_filename

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@home_bp.route('/', methods=['GET', 'POST'])
def home():
    global ROOT_PATH
    if request.method == 'POST':
        print('POST method!', file=sys.stderr)
        if request.files.get('file'):
            f = request.files['file']
            tmp_path = os.path.join(ROOT_PATH + '/tmp',secure_filename(f.filename))
            f.save(tmp_path)
            df = pd.read_csv(tmp_path)
            print(df.head())
            tmp_filename = 'tmp/my_tmp_file.csv'
            session['df_path'] = tmp_path
            return render_template('home.html', df=df)
        
    return render_template('home.html', df=pd.DataFrame()) 

@home_bp.route('/about', methods=['GET'])
def about():
    """Homepage."""
    return render_template('about.html') 


@home_bp.route('/plot', methods=['GET', 'POST'])
def plot():
    print(request.form)
    path = session['df_path'] if 'df_path' in session else False 
    if path:
        columns = request.form['df']
        print(f'Columns: {columns}')
        df = pd.read_csv(path)
        df = df[columns]
        x_axis = columns[-1]
        print(f'X_AXIS: {x_axis}')
        json = get_plot(df, x_axis)
        return render_template('plot.html', plot=json)
    

def create_plot():

    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe


    data = [
        go.Bar(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON