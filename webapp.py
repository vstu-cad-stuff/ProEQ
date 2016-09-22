from flask import render_template, jsonify, url_for, request, redirect
from flask_user import login_required, SQLAlchemyAdapter, UserManager
from werkzeug import secure_filename
from __init__ import app, db
from csv import DictReader
from model import User
from os import path


@app.route('/analyze', methods=['GET', 'POST'])
@login_required
def analyze(file=None):
    if request.method == 'GET':
        return render_template('analyze.html', file=request.args['file'])
    elif request.method == 'POST':
        folder = app.config['UPLOAD_FOLDER']
        file = path.join(folder, secure_filename(request.args['file']))
        if path.exists(file):
            raw = list(DictReader(open(file, 'r'), delimiter=';'))
            window = 96 * 7
            data = list(map(
                lambda x: [x[0], float(x[1]['Energy'].replace(',', '.'))], 
                enumerate(raw[:window])))
            return jsonify({'data': [['x', 'y']] + data})
        return 'File not found', 404

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/load', methods=['GET', 'POST'])
@login_required
def load():
    if request.method == 'GET':
        return render_template('load.html')
    elif request.method == 'POST':
        up_file = request.files.get('file')
        if up_file:
            folder = app.config['UPLOAD_FOLDER']
            filename = path.join(folder, secure_filename(up_file.filename))
            up_file.save(filename)
            return redirect(url_for('analyze', file=up_file.filename))
        return 'Something happened', 400

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    db_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(db_adapter, app)
    app.run(debug=True)