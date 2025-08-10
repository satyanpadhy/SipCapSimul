import streamlit as st
import os
import uuid
from datetime import datetime
from sip_utils import extract_sip_messages, filter_messages, compare_messages, highlight_text_differences
import pandas as pd

# Try to import magic, but handle case where it's not available
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="PCAP SIP Comparator",
    page_icon="📊",
    layout="wide"
)

# Helper functions
def is_valid_pcap(file):
    """Validate if uploaded file is a valid PCAP file"""
    try:
        # Read first 4 bytes to check magic number
        file.seek(0)
        header = file.read(4)
        file.seek(0)  # Reset file pointer
        
        allowed_headers = [b'\xd4\xc3\xb2\xa1', b'\xa1\xb2\xc3\xd4', 
                          b'\x4d\x3c\xb2\xa1', b'\xa1\xb2\x3c\x4d']
        
        if any(header.startswith(mh) for mh in allowed_headers):
            return True
            
        # Fallback: check file extension
        if file.name.lower().endswith(('.pcap', '.pcapng')):
            return True
            
        # Additional fallback: use magic if available
        if MAGIC_AVAILABLE:
            try:
                mime = magic.from_buffer(header, mime=True)
                if mime in [b'data', b'application/vnd.tcpdump.pcap', b'application/octet-stream']:
                    return True
            except Exception:
                pass
                
    except Exception:
        pass
    return False

def save_uploaded_file(uploaded_file):
    """Save uploaded file temporarily and return path"""
    if uploaded_file is not None:
        # Create temp directory if it doesn't exist
        os.makedirs('temp_uploads', exist_ok=True)
        
        # Generate unique filename
        filename = f"{uuid.uuid4()}_{uploaded_file.name}"
        filepath = os.path.join('temp_uploads', filename)
        
        with open(filepath, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        return filepath
    return None

def highlight_differences(text1, text2):
    """Highlight differences between two text strings"""
    ranges1, ranges2 = highlight_text_differences(text1, text2)
    
    # Create highlighted text
    highlighted1 = text1
    highlighted2 = text2
    
    for start, end in ranges1:
        highlighted1 = highlighted1[:start] + f"**{highlighted1[start:end]}**" + highlighted1[end:]
    
    for start, end in ranges2:
        highlighted2 = highlighted2[:start] + f"**{highlighted2[start:end]}**" + highlighted2[end:]
    
    return highlighted1, highlighted2

# Main application
def main():
    st.title("PCAP SIP Comparator")
    
    # Initialize session state
    if 'messages1' not in st.session_state:
        st.session_state.messages1 = []
    if 'messages2' not in st.session_state:
        st.session_state.messages2 = []
    if 'filtered1' not in st.session_state:
        st.session_state.filtered1 = []
    if 'filtered2' not in st.session_state:
        st.session_state.filtered2 = []
    if 'unmatched1' not in st.session_state:
        st.session_state.unmatched1 = []
    if 'unmatched2' not in st.session_state:
        st.session_state.unmatched2 = []
    if 'selected1' not in st.session_state:
        st.session_state.selected1 = None
    if 'selected2' not in st.session_state:
        st.session_state.selected2 = None
    
    # File upload section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("PCAP File 1")
        uploaded_file1 = st.file_uploader(
            "Choose first PCAP file",
            type=['pcap', 'pcapng'],
            key="file1"
        )
    
    with col2:
        st.subheader("PCAP File 2")
        uploaded_file2 = st.file_uploader(
            "Choose second PCAP file",
            type=['pcap', 'pcapng'],
            key="file2"
        )
    
    # Process files when both are uploaded
    if uploaded_file1 and uploaded_file2:
        # Validate files
        if not is_valid_pcap(uploaded_file1) or not is_valid_pcap(uploaded_file2):
            st.error("❌ Invalid file type. Please upload valid PCAP files.")
            return
        
        # Save files temporarily
        filepath1 = save_uploaded_file(uploaded_file1)
        filepath2 = save_uploaded_file(uploaded_file2)
        
        try:
            with st.spinner("🔍 Extracting SIP messages..."):
                messages1 = extract_sip_messages(filepath1)
                messages2 = extract_sip_messages(filepath2)
            
            # Store in session state
            st.session_state.messages1 = messages1
            st.session_state.messages2 = messages2
            st.session_state.filtered1 = messages1
            st.session_state.filtered2 = messages2
            st.session_state.unmatched1 = []
            st.session_state.unmatched2 = []
            
            st.success(f"✅ Extracted {len(messages1)} messages from File 1 and {len(messages2)} messages from File 2")
            
        except Exception as e:
            st.error(f"❌ Error processing files: {str(e)}")
        
        finally:
            # Clean up temporary files
            try:
                if filepath1 and os.path.exists(filepath1):
                    os.remove(filepath1)
                if filepath2 and os.path.exists(filepath2):
                    os.remove(filepath2)
            except Exception:
                pass
    
    # Filtering controls (only show if files are loaded)
    if st.session_state.messages1 or st.session_state.messages2:
        st.subheader("🔍 Filtering & Comparison")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            msg_type = st.selectbox(
                "SIP Type",
                ["ALL", "INVITE", "ACK", "BYE", "CANCEL", "OPTIONS", "REGISTER", "200 OK", "4XX", "5XX", "6XX"]
            )
        
        with col2:
            callid_filter = st.text_input("Call-ID Filter", placeholder="Filter by Call-ID")
        
        with col3:
            threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.8, 0.05)
        
        with col4:
            if st.button("🔍 Apply Filters", type="primary"):
                # Apply filters
                filtered1 = filter_messages(st.session_state.messages1, msg_type, callid_filter)
                filtered2 = filter_messages(st.session_state.messages2, msg_type, callid_filter)
                
                st.session_state.filtered1 = filtered1
                st.session_state.filtered2 = filtered2
                st.session_state.unmatched1 = []
                st.session_state.unmatched2 = []
                
                st.success(f"✅ Filtered: {len(filtered1)} messages in File 1, {len(filtered2)} messages in File 2")
        
        # Compare button
        if st.button("🔄 Compare Messages", type="secondary"):
            with st.spinner("Comparing messages..."):
                # Find unmatched messages
                unmatched1 = []
                unmatched2 = []
                
                for i, msg1 in enumerate(st.session_state.filtered1):
                    found = False
                    for msg2 in st.session_state.filtered2:
                        if compare_messages(msg1, msg2, threshold=threshold):
                            found = True
                            break
                    if not found:
                        unmatched1.append(i)
                
                for i, msg2 in enumerate(st.session_state.filtered2):
                    found = False
                    for msg1 in st.session_state.filtered1:
                        if compare_messages(msg2, msg1, threshold=threshold):
                            found = True
                            break
                    if not found:
                        unmatched2.append(i)
                
                st.session_state.unmatched1 = unmatched1
                st.session_state.unmatched2 = unmatched2
                
                st.success(f"✅ Comparison complete: {len(unmatched1)} unmatched in File 1, {len(unmatched2)} unmatched in File 2")
    
    # Message display section
    if st.session_state.filtered1 or st.session_state.filtered2:
        st.subheader("📋 Messages")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**File 1 Messages**")
            if st.session_state.filtered1:
                for i, msg in enumerate(st.session_state.filtered1):
                    # Create a unique key for each message
                    key = f"msg1_{i}"
                    
                    # Determine background color
                    bg_color = ""
                    if i == st.session_state.selected1:
                        bg_color = "background-color: #cce5ff;"
                    elif i in st.session_state.unmatched1:
                        bg_color = "background-color: #fff3cd;"
                    
                    # Display message
                    with st.container():
                        st.markdown(f"""
                        <div style="padding: 8px; border-bottom: 1px solid #ddd; {bg_color} cursor: pointer;" 
                                 onclick="document.getElementById('select1_{i}').click()">
                            <strong>{msg.get('time', 'Unknown')}</strong> - {msg.get('first_line', msg.get('type', ''))}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"Select", key=f"select1_{i}", help=f"Select message {i}"):
                            st.session_state.selected1 = i
                            st.rerun()
            else:
                st.info("No messages in File 1")
        
        with col2:
            st.write("**File 2 Messages**")
            if st.session_state.filtered2:
                for i, msg in enumerate(st.session_state.filtered2):
                    # Create a unique key for each message
                    key = f"msg2_{i}"
                    
                    # Determine background color
                    bg_color = ""
                    if i == st.session_state.selected2:
                        bg_color = "background-color: #cce5ff;"
                    elif i in st.session_state.unmatched2:
                        bg_color = "background-color: #fff3cd;"
                    
                    # Display message
                    with st.container():
                        st.markdown(f"""
                        <div style="padding: 8px; border-bottom: 1px solid #ddd; {bg_color} cursor: pointer;" 
                                 onclick="document.getElementById('select2_{i}').click()">
                            <strong>{msg.get('time', 'Unknown')}</strong> - {msg.get('first_line', msg.get('type', ''))}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"Select", key=f"select2_{i}", help=f"Select message {i}"):
                            st.session_state.selected2 = i
                            st.rerun()
            else:
                st.info("No messages in File 2")
        
        # Message details section
        if st.session_state.selected1 is not None or st.session_state.selected2 is not None:
            st.subheader("📄 Message Details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**File 1 Message Details**")
                if st.session_state.selected1 is not None and st.session_state.selected1 < len(st.session_state.filtered1):
                    selected_msg1 = st.session_state.filtered1[st.session_state.selected1]
                    st.text_area("Raw Message:", selected_msg1.get('message', ''), height=200, key="details1")
                else:
                    st.info("No message selected")
            
            with col2:
                st.write("**File 2 Message Details**")
                if st.session_state.selected2 is not None and st.session_state.selected2 < len(st.session_state.filtered2):
                    selected_msg2 = st.session_state.filtered2[st.session_state.selected2]
                    st.text_area("Raw Message:", selected_msg2.get('message', ''), height=200, key="details2")
                else:
                    st.info("No message selected")
            
            # Side-by-side comparison
            if (st.session_state.selected1 is not None and st.session_state.selected1 < len(st.session_state.filtered1) and
                st.session_state.selected2 is not None and st.session_state.selected2 < len(st.session_state.filtered2)):
                
                st.subheader("🔄 Side-by-Side Comparison")
                
                msg1 = st.session_state.filtered1[st.session_state.selected1]
                msg2 = st.session_state.filtered2[st.session_state.selected2]
                
                text1 = msg1.get('message', '')
                text2 = msg2.get('message', '')
                
                highlighted1, highlighted2 = highlight_differences(text1, text2)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**File 1 Message (with differences highlighted)**")
                    st.markdown(highlighted1)
                
                with col2:
                    st.write("**File 2 Message (with differences highlighted)**")
                    st.markdown(highlighted2)
                
                # Similarity score
                similarity = compare_messages(msg1, msg2, threshold=threshold)
                st.metric("Messages Match", "✅ Yes" if similarity else "❌ No")
    
    # Instructions when no files are loaded
    if not st.session_state.messages1 and not st.session_state.messages2:
        st.info("📝 Please upload both PCAP files to begin analysis")
        
        st.markdown("""
        ### 🚀 How to Use:
        1. **Upload two PCAP files** using the file uploaders above
        2. **Apply filters** to focus on specific message types or Call-IDs
        3. **Compare messages** to find unmatched messages (highlighted in yellow)
        4. **Click on messages** to view details and compare side-by-side
        5. **View highlighted differences** when both messages are selected
        """)

if __name__ == "__main__":
    main() 