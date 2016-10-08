from flask_user import login_required, SQLAlchemyAdapter, UserManager, current_user
from flask import render_template, jsonify, url_for, request, redirect
from werkzeug import secure_filename
from __init__ import app, db
from os import path, listdir
from csv import DictReader
from model import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard/analysis', methods=['GET', 'POST'])
@login_required
def dashboard_analysis(file=None):
    if request.method == 'GET':
        return render_template('analysis.html', args={'file': request.args['file']})
    elif request.method == 'POST':
        folder = app.config['UPLOAD_FOLDER']
        filename = path.join(folder, secure_filename(request.args['file']))
        if path.exists(filename):
            raw = list(DictReader(open(filename, 'r'), delimiter=';'))
            window_start, window_end = (0, 96 * 7)
            data = list(map(
                lambda x: [x[0], float(x[1]['Energy'].replace(',', '.'))], 
                enumerate(raw[window_start:window_end])))
            return_data = {
                'data': [['x', 'y']] + data,
                'count': len(raw),
                'range': [window_start, window_end],
                'period': 96, # calculate it!
            }
            return jsonify(return_data)
        return 'File not found', 404

@app.route('/dashboard/data', methods=['GET', 'POST'])
@login_required
def dashboard_data():
    if request.method == 'GET':
        file_list = listdir(app.config['UPLOAD_FOLDER'])
        return render_template('data.html', args={'file_list': file_list})
    elif request.method == 'POST':
        up_file = request.files.get('file')
        if up_file:
            folder = app.config['UPLOAD_FOLDER']
            filename = path.join(folder, secure_filename(up_file.filename))
            up_file.save(filename)
            return redirect(url_for('dashboard_analysis', file=up_file.filename))

@app.route('/dashboard/model', methods=['POST'])
@login_required
def model():
    params = request.get_json()
    # write code for predict model
    # and send result to web-gui
    return 'Okay :)', 200

if __name__ == '__main__':
    db_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(db_adapter, app)
    app.run(debug=True)