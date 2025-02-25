from flask import Blueprint, render_template, flash, redirect, url_for, session, request, jsonify
from app.utils.decorators import login_required
from app.models.log import Log
from app.models.payload import Payload
from app import db, socketio
import pandas as pd
import os

main_bp = Blueprint('main', __name__,
                   static_folder='../static',
                   static_url_path='/static')

@main_bp.route('/testing')
def index():
    try:
        logs = Log.query.order_by(Log.log_time.desc()).all()
        return render_template('testing.html', logs=logs)
    except Exception as e:
        flash('Error fetching logs data', 'danger')
        return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/export')
@login_required
def export():
    try:
        logs = Log.query.order_by(Log.log_time.desc()).all()
        data = [{'log_time': log.log_time, 'severity': log.severity, 'message': log.message} for log in logs]
        df = pd.DataFrame(data)
        df.drop(columns=['delete', 'view more'], errors='ignore', inplace=True)

        export_path = os.path.join('exports', 'logs.xlsx')
        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        df.to_excel(export_path, index=False)

        return jsonify(success=True, message='Logs exported successfully.', file_path=export_path)
    except Exception as e:
        flash('Error exporting logs', 'danger')
        return redirect(url_for('main.dashboard'))

@main_bp.route('/importt')
@login_required
def importt():
    payloads = Payload.query.all()
    return render_template('importt.html', payloads=payloads)

@main_bp.route('/view-payloads', methods=['GET'])
@login_required
def view_payloads():
    try:
        payloads = Payload.query.all()
        return render_template('view_payloads.html', payloads=payloads)
    except Exception as e:
        flash('Error fetching payload data', 'danger')
        return redirect(url_for('main.dashboard'))

@main_bp.route('/delete-payload/<int:id>', methods=['DELETE'])
def delete_payload(id):
    payload = Payload.query.get(id)
    if payload:
        db.session.delete(payload)
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False, message='Payload not found')

@main_bp.route('/account_settings')
@login_required
def account_settings():
    return render_template('account_settings.html')

@main_bp.route('/upload-payload', methods=['POST'])
@login_required
def upload_payload():
    if 'file' not in request.files:
        return jsonify(success=False, message='No file part')
    
    file = request.files['file']
    if file.filename == '':
        return jsonify(success=False, message='No selected file')

    allowed_extensions = {'txt', 'csv', 'xlsx'}
    file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    
    if file_extension not in allowed_extensions:
        return jsonify(success=False, message='Invalid file type. Please upload .txt, .csv, or .xlsx files.')

    nama_payload = request.form.get('nama_payload')
    severity = request.form.get('severity')

    try:
        if file_extension == 'txt':
            content = file.read().decode('utf-8')
            lines = content.splitlines()
            jumlah_baris = len(lines)
            log_entry = Payload(nama_payload=nama_payload, jumlah_baris=jumlah_baris, severity=severity)
            db.session.add(log_entry)

        elif file_extension == 'csv':
            df = pd.read_csv(file)
            for _, row in df.iterrows():
                log_entry = Payload(nama_payload=row['nama_payload'], jumlah_baris=row['jumlah_baris'], severity=row['severity'])
                db.session.add(log_entry)
        
        elif file_extension == 'xlsx':
            df = pd.read_excel(file)
            for _, row in df.iterrows():
                log_entry = Payload(nama_payload=row['nama_payload'], jumlah_baris=row['jumlah_baris'], severity=row['severity'])
                db.session.add(log_entry)

        db.session.commit()
        return jsonify(success=True, payload={'nama_payload': nama_payload, 'jumlah_baris': jumlah_baris, 'severity': severity})
    except Exception as e:
        return jsonify(success=False, message=str(e))

@main_bp.route('/get_log_data', methods=['GET'])
@login_required
def get_log_data():
    try:
        logs = Log.query.all()
        severity_count = {'Informative': 0, 'Low': 0, 'Medium': 0, 'High': 0, 'Critical': 0}
        for log in logs:
            severity_count[log.severity] += 1
        return jsonify(severity_count)
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500
    
@main_bp.route('/delete-log/<int:id>', methods=['POST', 'DELETE'])
@login_required
def delete_log(id):
    try:
        log_entry = Log.query.get(id)
        if not log_entry:
            return jsonify(success=False, message='Log entry not found'), 404
        db.session.delete(log_entry)
        db.session.commit()
        return jsonify(success=True, message='Log entry deleted successfully')
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

@main_bp.route('/detect-threat', methods=['POST'])
def detect_threat():
    threat_data = request.json
    socketio.emit('new_threat', threat_data)
    return jsonify(success=True)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
