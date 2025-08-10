from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from sip_utils import extract_sip_messages, filter_messages, compare_messages, highlight_text_differences
import uuid
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Try to import magic, but handle case where it's not available
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Production configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.environ.get('FLASK_ENV') == 'development'

# Flask-Limiter for rate limiting
limiter = Limiter(get_remote_address, app=app, default_limits=["20 per minute"])

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Helper: Validate file type using python-magic
ALLOWED_MIME_TYPES = {b"application/vnd.tcpdump.pcap", b"application/octet-stream"}
ALLOWED_MAGIC_HEADERS = [b'\xd4\xc3\xb2\xa1', b'\xa1\xb2\xc3\xd4', b'\x4d\x3c\xb2\xa1', b'\xa1\xb2\x3c\x4d']

def is_valid_pcap(filepath):
    try:
        with open(filepath, 'rb') as f:
            header = f.read(4)
            if any(header.startswith(mh) for mh in ALLOWED_MAGIC_HEADERS):
                return True
        # Fallback: check MIME type if magic is available
        if MAGIC_AVAILABLE:
            try:
                mime = magic.from_file(filepath, mime=True)
                if mime in [b'data', b'application/vnd.tcpdump.pcap', b'application/octet-stream']:
                    return True
            except Exception:
                pass
        # Additional fallback: check file extension
        if filepath.lower().endswith(('.pcap', '.pcapng')):
            return True
    except Exception:
        pass
    return False

@app.route('/')
@limiter.exempt
# Home page does not need rate limiting
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
@limiter.limit("10 per minute")
def upload_file():
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({'error': 'Both PCAP files are required'}), 400
    
    file1 = request.files['file1']
    file2 = request.files['file2']
    
    if file1.filename == '' or file2.filename == '':
        return jsonify({'error': 'No selected files'}), 400
    
    # Use random UUID filenames to avoid collisions
    filename1 = f"{uuid.uuid4()}.pcap"
    filename2 = f"{uuid.uuid4()}.pcap"
    filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
    filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
    try:
        file1.save(filepath1)
        file2.save(filepath2)
        # Validate file type
        if not is_valid_pcap(filepath1) or not is_valid_pcap(filepath2):
            os.remove(filepath1)
            os.remove(filepath2)
            return jsonify({'error': 'Invalid file type. Please upload valid PCAP files.'}), 400
        messages1 = extract_sip_messages(filepath1)
        messages2 = extract_sip_messages(filepath2)
        return jsonify({
            'pcap1': messages1,
            'pcap2': messages2
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Always attempt to delete files
        try:
            if os.path.exists(filepath1):
                os.remove(filepath1)
            if os.path.exists(filepath2):
                os.remove(filepath2)
        except Exception:
            pass

@app.route('/compare', methods=['POST'])
@limiter.limit("30 per minute")
def compare():
    data = request.get_json()
    messages1 = data.get('pcap1', [])
    messages2 = data.get('pcap2', [])
    threshold = float(data.get('threshold', 0.8))
    unmatched1 = []
    unmatched2 = []
    for i, msg1 in enumerate(messages1):
        found = False
        for msg2 in messages2:
            if compare_messages(msg1, msg2, threshold=threshold):
                found = True
                break
        if not found:
            unmatched1.append(i)
    for i, msg2 in enumerate(messages2):
        found = False
        for msg1 in messages1:
            if compare_messages(msg2, msg1, threshold=threshold):
                found = True
                break
        if not found:
            unmatched2.append(i)
    return jsonify({'unmatched1': unmatched1, 'unmatched2': unmatched2})

@app.route('/filter', methods=['POST'])
@limiter.limit("30 per minute")
def filter_endpoint():
    data = request.get_json()
    messages = data.get('messages', [])
    msg_type = data.get('msg_type', 'ALL')
    callid_filter = data.get('callid_filter', '')
    filtered = filter_messages(messages, msg_type, callid_filter)
    return jsonify({'filtered': filtered})

@app.route('/diff', methods=['POST'])
@limiter.limit("30 per minute")
def diff_endpoint():
    data = request.get_json()
    text1 = data.get('text1', '')
    text2 = data.get('text2', '')
    ranges1, ranges2 = highlight_text_differences(text1, text2)
    return jsonify({'ranges1': ranges1, 'ranges2': ranges2})

# NOTE: For production, always deploy behind HTTPS to protect uploads in transit.

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])