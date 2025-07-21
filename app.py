from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from sip_utils import extract_sip_messages, filter_messages, compare_messages, highlight_text_differences

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({'error': 'Both PCAP files are required'}), 400
    
    file1 = request.files['file1']
    file2 = request.files['file2']
    
    if file1.filename == '' or file2.filename == '':
        return jsonify({'error': 'No selected files'}), 400
    
    try:
        # Save and process first file
        filename1 = secure_filename(file1.filename)
        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        file1.save(filepath1)
        messages1 = extract_sip_messages(filepath1)
        
        # Save and process second file
        filename2 = secure_filename(file2.filename)
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
        file2.save(filepath2)
        messages2 = extract_sip_messages(filepath2)
        
        # Clean up uploaded files
        os.remove(filepath1)
        os.remove(filepath2)
        
        return jsonify({
            'pcap1': messages1,
            'pcap2': messages2
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/compare', methods=['POST'])
def compare():
    data = request.get_json()
    messages1 = data.get('pcap1', [])
    messages2 = data.get('pcap2', [])
    threshold = float(data.get('threshold', 0.8))
    # Find messages in pcap1 not matched in pcap2 and vice versa
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
def filter_endpoint():
    data = request.get_json()
    messages = data.get('messages', [])
    msg_type = data.get('msg_type', 'ALL')
    callid_filter = data.get('callid_filter', '')
    filtered = filter_messages(messages, msg_type, callid_filter)
    return jsonify({'filtered': filtered})

@app.route('/diff', methods=['POST'])
def diff_endpoint():
    data = request.get_json()
    text1 = data.get('text1', '')
    text2 = data.get('text2', '')
    ranges1, ranges2 = highlight_text_differences(text1, text2)
    return jsonify({'ranges1': ranges1, 'ranges2': ranges2})

if __name__ == '__main__':
    app.run(debug=True)