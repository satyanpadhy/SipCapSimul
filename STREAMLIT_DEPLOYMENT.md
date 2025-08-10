# Streamlit SIP PCAP Comparison Tool - Deployment Guide

## 🚀 Why Streamlit is Perfect for This Tool

- **Interactive Interface**: Real-time updates and responsive UI
- **Built-in File Upload**: Native file upload widgets
- **Data Visualization**: Easy integration with Plotly charts
- **Simpler Deployment**: Often easier than Flask for data apps
- **Better UX**: More intuitive for technical users
- **Session State**: Maintains data between interactions

## 📦 Quick Deploy Options

### 1. Streamlit Cloud (Recommended - Free)
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign up with GitHub
3. Click "New app"
4. Select your repository
5. Set main file path: `streamlit_app.py`
6. Deploy with one click!

### 2. Railway (Free Tier)
1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Add environment variable: `STREAMLIT_SERVER_PORT=8501`
4. Railway will auto-detect and deploy

### 3. Render (Free Tier)
1. Go to [render.com](https://render.com)
2. Create new "Web Service"
3. Connect your repository
4. Configure:
   - **Build Command**: `pip install -r requirements_streamlit.txt`
   - **Start Command**: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`

### 4. Heroku
```bash
# Create Procfile for Streamlit
echo "web: streamlit run streamlit_app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create your-app-name
git add .
git commit -m "Add Streamlit app"
git push heroku main
```

### 5. Google Cloud Run
```bash
# Create Dockerfile
cat > Dockerfile << EOF
FROM python:3.9-slim
WORKDIR /app
COPY requirements_streamlit.txt .
RUN pip install -r requirements_streamlit.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
EOF

# Deploy to Cloud Run
gcloud run deploy --source .
```

## 🔧 Local Development

### Install Dependencies
```bash
pip install -r requirements_streamlit.txt
```

### Run Locally
```bash
streamlit run streamlit_app.py
```

### Development with Auto-reload
```bash
streamlit run streamlit_app.py --server.runOnSave true
```

## 🌐 Environment Variables

Set these in your hosting platform:

```bash
# Optional: Customize Streamlit behavior
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
```

## 📊 Features Overview

### 🎯 Core Features
- **Dual File Upload**: Upload two PCAP files simultaneously
- **Real-time Processing**: Immediate feedback during analysis
- **Interactive Filters**: Sidebar controls for threshold and filtering
- **Message Browser**: Tabbed interface to browse messages
- **Side-by-Side Comparison**: Visual diff highlighting
- **Data Visualization**: Pie charts and box plots for analysis

### 📈 Visualizations
- **Message Type Distribution**: Pie charts showing SIP method breakdown
- **Message Length Analysis**: Box plots comparing message sizes
- **Real-time Metrics**: Live counters and statistics
- **Interactive Tables**: Sortable dataframes with message details

### 🔍 Analysis Tools
- **Similarity Threshold**: Adjustable matching sensitivity
- **Message Filtering**: Filter by type and Call-ID
- **Difference Highlighting**: Bold text for differences
- **Export Capabilities**: Copy data for external analysis

## 🛡️ Security Features

- **File Validation**: PCAP magic number checking
- **Temporary Storage**: Files deleted after processing
- **Input Sanitization**: Safe file handling
- **Session Isolation**: Separate data per user session

## 📱 Responsive Design

- **Wide Layout**: Optimized for desktop analysis
- **Mobile Friendly**: Responsive design for tablets
- **Sidebar Navigation**: Easy access to controls
- **Tabbed Interface**: Organized content sections

## 🚀 Performance Optimizations

- **Lazy Loading**: Data processed only when needed
- **Session State**: Cached results between interactions
- **Efficient File Handling**: Stream-based processing
- **Memory Management**: Automatic cleanup of temporary files

## 🔧 Customization

### Theme Customization
```python
# In streamlit_app.py, add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)
```

### Adding New Visualizations
```python
# Example: Add timeline visualization
import plotly.express as px

def create_timeline_chart(messages):
    df = pd.DataFrame([
        {'timestamp': msg.get('timestamp'), 'method': msg.get('method')}
        for msg in messages
    ])
    fig = px.timeline(df, x_start='timestamp', y='method')
    return fig
```

## 🐛 Troubleshooting

### Common Issues:
1. **Import Errors**: Ensure all requirements are installed
2. **File Upload Issues**: Check file size limits and permissions
3. **Memory Errors**: Large PCAP files may cause issues
4. **Port Conflicts**: Ensure port 8501 is available

### Debug Mode:
```bash
streamlit run streamlit_app.py --logger.level debug
```

## 📈 Monitoring

### Built-in Streamlit Analytics:
- Page views and user sessions
- Component usage statistics
- Performance metrics

### Custom Monitoring:
```python
# Add custom metrics
import time

start_time = time.time()
# ... processing ...
st.metric("Processing Time", f"{time.time() - start_time:.2f}s")
```

## 🔄 Migration from Flask

### Key Differences:
- **No Routes**: Streamlit uses function-based flow
- **Session State**: Instead of Flask sessions
- **File Upload**: Native widgets vs. Flask file handling
- **Real-time Updates**: Automatic UI refresh

### Benefits:
- **Simpler Code**: Less boilerplate
- **Better UX**: More interactive interface
- **Easier Deployment**: Streamlit Cloud integration
- **Built-in Features**: File upload, charts, tables

## 🎯 Best Practices

1. **Use Session State**: Store data between interactions
2. **Optimize File Processing**: Process in chunks for large files
3. **Add Progress Indicators**: Use `st.spinner()` for long operations
4. **Handle Errors Gracefully**: Use try-catch blocks
5. **Clean Up Resources**: Delete temporary files
6. **Use Caching**: Cache expensive operations with `@st.cache_data`

## 🚀 Next Steps

1. **Deploy to Streamlit Cloud** for instant sharing
2. **Add Authentication** if needed
3. **Implement Caching** for better performance
4. **Add Export Features** (CSV, JSON)
5. **Create Custom Components** for advanced features 