# PCAP SIP Comparator – Product Backlog

## 1. User Experience & Usability
- Download/export comparison results (PDF, CSV, HTML)
- Session persistence (save/reload comparisons, bookmark filter states)
- Drag-and-drop file upload
- Progress indicators for uploads and processing
- Improved error handling and user feedback
- Responsive design for tablets and mobile

## 2. SIP-Specific Features
- Call flow visualization (ladder diagram/sequence chart)
- Group messages by Call-ID/dialog (expand/collapse call legs)
- Header-level diff (highlight changed SIP headers/values)
- Enhanced search/filter (regex, by IP/port/user agent)
- Decode and pretty-print SIP messages (color-coded, readable format)

## 3. Collaboration & Sharing
- Shareable links to saved comparisons (with expiration/security)
- Annotations/comments on messages or differences

## 4. Performance & Scalability
- Chunked/lazy loading for large PCAPs
- Server-side async processing with job status updates

## 5. Security & Privacy
- File retention policy and "delete now" option
- User authentication (optional, for enterprise/team use)

## 6. Help & Documentation
- Integrated help/tutorial or onboarding tour
- Sample PCAP files for demo/testing

## 7. Advanced/Future Features
- Automated SIP issue detection (missing ACK, retransmissions, malformed headers)
- API access for programmatic comparison (REST API)
- Multi-file comparison (more than two PCAPs at once)

---

**Prioritization for MVP+1:**
1. Call flow visualization (ladder diagram)
2. Header-level diff
3. Export/share results
4. Better error handling and progress feedback
5. Call grouping by Call-ID 