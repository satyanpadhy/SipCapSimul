# PCAP SIP Comparator

A web-based tool for comparing SIP protocol messages between two PCAP (Wireshark capture) files. This tool provides an intuitive web interface similar to Beyond Compare, making it easier to analyze and compare SIP messages from any browser.

## Features

- Load and compare two PCAP files simultaneously
- Automatic SIP message extraction
- **Advanced Filtering:** Filter SIP messages by type (e.g., INVITE, ACK, 200 OK, 4XX, etc.) and Call-ID using dropdown and input controls
- **Visual Comparison:** Highlight unmatched messages between the two files
- **Line-by-Line Difference Highlighting:** Select a message in each pane to see line-level differences highlighted in the details view
- User-friendly graphical interface with modern styling and resizable panes
- Time-stamped message display
- Enhanced UI layout with split-screen views and better scrolling for message lists and details

## How It Works

1. **Upload Files:** Use the file inputs to select your two PCAP files. Files are processed and SIP messages are extracted automatically.
2. **Filter Messages:** Use the SIP Type dropdown and Call-ID input to filter messages in both panes. Click "Apply Filters" to update the lists.
3. **Compare:** Click the "Compare" button to highlight messages that are unmatched between the two files (yellow background).
4. **View Differences:** Click a message in each pane to view their details side-by-side. Any differing lines are highlighted for easy comparison.

## Prerequisites

- Python 3.8 or higher
- Required Python packages (listed in requirements.txt)

## Local Development

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   python app.py
   ```
4. Open http://localhost:5000 in your browser

## Usage

1. Open the application in your web browser
2. Using the interface:
   - Use the file inputs to select your PCAP files
   - Files will be automatically processed and compared
   - SIP messages will be displayed in two resizable panes
   - Use the filter controls to search through messages by type or Call-ID
   - Click "Compare" to highlight unmatched messages
   - Click on any message in each pane to view and highlight their line-by-line differences

## Notes

- The tool currently focuses on SIP protocol messages only
- Messages are compared using a similarity threshold of 80%
- Only UTF-8 encoded SIP messages are supported

## Limitations

- Large PCAP files may take longer to process
- Currently only supports UDP-based SIP messages
- Message comparison is based on content similarity, not strict equality

## Deployment

This is a web application built with Python Flask. Here are several deployment options:

### Heroku Deployment

1. Install Heroku CLI and login:
   ```bash
   heroku login
   ```
2. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```
3. Deploy the application:
   ```bash
   git push heroku main
   ```

### Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t pcap-sip-comparator .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 pcap-sip-comparator
   ```

### Manual Server Deployment

1. Set up a server with Python and required packages
2. Configure Nginx/Apache as reverse proxy
3. Run the application with Gunicorn:
   ```bash
   gunicorn app:app
   ```

### Security Considerations

1. Set up HTTPS using Let's Encrypt
2. Configure proper file upload limits
3. Implement user authentication if needed
4. Regular security updates