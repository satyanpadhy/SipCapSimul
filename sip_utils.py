import re
from scapy.all import rdpcap, UDP, Raw
from difflib import SequenceMatcher

# --- SIP Message Extraction ---
def extract_sip_messages(pcap_path):
    messages = []
    try:
        packets = rdpcap(pcap_path)
        for packet in packets:
            if UDP in packet and Raw in packet:
                try:
                    raw_data = packet[Raw].load.decode('utf-8', errors='ignore')
                    if 'SIP/2.0' in raw_data:
                        # Parse SIP message to get method/status and Call-ID
                        first_line = raw_data.split('\n')[0].strip()
                        call_id = ''
                        for line in raw_data.split('\n'):
                            if 'Call-ID:' in line:
                                call_id = line.split('Call-ID:')[1].strip()
                                break
                        messages.append({
                            'time': float(packet.time),
                            'message': raw_data,
                            'first_line': first_line,
                            'call_id': call_id
                        })
                except Exception:
                    continue
    except Exception:
        pass
    return messages

# --- Filtering ---
def filter_message(msg, msg_type="ALL", callid_filter=""):
    # Message type filter
    if msg_type != "ALL":
        if msg_type in ["4XX", "5XX", "6XX"]:
            first_word = msg['first_line'].split()[0]
            if first_word.isdigit():
                code = int(first_word)
                if msg_type == "4XX" and not (400 <= code <= 499):
                    return False
                if msg_type == "5XX" and not (500 <= code <= 599):
                    return False
                if msg_type == "6XX" and not (600 <= code <= 699):
                    return False
        elif msg_type not in msg['first_line']:
            return False
    # Call-ID filter
    if callid_filter and callid_filter not in msg['call_id']:
        return False
    return True

def filter_messages(messages, msg_type="ALL", callid_filter=""):
    return [msg for msg in messages if filter_message(msg, msg_type, callid_filter)]

# --- Comparison ---
def compare_messages(msg1, msg2, threshold=0.8):
    # Compare Call-IDs
    if msg1['call_id'] and msg2['call_id'] and msg1['call_id'] == msg2['call_id']:
        return True
    # Weighted similarity
    first_line_ratio = SequenceMatcher(None, msg1['first_line'], msg2['first_line']).ratio()
    content_ratio = SequenceMatcher(None, msg1['message'], msg2['message']).ratio()
    weighted_ratio = (first_line_ratio * 0.6) + (content_ratio * 0.4)
    return weighted_ratio > threshold

# --- Highlight Differences ---
def highlight_text_differences(text1, text2):
    import difflib
    d = difflib.Differ()
    diff = list(d.compare(text1.splitlines(True), text2.splitlines(True)))
    text1_ranges = []
    text2_ranges = []
    pos1 = pos2 = 0
    for line in diff:
        if line.startswith('  '):
            pos1 += len(line[2:])
            pos2 += len(line[2:])
        elif line.startswith('- '):
            start = pos1
            pos1 += len(line[2:])
            text1_ranges.append((start, pos1))
        elif line.startswith('+ '):
            start = pos2
            pos2 += len(line[2:])
            text2_ranges.append((start, pos2))
    return text1_ranges, text2_ranges 