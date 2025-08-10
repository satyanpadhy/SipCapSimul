# SIP PCAP Comparison Tool - Deployment Guide

## Quick Deploy Options

### 1. Railway (Recommended - Free)
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect Python and deploy
6. Set environment variable: `SECRET_KEY=your-secret-key-here`

### 2. Render (Free Tier Available)
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment Variable**: `SECRET_KEY=your-secret-key-here`

### 3. Heroku
```bash
# Install Heroku CLI
heroku login
heroku create your-app-name
git add .
git commit -m "Initial deployment"
git push heroku main
heroku config:set SECRET_KEY=your-secret-key-here
```

### 4. PythonAnywhere
1. Sign up at [pythonanywhere.com](https://pythonanywhere.com)
2. Upload files or clone from GitHub
3. Create web app → Flask → Python 3.8+
4. Set working directory to your project folder
5. Configure WSGI file to point to `app.py`
6. Set environment variable in WSGI file

## Environment Variables

Set these in your hosting platform:

```bash
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production
```

## Security Considerations

1. **Always use HTTPS** - Most platforms provide this automatically
2. **Set a strong SECRET_KEY** - Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
3. **Rate limiting** - Already configured in the app
4. **File validation** - PCAP files are validated before processing
5. **Temporary file cleanup** - Files are automatically deleted after processing

## Performance Notes

- **Memory usage**: Moderate (depends on PCAP file sizes)
- **CPU usage**: High during PCAP processing
- **Storage**: Minimal (files are temporary)
- **Bandwidth**: Depends on uploaded file sizes

## Troubleshooting

### Common Issues:
1. **Import errors**: Make sure all requirements are installed
2. **Permission errors**: Check file permissions on uploads folder
3. **Memory errors**: Large PCAP files may cause issues
4. **Timeout errors**: Increase timeout limits for large files

### Logs:
- Check your hosting platform's log viewer
- Flask debug mode will show detailed errors (disable in production)

## Monitoring

Consider adding:
- Application performance monitoring (APM)
- Error tracking (Sentry)
- Uptime monitoring
- File upload analytics

## Scaling

For high traffic:
- Use Redis for rate limiting storage
- Implement file size limits
- Add CDN for static assets
- Consider microservices architecture 