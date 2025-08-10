# 🔧 Deployment Troubleshooting Guide

## 🚨 Common Issues & Solutions

### Issue 1: python-magic-bin Dependency Error

**Error Message:**
```
ERROR: Could not find a version that satisfies the requirement python-magic-bin>=0.4.14
ERROR: No matching distribution found for python-magic-bin>=0.4.14
```

**Solution:**
- ✅ **Fixed**: Removed `python-magic-bin` from requirements files
- ✅ **Fixed**: Added fallback validation using file extensions
- ✅ **Fixed**: Made magic library optional with graceful degradation

**What Changed:**
- `requirements_streamlit.txt` and `requirements.txt` no longer include `python-magic-bin`
- File validation now works with or without the magic library
- Added `.pcapng` extension support

### Issue 2: Streamlit Cloud Deployment Fails

**Common Causes:**
1. **Dependency conflicts**
2. **Missing requirements file**
3. **Incorrect main file path**

**Solutions:**
```bash
# Ensure you're using the correct requirements file
# For Streamlit: requirements_streamlit.txt
# For Flask: requirements.txt

# Check your main file path in Streamlit Cloud
# Should be: streamlit_app.py
```

### Issue 3: File Upload Issues

**Problem:** Files not uploading or processing correctly

**Solutions:**
1. **Check file size limits** (default: 16MB)
2. **Verify file format** (.pcap, .pcapng)
3. **Check browser console** for JavaScript errors

### Issue 4: Memory Errors

**Problem:** Large PCAP files cause memory issues

**Solutions:**
1. **Use smaller test files** first
2. **Check file size** before uploading
3. **Consider chunked processing** for very large files

## 🔧 Platform-Specific Issues

### Streamlit Cloud

**Pros:**
- ✅ Easy deployment
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Built-in analytics

**Cons:**
- ❌ Limited memory (1GB)
- ❌ File size limits
- ❌ Dependency restrictions

**Best Practices:**
```bash
# Use requirements_streamlit.txt
# Keep files under 16MB
# Test with small PCAP files first
```

### Railway

**Pros:**
- ✅ Generous free tier
- ✅ Easy deployment
- ✅ Good performance

**Cons:**
- ❌ Requires credit card for verification

**Best Practices:**
```bash
# Set environment variables
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Render

**Pros:**
- ✅ Free tier available
- ✅ Good documentation
- ✅ Reliable service

**Cons:**
- ❌ Slower cold starts
- ❌ Limited resources on free tier

**Best Practices:**
```bash
# Use these build settings:
# Build Command: pip install -r requirements_streamlit.txt
# Start Command: streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0
```

### Heroku

**Pros:**
- ✅ Mature platform
- ✅ Good documentation
- ✅ Reliable service

**Cons:**
- ❌ No free tier
- ❌ More complex setup

**Best Practices:**
```bash
# Use Procfile for deployment
# Set environment variables
# Monitor dyno usage
```

## 🛠️ Debugging Steps

### Step 1: Check Logs
```bash
# Streamlit Cloud: View logs in dashboard
# Railway: Check deployment logs
# Render: View build and runtime logs
# Heroku: heroku logs --tail
```

### Step 2: Test Locally
```bash
# Test the exact same setup locally
pip install -r requirements_streamlit.txt
streamlit run streamlit_app.py
```

### Step 3: Verify Dependencies
```bash
# Check if all dependencies are available
pip check
pip list
```

### Step 4: Test File Processing
```bash
# Create a minimal test PCAP file
# Test with small files first
# Verify file validation works
```

## 🚀 Quick Fixes

### For python-magic Issues:
```python
# The app now handles missing magic library gracefully
# File validation works with extensions: .pcap, .pcapng
# No action needed - already fixed
```

### For Memory Issues:
```python
# Add file size checks
if uploaded_file.size > 16 * 1024 * 1024:  # 16MB
    st.error("File too large. Please use files under 16MB.")
    return
```

### For Deployment Issues:
```bash
# 1. Use requirements_streamlit.txt for Streamlit
# 2. Set main file path to streamlit_app.py
# 3. Check all files are committed to Git
# 4. Verify .gitignore is correct
```

## 📋 Pre-Deployment Checklist

### ✅ Code Ready:
- [ ] All files committed to Git
- [ ] Requirements files updated
- [ ] No hardcoded paths
- [ ] Error handling implemented

### ✅ Dependencies:
- [ ] `requirements_streamlit.txt` for Streamlit
- [ ] `requirements.txt` for Flask
- [ ] No platform-specific dependencies
- [ ] All imports handled gracefully

### ✅ Configuration:
- [ ] Environment variables set
- [ ] Port configuration correct
- [ ] File paths relative
- [ ] Debug mode disabled

### ✅ Testing:
- [ ] Tested locally
- [ ] Small files work
- [ ] Error messages clear
- [ ] UI responsive

## 🆘 Getting Help

### If Issues Persist:
1. **Check the logs** for specific error messages
2. **Test locally** with the same setup
3. **Try a different platform** (Railway, Render, etc.)
4. **Create a minimal test case** to isolate the issue

### Useful Resources:
- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Railway Documentation](https://docs.railway.app)
- [Render Documentation](https://render.com/docs)
- [Heroku Documentation](https://devcenter.heroku.com)

## 🎯 Success Indicators

### ✅ Deployment Successful:
- App loads without errors
- File upload works
- Processing completes
- Results display correctly

### ✅ Performance Good:
- Page loads in <5 seconds
- File processing <30 seconds
- Memory usage stable
- No timeout errors

### ✅ User Experience:
- Clear error messages
- Progress indicators
- Responsive interface
- Intuitive navigation 