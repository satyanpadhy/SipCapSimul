import streamlit as st
import os
import uuid
import magic
from datetime import datetime
from sip_utils import extract_sip_messages, filter_messages, compare_messages, highlight_text_differences
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO

# Page configuration
st.set_page_config(
    page_title="SIP PCAP Comparison Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .file-upload-box {
        border: 2px dashed #1f77b4;
        border-radius: 0.5rem;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

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
        if file.name.lower().endswith('.pcap'):
            return True
            
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

def create_message_dataframe(messages):
    """Convert messages to pandas DataFrame for analysis"""
    if not messages:
        return pd.DataFrame()
    
    data = []
    for i, msg in enumerate(messages):
        data.append({
            'Index': i,
            'Method': msg.get('method', 'Unknown'),
            'Call-ID': msg.get('call_id', 'Unknown'),
            'From': msg.get('from', 'Unknown'),
            'To': msg.get('to', 'Unknown'),
            'Length': len(msg.get('raw_message', '')),
            'Timestamp': msg.get('timestamp', 'Unknown')
        })
    
    return pd.DataFrame(data)

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
    st.markdown('<h1 class="main-header">📊 SIP PCAP Comparison Tool</h1>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    st.sidebar.header("⚙️ Configuration")
    
    # Similarity threshold
    threshold = st.sidebar.slider(
        "Similarity Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.8,
        step=0.05,
        help="Minimum similarity score for messages to be considered matching"
    )
    
    # Message type filter
    msg_type_filter = st.sidebar.selectbox(
        "Message Type Filter",
        ["ALL", "INVITE", "ACK", "BYE", "CANCEL", "REGISTER", "OPTIONS", "INFO", "PRACK", "UPDATE", "REFER", "SUBSCRIBE", "NOTIFY", "PUBLISH", "MESSAGE"]
    )
    
    # Call-ID filter
    callid_filter = st.sidebar.text_input(
        "Call-ID Filter",
        placeholder="Enter Call-ID to filter messages"
    )
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📁 PCAP File 1")
        uploaded_file1 = st.file_uploader(
            "Choose first PCAP file",
            type=['pcap', 'pcapng'],
            key="file1"
        )
    
    with col2:
        st.subheader("📁 PCAP File 2")
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
            
            # Display file statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("File 1 Messages", len(messages1))
            
            with col2:
                st.metric("File 2 Messages", len(messages2))
            
            with col3:
                st.metric("Total Messages", len(messages1) + len(messages2))
            
            with col4:
                st.metric("Similarity Threshold", f"{threshold:.2f}")
            
            # Filter messages if needed
            if msg_type_filter != "ALL" or callid_filter:
                messages1_filtered = filter_messages(messages1, msg_type_filter, callid_filter)
                messages2_filtered = filter_messages(messages2, msg_type_filter, callid_filter)
            else:
                messages1_filtered = messages1
                messages2_filtered = messages2
            
            # Create DataFrames for analysis
            df1 = create_message_dataframe(messages1_filtered)
            df2 = create_message_dataframe(messages2_filtered)
            
            # Comparison analysis
            st.subheader("🔍 Comparison Analysis")
            
            if st.button("🚀 Compare Messages", type="primary"):
                with st.spinner("Comparing messages..."):
                    # Find unmatched messages
                    unmatched1 = []
                    unmatched2 = []
                    
                    for i, msg1 in enumerate(messages1_filtered):
                        found = False
                        for msg2 in messages2_filtered:
                            if compare_messages(msg1, msg2, threshold=threshold):
                                found = True
                                break
                        if not found:
                            unmatched1.append(i)
                    
                    for i, msg2 in enumerate(messages2_filtered):
                        found = False
                        for msg1 in messages1_filtered:
                            if compare_messages(msg2, msg1, threshold=threshold):
                                found = True
                                break
                        if not found:
                            unmatched2.append(i)
                    
                    # Display results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Unmatched in File 1", len(unmatched1))
                        if unmatched1:
                            st.write("**Unmatched Message Indices:**")
                            st.write(unmatched1)
                    
                    with col2:
                        st.metric("Unmatched in File 2", len(unmatched2))
                        if unmatched2:
                            st.write("**Unmatched Message Indices:**")
                            st.write(unmatched2)
                    
                    # Visualization
                    if len(df1) > 0 or len(df2) > 0:
                        st.subheader("📈 Message Analysis")
                        
                        # Message type distribution
                        if len(df1) > 0:
                            fig1 = px.pie(df1, names='Method', title='File 1 - Message Type Distribution')
                            st.plotly_chart(fig1, use_container_width=True)
                        
                        if len(df2) > 0:
                            fig2 = px.pie(df2, names='Method', title='File 2 - Message Type Distribution')
                            st.plotly_chart(fig2, use_container_width=True)
                        
                        # Message length comparison
                        if len(df1) > 0 and len(df2) > 0:
                            combined_df = pd.concat([
                                df1.assign(File='File 1'),
                                df2.assign(File='File 2')
                            ])
                            
                            fig3 = px.box(combined_df, x='File', y='Length', color='Method',
                                         title='Message Length Distribution by File')
                            st.plotly_chart(fig3, use_container_width=True)
            
            # Message browser
            st.subheader("📋 Message Browser")
            
            tab1, tab2 = st.tabs(["File 1 Messages", "File 2 Messages"])
            
            with tab1:
                if len(df1) > 0:
                    st.dataframe(df1, use_container_width=True)
                    
                    # Message detail viewer
                    if len(messages1_filtered) > 0:
                        msg_index = st.selectbox("Select message to view:", range(len(messages1_filtered)), key="msg1")
                        selected_msg = messages1_filtered[msg_index]
                        
                        st.subheader("Message Details")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Method:**", selected_msg.get('method', 'Unknown'))
                            st.write("**Call-ID:**", selected_msg.get('call_id', 'Unknown'))
                            st.write("**From:**", selected_msg.get('from', 'Unknown'))
                            st.write("**To:**", selected_msg.get('to', 'Unknown'))
                        
                        with col2:
                            st.write("**Length:**", len(selected_msg.get('raw_message', '')))
                            st.write("**Timestamp:**", selected_msg.get('timestamp', 'Unknown'))
                        
                        st.text_area("Raw Message:", selected_msg.get('raw_message', ''), height=200)
                else:
                    st.info("No messages found in File 1")
            
            with tab2:
                if len(df2) > 0:
                    st.dataframe(df2, use_container_width=True)
                    
                    # Message detail viewer
                    if len(messages2_filtered) > 0:
                        msg_index = st.selectbox("Select message to view:", range(len(messages2_filtered)), key="msg2")
                        selected_msg = messages2_filtered[msg_index]
                        
                        st.subheader("Message Details")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Method:**", selected_msg.get('method', 'Unknown'))
                            st.write("**Call-ID:**", selected_msg.get('call_id', 'Unknown'))
                            st.write("**From:**", selected_msg.get('from', 'Unknown'))
                            st.write("**To:**", selected_msg.get('to', 'Unknown'))
                        
                        with col2:
                            st.write("**Length:**", len(selected_msg.get('raw_message', '')))
                            st.write("**Timestamp:**", selected_msg.get('timestamp', 'Unknown'))
                        
                        st.text_area("Raw Message:", selected_msg.get('raw_message', ''), height=200)
                else:
                    st.info("No messages found in File 2")
            
            # Side-by-side comparison
            if len(messages1_filtered) > 0 and len(messages2_filtered) > 0:
                st.subheader("🔄 Side-by-Side Comparison")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    msg1_index = st.selectbox("Select File 1 message:", range(len(messages1_filtered)), key="comp1")
                
                with col2:
                    msg2_index = st.selectbox("Select File 2 message:", range(len(messages2_filtered)), key="comp2")
                
                if st.button("🔍 Compare Selected Messages"):
                    msg1 = messages1_filtered[msg1_index]
                    msg2 = messages2_filtered[msg2_index]
                    
                    text1 = msg1.get('raw_message', '')
                    text2 = msg2.get('raw_message', '')
                    
                    highlighted1, highlighted2 = highlight_differences(text1, text2)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("File 1 Message")
                        st.markdown(highlighted1)
                    
                    with col2:
                        st.subheader("File 2 Message")
                        st.markdown(highlighted2)
                    
                    # Similarity score
                    similarity = compare_messages(msg1, msg2, threshold=threshold)
                    st.metric("Messages Match", "✅ Yes" if similarity else "❌ No")
        
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
    
    elif uploaded_file1 or uploaded_file2:
        st.info("📝 Please upload both PCAP files to begin analysis")
    
    else:
        st.markdown("""
        <div class="file-upload-box">
            <h3>📁 Upload PCAP Files</h3>
            <p>Upload two PCAP files to compare SIP messages</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### 🚀 Features:
        - **SIP Message Extraction**: Automatically extracts SIP messages from PCAP files
        - **Message Comparison**: Compare messages with configurable similarity threshold
        - **Filtering**: Filter by message type and Call-ID
        - **Visualization**: Charts and graphs for message analysis
        - **Side-by-Side Comparison**: Highlight differences between messages
        - **Real-time Analysis**: Interactive interface with immediate results
        """)

if __name__ == "__main__":
    main() 