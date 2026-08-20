import sys
import os

# Add the parent directory to path so modules can be found
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import uuid
import json
import time
from datetime import datetime

# Import modules from the modules folder
from password_assembly import check_password_with_assembly as password_analyze
from modules.typing_biometrics import analyze as typing_analyze
from modules.behavioral_risk import analyze as behavioral_analyze
from modules.usb_intel import scan as usb_scan
from modules.file_scanner import scan_usb_files, scan_hidden_files
from modules.device_intel import get_profile as device_profile
from modules.threat_engine import calculate_final_score, generate_recommendations

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.urandom(32)
CORS(app)

# Store for active sessions
sessions = {}

@app.route('/')
def index():
    # Serve the HTML file directly without Jinja2 parsing
    return send_from_directory('templates', 'index.html')

@app.route('/begin', methods=['POST'])
def begin_assessment():
    session_id = str(uuid.uuid4())[:8]
    codename = request.json.get('codename', 'SHADOW').upper()
    phantom_id = f"PH-{session_id[:4].upper()}-{session_id[4:6].upper()}{session_id[6:]}"
    
    sessions[session_id] = {
        'codename': codename,
        'phantom_id': phantom_id,
        'created_at': datetime.now().isoformat(),
        'password_data': {},
        'typing_signature': None,
        'behavioral_data': None,
        'usb_data': None,
        'file_scan': None,
        'device_profile': None,
        'final_score': None
    }
    
    return jsonify({'session_id': session_id, 'codename': codename, 'phantom_id': phantom_id})

@app.route('/assess/password', methods=['POST'])
def assess_password():
    data = request.json
    password = data.get('password', '')
    result = password_analyze(password)
    return jsonify(result)

@app.route('/assess/typing', methods=['POST'])
def assess_typing():
    data = request.json
    keystrokes = data.get('keystrokes', [])
    phrase = data.get('phrase', '')
    result = typing_analyze(keystrokes, phrase)
    return jsonify(result)

@app.route('/assess/behavioral', methods=['POST'])
def assess_behavioral():
    data = request.json
    result = behavioral_analyze(data)
    return jsonify(result)

@app.route('/scan/usb', methods=['GET'])
def scan_usb_route():
    result = usb_scan()
    return jsonify(result)

@app.route('/scan/usb/files', methods=['POST'])
def scan_usb_files_route():
    mount_point = request.json.get('mount_point', '')
    result = scan_usb_files(mount_point)
    return jsonify(result)

@app.route('/scan/hidden', methods=['POST'])
def scan_hidden_route():
    mount_point = request.json.get('mount_point', '')
    result = scan_hidden_files(mount_point)
    return jsonify(result)

@app.route('/scan/device', methods=['POST'])
def scan_device_route():
    mount_point = request.json.get('mount_point', '')
    result = device_profile(mount_point)
    return jsonify(result)

@app.route('/generate/report', methods=['POST'])
def generate_report():
    data = request.json
    session_id = data.get('session_id')
    
    if session_id not in sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    session_data = sessions[session_id]
    
    # Combine all assessments
    final_score = calculate_final_score(
        session_data.get('password_data', {}),
        session_data.get('typing_signature', {}),
        session_data.get('behavioral_data', {}),
        session_data.get('usb_data', {}),
        session_data.get('file_scan', {})
    )
    
    session_data['final_score'] = final_score
    
    recommendations = generate_recommendations(final_score, session_data)
    
    report = {
        'subject': session_data['codename'],
        'phantom_id': session_data['phantom_id'],
        'overall_score': final_score['total'],
        'components': {
            'password': final_score.get('password', 0),
            'typing': final_score.get('typing', 0),
            'behavioral': final_score.get('behavioral', 0),
            'usb': final_score.get('usb', 0),
            'files': final_score.get('files', 0)
        },
        'threat_exposure': final_score.get('threat_level', 'Unknown'),
        'recommendations': recommendations,
        'generated_at': datetime.now().isoformat()
    }
    
    return jsonify(report)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)