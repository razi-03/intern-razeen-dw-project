# Lead Generation Workflow Overview

## 1. Lead Scraping & Data Extraction

- Scheduled trigger (runs weekdays at 9 AM)  
- HTTP requests to scrape target websites  
- JavaScript-based data extraction (emails, names, companies, phone numbers)  
- Data cleaning and deduplication  

## 2. Google Sheets Integration

- Automatic storage of leads  
- Status tracking (contacted, response received)  
- Free tier compatible  

## 3. Email Outreach

- Personalized email generation  
- Gmail SMTP integration  
- 3-day automatic follow-up system  
- Works within Gmail's free sending limits  

## 4. Slack Notifications

- New lead alerts  
- Follow-up notifications  
- Response tracking alerts  

## 5. Response Handling

- Webhook to capture lead responses  
- Automatic status updates in Google Sheets  

---

## 📋 Setup Instructions

- Import the JSON into n8n  
- Replace placeholders:  
  - `YOUR_GOOGLE_SHEET_ID` - Your Google Sheet ID  
  - `YOUR_SLACK_CHANNEL_ID` - Your Slack channel ID  
  - `your-email@gmail.com` - Your Gmail address  
  - Credential IDs for Google Sheets, Gmail, and Slack  
- Configure Target URLs in the **Define Target URLs** node  
- Customize email templates in the personalization nodes  
- Set up credentials for Google Sheets, Gmail, and Slack APIs  

---

## ⚠️ Important Notes

- Always respect `robots.txt` and website terms of service  
- LinkedIn scraping may violate their ToS - use public business directories instead  
- Stay within Gmail's 500 emails/day limit  
- Test with a small batch first  
- The workflow is fully functional and ready to import!  
