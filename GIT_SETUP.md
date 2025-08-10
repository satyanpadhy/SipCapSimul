# 📁 Git Setup Guide - SIP PCAP Comparison Tool

## 🎯 Files to ADD to Git (Essential)

### Core Application Files
```bash
# Main application files
app.py                          # Flask version
streamlit_app.py                # Streamlit version
sip_utils.py                    # SIP processing utilities
requirements.txt                # Flask dependencies
requirements_streamlit.txt      # Streamlit dependencies

# Configuration files
Dockerfile                      # Docker configuration
Procfile                        # Heroku deployment
.gitignore                      # Git ignore rules

# Documentation
README.md                       # Main documentation
DEPLOYMENT.md                   # Flask deployment guide
STREAMLIT_DEPLOYMENT.md         # Streamlit deployment guide
QUICK_DEPLOY.md                 # Quick deployment guide
SAMPLE_DATA.md                  # Testing guide
ENHANCEMENTS.md                 # Enhancement roadmap
GIT_SETUP.md                    # This file

# Templates (for Flask version)
templates/
├── index.html                  # Main web interface

# Other utilities
pcap_compare.py                 # Standalone comparison script
Backlog.md                      # Development backlog
```

### Command to Add Essential Files:
```bash
git add app.py streamlit_app.py sip_utils.py
git add requirements.txt requirements_streamlit.txt
git add Dockerfile Procfile .gitignore
git add README.md DEPLOYMENT.md STREAMLIT_DEPLOYMENT.md
git add QUICK_DEPLOY.md SAMPLE_DATA.md ENHANCEMENTS.md
git add templates/index.html
git add pcap_compare.py Backlog.md
```

## 🚫 Files to EXCLUDE from Git (Already in .gitignore)

### Python Cache & Build Files
- `__pycache__/` - Python bytecode cache
- `*.pyc`, `*.pyo` - Compiled Python files
- `*.egg-info/` - Package metadata
- `build/`, `dist/` - Build directories

### Virtual Environments
- `venv/`, `env/`, `ENV/` - Python virtual environments

### IDE Files
- `.idea/`, `.vscode/` - IDE configuration
- `*.swp`, `*.swo` - Vim swap files

### Application Data
- `uploads/` - Temporary uploaded files
- `*.pcap`, `*.pcapng` - PCAP files (user data)
- `temp_uploads/` - Streamlit temp files

### Environment & Secrets
- `.env`, `.env.local` - Environment variables
- `*.log` - Log files

## 🚀 Complete Git Setup Commands

### Step 1: Initialize Git Repository
```bash
git init
```

### Step 2: Add All Essential Files
```bash
# Add core application files
git add app.py streamlit_app.py sip_utils.py

# Add dependency files
git add requirements.txt requirements_streamlit.txt

# Add deployment configuration
git add Dockerfile Procfile .gitignore

# Add documentation
git add README.md DEPLOYMENT.md STREAMLIT_DEPLOYMENT.md
git add QUICK_DEPLOY.md SAMPLE_DATA.md ENHANCEMENTS.md GIT_SETUP.md

# Add templates and utilities
git add templates/
git add pcap_compare.py Backlog.md
```

### Step 3: Verify What's Being Added
```bash
git status
```

### Step 4: Make Initial Commit
```bash
git commit -m "Initial commit: SIP PCAP Comparison Tool

- Flask web application for SIP message comparison
- Streamlit interactive data app
- PCAP file processing and analysis
- Message filtering and visualization
- Deployment guides for multiple platforms"
```

### Step 5: Connect to GitHub
```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

## 📋 File Structure After Git Setup

```
sip-pcap-comparison-tool/
├── 📄 app.py                    # Flask application
├── 📄 streamlit_app.py          # Streamlit application
├── 📄 sip_utils.py              # SIP processing utilities
├── 📄 requirements.txt          # Flask dependencies
├── 📄 requirements_streamlit.txt # Streamlit dependencies
├── 📄 Dockerfile                # Docker configuration
├── 📄 Procfile                  # Heroku configuration
├── 📄 .gitignore                # Git ignore rules
├── 📁 templates/
│   └── 📄 index.html            # Flask web interface
├── 📄 README.md                 # Main documentation
├── 📄 DEPLOYMENT.md             # Flask deployment guide
├── 📄 STREAMLIT_DEPLOYMENT.md   # Streamlit deployment guide
├── 📄 QUICK_DEPLOY.md           # Quick deployment guide
├── 📄 SAMPLE_DATA.md            # Testing guide
├── 📄 ENHANCEMENTS.md           # Enhancement roadmap
├── 📄 GIT_SETUP.md              # Git setup guide
├── 📄 pcap_compare.py           # Standalone script
└── 📄 Backlog.md                # Development backlog
```

## 🔍 Verify Your Setup

### Check What's Tracked:
```bash
git ls-files
```

### Check What's Ignored:
```bash
git status --ignored
```

### Expected Output:
```bash
# Files that should be tracked:
app.py
streamlit_app.py
sip_utils.py
requirements.txt
requirements_streamlit.txt
Dockerfile
Procfile
.gitignore
README.md
DEPLOYMENT.md
STREAMLIT_DEPLOYMENT.md
QUICK_DEPLOY.md
SAMPLE_DATA.md
ENHANCEMENTS.md
GIT_SETUP.md
templates/index.html
pcap_compare.py
Backlog.md

# Files that should be ignored:
__pycache__/
uploads/
*.pcap
*.pcapng
temp_uploads/
.env
*.log
```

## 🚨 Important Notes

### ✅ DO Include:
- All Python source code
- Configuration files (Dockerfile, Procfile)
- Documentation files
- Template files
- Requirements files

### ❌ DON'T Include:
- PCAP files (user data)
- Temporary upload directories
- Python cache files
- Environment variables
- Log files
- Virtual environments

## 🎯 Quick One-Liner Setup

```bash
# Complete setup in one command
git init && git add . && git commit -m "Initial commit: SIP PCAP Comparison Tool" && git branch -M main
```

This will add all files except those in `.gitignore`, which is exactly what you want! 