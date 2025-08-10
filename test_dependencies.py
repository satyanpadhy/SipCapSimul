#!/usr/bin/env python3
"""
Quick dependency test for SIP PCAP Comparison Tool
Run this to verify all imports work before deployment
"""

def test_imports():
    """Test all required imports"""
    print("🔍 Testing imports...")
    
    try:
        import streamlit as st
        print("✅ streamlit imported successfully")
    except ImportError as e:
        print(f"❌ streamlit import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import plotly.express as px
        print("✅ plotly.express imported successfully")
    except ImportError as e:
        print(f"⚠️ plotly.express import failed: {e}")
    
    try:
        import plotly.graph_objects as go
        print("✅ plotly.graph_objects imported successfully")
    except ImportError as e:
        print(f"⚠️ plotly.graph_objects import failed: {e}")
    
    try:
        import scapy
        print("✅ scapy imported successfully")
    except ImportError as e:
        print(f"❌ scapy import failed: {e}")
        return False
    
    try:
        from sip_utils import extract_sip_messages, filter_messages, compare_messages, highlight_text_differences
        print("✅ sip_utils imported successfully")
    except ImportError as e:
        print(f"❌ sip_utils import failed: {e}")
        return False
    
    try:
        import magic
        print("✅ python-magic imported successfully")
    except ImportError as e:
        print(f"⚠️ python-magic import failed: {e}")
    
    return True

def test_basic_functionality():
    """Test basic functionality"""
    print("\n🔍 Testing basic functionality...")
    
    try:
        import pandas as pd
        # Test DataFrame creation
        df = pd.DataFrame({'test': [1, 2, 3]})
        print("✅ pandas DataFrame creation works")
    except Exception as e:
        print(f"❌ pandas test failed: {e}")
        return False
    
    try:
        from sip_utils import compare_messages
        # Test basic comparison
        msg1 = {'method': 'INVITE', 'call_id': 'test123'}
        msg2 = {'method': 'INVITE', 'call_id': 'test123'}
        result = compare_messages(msg1, msg2, threshold=0.8)
        print("✅ SIP message comparison works")
    except Exception as e:
        print(f"❌ SIP comparison test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 SIP PCAP Comparison Tool - Dependency Test")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test functionality
    functionality_ok = test_basic_functionality()
    
    print("\n" + "=" * 50)
    if imports_ok and functionality_ok:
        print("🎉 All tests passed! Ready for deployment.")
        return True
    else:
        print("❌ Some tests failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 