# 📊 Testing Your SIP PCAP Comparison Tool

## Option 1: Create Sample PCAP Files

### Using Wireshark:
1. Open Wireshark
2. Start capturing on your network interface
3. Make a SIP call (VoIP phone, softphone, etc.)
4. Stop capture after a few messages
5. Save as `.pcap` file
6. Repeat for a second capture with different conditions

### Using tcpdump:
```bash
# Capture SIP traffic on port 5060
sudo tcpdump -i any -w capture1.pcap port 5060

# Make some SIP calls, then stop with Ctrl+C
# Repeat for capture2.pcap
```

## Option 2: Download Sample PCAP Files

### Free SIP PCAP Samples:
- [Wireshark Sample Captures](https://wiki.wireshark.org/SampleCaptures)
- [VoIP Sample Captures](https://www.voip-info.org/wiki/view/VoIP+Sample+Captures)
- [SIP Test Files](https://github.com/sipcapture/homer-capture)

### Create Your Own Test Scenarios:
1. **Normal Call Flow**: INVITE → 200 OK → ACK → BYE
2. **Failed Call**: INVITE → 404 Not Found
3. **Different Call IDs**: Same scenario with different Call-IDs
4. **Different Methods**: Mix of INVITE, REGISTER, OPTIONS

## Option 3: Generate Synthetic PCAP Files

### Using Python with Scapy:
```python
from scapy.all import *
import random

def create_sip_packet(method="INVITE", call_id="test123"):
    # Create a basic SIP packet
    sip_msg = f"""INVITE sip:user@example.com SIP/2.0
Via: SIP/2.0/UDP 192.168.1.100:5060
From: <sip:caller@example.com>
To: <sip:user@example.com>
Call-ID: {call_id}
CSeq: 1 INVITE
Contact: <sip:caller@192.168.1.100:5060>
Content-Length: 0

"""
    
    # Create IP/UDP packet
    ip_pkt = IP(src="192.168.1.100", dst="192.168.1.200")
    udp_pkt = UDP(sport=5060, dport=5060)
    
    # Combine and save
    pkt = ip_pkt/udp_pkt/Raw(load=sip_msg)
    return pkt

# Generate multiple packets
packets = []
for i in range(10):
    pkt = create_sip_packet(call_id=f"call_{i}")
    packets.append(pkt)

# Save to PCAP file
wrpcap("sample_sip.pcap", packets)
```

## Testing Scenarios

### 1. Basic Functionality Test:
- Upload two identical PCAP files
- Should show 0 unmatched messages
- All similarity scores should be 1.0

### 2. Difference Detection Test:
- Upload two PCAP files with slight differences
- Adjust similarity threshold
- Verify unmatched messages are detected

### 3. Filtering Test:
- Upload files with mixed SIP methods
- Test message type filtering
- Test Call-ID filtering

### 4. Visualization Test:
- Check pie charts display correctly
- Verify box plots show message length distribution
- Test interactive features

## Expected Results

### For Identical Files:
- ✅ 0 unmatched messages in both files
- ✅ 100% similarity scores
- ✅ Same message counts
- ✅ Identical visualizations

### For Different Files:
- ❌ Some unmatched messages
- ⚠️ Lower similarity scores
- 📊 Different message distributions
- 🔍 Highlighted differences in side-by-side comparison

## Troubleshooting

### Common Issues:
1. **No messages found**: Check if PCAP contains SIP traffic on port 5060
2. **Import errors**: Ensure all dependencies are installed
3. **File upload issues**: Check file size limits
4. **Memory errors**: Try smaller PCAP files

### Debug Tips:
- Use Wireshark to verify PCAP contents
- Check console logs for errors
- Test with known good PCAP files first 