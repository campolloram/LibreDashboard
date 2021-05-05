from flask import Blueprint, render_template, request, session, url_for
from flask import current_app as app
from libredashboard.utils import get_plot
import pandas as pd
import plotly
import plotly.graph_objs as go
import numpy as np
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


# Context Processors
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static' or endpoint == 'templates':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


# Routes
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
            return render_template('home.html', df=df, columns=df.columns)
        
    return render_template('home.html', df=pd.DataFrame(), columns=[]) 


@home_bp.route('/about', methods=['GET'])
def about():
    """Homepage."""
    return render_template('about.html') 


@home_bp.route('/plot', methods=['GET', 'POST'])
def plot():
    path = session['df_path'] if 'df_path' in session else False 
    if path:
        columns = request.form.getlist('df')
        df = pd.read_csv(path)
        x_axis = request.form['x_axis']
        complete_columns = columns + [x_axis]
        
        df = df[complete_columns]
        json = get_plot(df, x_axis)
        return render_template('plot.html', plot=json)
